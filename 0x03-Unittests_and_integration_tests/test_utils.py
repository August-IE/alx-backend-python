#!/usr/bin/env python3
'''A module that parameterize a unit test
Mock HTTP calls, Parameterize and patch
'''

import unittest
from parameterized import parameterized
from unittest.mock import patch, Mock
from utils import access_nested_map, memoize, get_json


class TestAccessNestedMap(unittest.TestCase):
    '''Test case for `utils.access_nested_map` function.
    '''

    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2),
    ])
    def test_access_nested_map(
            self,
            nested_map,
            path,
            expected
            ):
        '''Tests `access_nexted_map`'s output
        '''
        self.assertEqual(access_nested_map(nested_map, path), expected)

    @parameterized.expand([
        ({}, ("a",), KeyError),
        ({"a": 1}, ("a", "b"), KeyError),
    ])
    def test_access_nested_map_exception(
            self,
            nested_map,
            path,
            exception,
            ):
        '''Tests `access_nested_map`'s exception raising.
        '''
        with self.assertRaises(exception):
            access_nested_map(nested_map, path)


class TestGetJson(unittest.TestCase):
    '''Tests the `utils.get_json` function returns the expected result.
    '''

    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False}),
    ])
    def test_get_json(
            self,
            test_url,
            test_payload,
            ):
        '''Tests `get_json`'s output.
        '''

        attrs = {'json.return_value': test_payload}

        with patch("requests.get", return_value=Mock(**attrs)) as req_get:
            result = get_json(test_url)
            self.assertEqual(result, test_payload)
            req_get.assert_called_once_with(test_url)


class TestMemoize(unittest.TestCase):
    """Tests the `memoize` function with given params."""
    def test_memoize(self):
        """Tests `memoize`'s output."""
        class TestClass:
            def a_method(self):
                return 42

            @memoize
            def a_property(self):
                return self.a_method()

        test_class = TestClass()

        with patch.object(test_class, "a_method", return_value=42) as memo_fxn:
            self.assertEqual(test_class.a_property, 42)
            self.assertEqual(test_class.a_property, 42)
            memo_fxn.assert_called_once()
