#!/usr/bin/env python3
'''A module that parameterize a unit test
'''

import unittest
from parameterized import parameterized
from unittest.mock import patch
from utils import access_nested_map


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
