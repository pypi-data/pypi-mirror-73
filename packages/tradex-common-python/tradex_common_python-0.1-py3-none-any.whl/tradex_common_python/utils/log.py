import logging
import logging.config
import logging.handlers
from logging import StreamHandler
import sys
import logging as pylog
import logging.handlers as pyhandlers
from distutils.util import strtobool
import multiprocessing
import time
import os

from tradex_common_python.utils.EnhancedRotatingFileHandler import EnhancedRotatingFileHandler

BASIC_FORMAT = '%(asctime)s    %(levelname)s    %(name)s:    %(message)s'
FORMAT = '%(asctime)s:%(levelname)-8s:[%(filename)s:%(lineno)d] %(message)s'


def init_log_to_stream(stream, log_level: int = logging.WARN, file_mode: str = None, log_format: str = BASIC_FORMAT):
    if log_format is None or log_format == '':
        log_format = BASIC_FORMAT
    logging.basicConfig(level=log_level, filemode=file_mode,
                        format=log_format, stream=stream)


def init_log_to_file(file_name, log_level: int = logging.WARN, log_format: str = BASIC_FORMAT,
                     max_bytes=10 * 1024 * 1024,
                     day_format: str = '%Y-%m-%d',
                     to_console: bool = True):
    logging.getLogger().handlers.clear()
    logging.getLogger().setLevel(log_level)
    log_handler = EnhancedRotatingFileHandler(
        filename=file_name, when='MIDNIGHT', interval=1, maxBytes=max_bytes, delay=0)
    log_handler.suffix = day_format
    log_handler.setLevel(log_level)
    log_handler.setFormatter(logging.Formatter(log_format if log_format is not None else BASIC_FORMAT))
    logging.getLogger().addHandler(log_handler)
    if to_console:
        console_log_handler = StreamHandler(stream=sys.stdout)
        console_log_handler.setLevel(log_level)
        console_log_handler.setFormatter(logging.Formatter(log_format if log_format is not None else BASIC_FORMAT))
        logging.getLogger().addHandler(console_log_handler)


def init_log_to_console(log_level: int = logging.WARN, log_format: str = BASIC_FORMAT):
    if log_format is None or log_format == '':
        log_format = BASIC_FORMAT
    logging.basicConfig(level=log_level, format=log_format, stream=sys.stdout)


def log_level(name: str) -> int:
    if name == 'INFO':
        return logging.INFO
    elif name == 'ERROR':
        return logging.ERROR
    elif name == 'DEBUG':
        return logging.DEBUG
    return logging.WARN


# [loggers]
# keys=root,sampleLogger

# [handlers]
# keys=consoleHandler

# [formatters]
# keys=sampleFormatter

# [logger_root]
# level=DEBUG
# handlers=consoleHandler

# [logger_sampleLogger]
# level=DEBUG
# handlers=consoleHandler
# qualname=sampleLogger
# propagate=0

# [handler_consoleHandler]
# class=StreamHandler
# level=DEBUG
# formatter=sampleFormatter
# args=(sys.stdout,)

# [formatter_sampleFormatter]
# format=%(asctime)s - %(name)s - %(levelname)s - %(message)s
def init_log_by_config_file(file_name):
    logging.config.fileConfig(
        fname='file.conf', disable_existing_loggers=False)


class LogConfig:

    def __init__(self, logLevel=pylog.DEBUG, logFilePath="", isLogRotate=True,
                 isLogBoth=True):
        self.logLevel = logLevel
        # default log to stdout
        self.logFilePath = logFilePath
        # whether to log simultaneously to both stdout and file
        self.isLogBoth = isLogBoth
        # whether to rotate log file at midnight
        self.isLogRotate = isLogRotate




class MultiprocTimedRotatingFileHandler(pyhandlers.TimedRotatingFileHandler):
    """Multiprocessing aware.
    Only rotate log file on MainProcess, children just reopen"""

    def doRollover(self):
        oldStream = self.stream
        # get the time that this sequence started at and make it a TimeTuple
        currentTime = int(time.time())
        dstNow = time.localtime(currentTime)[-1]
        t = self.rolloverAt - self.interval
        if self.utc:
            timeTuple = time.gmtime(t)
        else:
            timeTuple = time.localtime(t)
            dstThen = timeTuple[-1]
            if dstNow != dstThen:
                if dstNow:
                    addend = 3600
                else:
                    addend = -3600
                timeTuple = time.localtime(t + addend)
        dfn = self.rotation_filename(self.baseFilename + "." +
                                     time.strftime(self.suffix, timeTuple))
        if multiprocessing.current_process().name == "MainProcess":
            os.rename(self.baseFilename, dfn)
        if not self.delay:
            self.stream = self._open()
            if oldStream:
                oldStream.close()
        newRolloverAt = self.computeRollover(currentTime)
        while newRolloverAt <= currentTime:
            newRolloverAt = newRolloverAt + self.interval
        # If DST changes and midnight or weekly rollover, adjust for this.
        if (self.when == 'MIDNIGHT' or self.when.startswith(
                'W')) and not self.utc:
            dstAtRollover = time.localtime(newRolloverAt)[-1]
            if dstNow != dstAtRollover:
                if not dstNow:  # DST kicks in before next rollover, so we need to deduct an hour
                    addend = -3600
                else:  # DST bows out before next rollover, so we need to add an hour
                    addend = 3600
                newRolloverAt += addend
        self.rolloverAt = newRolloverAt


def ApplyOnRootLogger(conf: LogConfig) -> pylog.Logger:
    logger = pylog.getLogger()
    logger.setLevel(conf.logLevel)
    handlers: [pylog.Handler] = []
    stdoutHandle = pylog.StreamHandler(sys.stdout)
    if conf.logFilePath == "":
        handlers = [stdoutHandle]
    else:
        if not conf.isLogRotate:
            fileHandler = pylog.FileHandler(conf.logFilePath)
        else:
            # when = "S"
            when = "MIDNIGHT"
            fileHandler = MultiprocTimedRotatingFileHandler(
                conf.logFilePath, when=when, interval=1)
        if conf.isLogBoth:
            handlers = [fileHandler, stdoutHandle]
        else:
            handlers = [fileHandler]
    for h in handlers:
        h.setFormatter(pylog.Formatter(FORMAT))
    logger.handlers = handlers
    return logger


# logger is the root logger
logger = ApplyOnRootLogger(LogConfig())