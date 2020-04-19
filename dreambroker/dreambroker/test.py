import unittest
import requests
import json


class TestAPI(unittest.TestCase):
    url = 'http://127.0.0.1:8000/analyze'
    header = {'content-type': 'application/json'}

    def testBaseCase(self):
        data = json.dumps({"text": "hello 2 times  "})
        response = requests.post(self.url, data=data, headers=self.header)
        expected = {
            "textLength": {"withSpaces": 15, "withoutSpaces": 11},
            "wordCount": 3,
            "characterCount": [{"e": 2}, {"h": 1}, {"i": 1}, {"l": 2}, {"m": 1}, {"o": 1}, {"s": 1}, {"t": 1}]
        }
        self.assertEqual(json.loads(response.text), expected)

    def testLeadingInteger(self):
        data = json.dumps({"text": "2 hello times  "})
        response = requests.post(self.url, data=data, headers=self.header)
        expected = {
            "textLength": {"withSpaces": 15, "withoutSpaces": 11},
            "wordCount": 3,
            "characterCount": [{"e": 2}, {"h": 1}, {"i": 1}, {"l": 2}, {"m": 1}, {"o": 1}, {"s": 1}, {"t": 1}]
        }
        self.assertEqual(json.loads(response.text), expected)

    def testNonEnglishChars(self):
        data = json.dumps({"text": "255   hello times åösd "})
        response = requests.post(self.url, data=data, headers=self.header)
        expected = {
            "textLength": {"withSpaces": 23, "withoutSpaces": 17},
            "wordCount": 4,
            "characterCount": [{"d": 1}, {"e": 2}, {"h": 1}, {"i": 1}, {"l": 2}, {"m": 1}, {"o": 1}, {"s": 2}, {"t": 1}]
        }
        self.assertEqual(json.loads(response.text), expected)

    def testEmpty(self):
        data = json.dumps({"text": ""})
        response = requests.post(self.url, data=data, headers=self.header)
        expected = {
            "textLength": {"withSpaces": 0, "withoutSpaces": 0},
            "wordCount": 0,
            "characterCount": []
        }
        self.assertEqual(json.loads(response.text), expected)

    def testWhitespaceChars(self):
        data = json.dumps({"text": "\n abc \t"})
        response = requests.post(self.url, data=data, headers=self.header)
        expected = {
            "textLength": {"withSpaces": 7, "withoutSpaces": 3},
            "wordCount": 1,
            "characterCount": [{'a': 1}, {'b': 1}, {'c': 1}]
        }
        self.assertEqual(json.loads(response.text), expected)
