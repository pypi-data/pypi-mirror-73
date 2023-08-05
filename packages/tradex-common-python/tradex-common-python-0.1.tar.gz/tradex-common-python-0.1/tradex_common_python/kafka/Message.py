from enum import Enum
from typing import Dict, Any


class MessageType(Enum):
    MESSAGE: str = 'MESSAGE'
    REQUEST: str = 'REQUEST'
    RESPONSE: str = 'RESPONSE'


class ResponseDestination:
    __slots__ = 'topic', 'uri'

    def __init__(self, topic: str, uri: str):
        self.topic: str = topic
        self.uri: str = uri

    def to_dict(self):
        return {
            'topic': self.topic,
            'uri': self.uri
        }


class Message:
    __slots__ = 'messageType', 'sourceId', 'messageId', 'transactionId', 'uri', 'responseDestination', 'data', 't'

    def __init__(self, messageType: str, sourceId: str, messageId: str, transactionId: str, uri: str,
                 responseDestination: str, data):
        self.messageType: str = messageType
        self.sourceId: str = sourceId
        self.messageId: str = messageId
        self.transactionId: str = transactionId
        self.uri: str = uri
        self.t: int = None
        self.responseDestination: ResponseDestination = responseDestination
        self.data: Any = data

    def to_dict(self):
        return {
            'messageType': self.messageType,
            'sourceId': self.sourceId,
            'messageId': self.messageId,
            'transactionId': self.transactionId,
            'uri': self.uri,
            'responseDestination': None if self.responseDestination is None else self.responseDestination.to_dict(),
            'data': self.data
        }


def create_from_dict(dict: Dict) -> Message:
    res_dict = dict.get('responseDestination')
    response: ResponseDestination = None if res_dict is None else ResponseDestination(res_dict.get('topic'),
                                                                                      res_dict.get('uri'))
    return Message(dict.get('messageType'), dict.get('sourceId'), dict.get('messageId'), dict.get('transactionId'),
                   dict.get('uri'), response, dict.get('data'))
