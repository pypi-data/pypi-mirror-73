import unittest
from .Request import Request

class TestRequest(unittest.TestCase):
    def test_upper(self):
        a = Request().from_dict({
            'headers': {
                'token': {
                    'userId': 10,
                },
                'accept-language': 'en',
            },
            'sourceIp': '10',
            'deviceType': 'ajhgdf'

        })
        self.assertEqual(a.headers.token.userId, 10)