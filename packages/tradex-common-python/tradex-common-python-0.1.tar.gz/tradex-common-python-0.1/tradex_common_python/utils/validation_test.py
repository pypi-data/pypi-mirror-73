import unittest
from .validation import validate, create_fail_validation
from ..errors.InvalidParameterError import InvalidParameterError


class TestValidation(unittest.TestCase):
    def test_require(self):
        try:
            validate("", "name").set_require().throw_valid(InvalidParameterError())
            self.assertFalse(True)
        except Exception as err:
            self.assertIsInstance(err, InvalidParameterError)

    def test_check(self):
        try:
            validate("jhgjgj", "name").set_require().add(invalid_format).throw_valid(InvalidParameterError())
            self.assertFalse(True)
        except Exception as err:
            self.assertIsInstance(err, InvalidParameterError)
            self.assertEqual(err.params[0].code, "FAIL")

    def test_pass(self):
        try:
            validate("jhgjgj", "name").set_require().throw_valid(InvalidParameterError())
            self.assertFalse(False)
        except Exception as err:
            self.assertFalse(True)

    # def test_pass_w_on_success(self):
    #     try:
    #         d = 20
    #         validate("jhgjgj", "name").set_require().set_success(lambda last_res, reses: d = 21).throw_valid(InvalidParameterError())
    #         self.assertEqual(d, 21)
    #     except Exception as err:
    #         self.assertFalse(True)


def invalid_format(value: str, name: str):
    return create_fail_validation("FAIL", [], name)
