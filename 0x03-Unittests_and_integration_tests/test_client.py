#!/usr/bin/env python3
"""A module for testing the client.py file
"""
import unittest
from unittest.mock import patch, MagicMock, Mock, PropertyMock
from parameterized import parameterized, parameterized_class
from client import GithubOrgClient

class TestGithubOrgClient(unittest.TestCase):
    """Test cases for the GithubOrgClient class."""

    @parameterized.expand([
        ("google", {'login': 'google', 'repos_url': 'https://api.github.com/users/google/repos'}),
        ("abc", {'login': 'abc', 'repos_url': 'https://api.github.com/users/abc/repos'}),
    ])
    @patch("client.get_json")
    def test_org(self, org, resp, mocked_fxn):
        """Test the org method."""
        mocked_fxn.return_value = resp
        gh_org_client = GithubOrgClient(org)
        self.assertEqual(gh_org_client.org(), resp)
        mocked_fxn.assert_called_once_with("https://api.github.com/orgs/{}".format(org))

    @patch("client.GithubOrgClient.org")
    def test_public_repos_url(self, mock_org):
        """Test the _public_repos_url property."""
        mock_org.return_value = {
            'repos_url': "https://api.github.com/users/google/repos",
        }
        self.assertEqual(
            GithubOrgClient("google")._public_repos_url,
            "https://api.github.com/users/google/repos",
        )

    @patch("client.get_json")
    def test_public_repos(self, mock_get_json):
        """Test the public_repos method."""
        test_payload = [
            {"name": "episodes.dart"},
            {"name": "kratu"},
        ]
        mock_get_json.return_value = test_payload
        with patch("client.GithubOrgClient._public_repos_url", new_callable=PropertyMock) as mock_public_repos_url:
            mock_public_repos_url.return_value = "https://api.github.com/users/google/repos"
            self.assertEqual(GithubOrgClient("google").public_repos(), ["episodes.dart", "kratu"])
            mock_public_repos_url.assert_called_once()
        mock_get_json.assert_called_once()

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
    ])
    def test_has_license(self, repo, key, expected):
        """Test the has_license method."""
        gh_org_client = GithubOrgClient("google")
        client_has_license = gh_org_client.has_license(repo, key)
        self.assertEqual(client_has_license, expected)

@parameterized_class([
    {
        'org_payload': {'login': 'google', 'repos_url': 'https://api.github.com/users/google/repos'},
        'repos_payload': [{"name": "episodes.dart"}, {"name": "kratu"}],
        'expected_repos': ["episodes.dart", "kratu"],
        'apache2_repos': ["episodes.dart"],
    },
])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration tests for the GithubOrgClient class."""

    @classmethod
    def setUpClass(cls):
        """Set up class fixtures before running tests."""
        route_payload = {
            'https://api.github.com/orgs/google': cls.org_payload,
            'https://api.github.com/users/google/repos': cls.repos_payload,
        }

        def get_payload(url):
            if url in route_payload:
                return Mock(**{'json.return_value': route_payload[url]})
            return HTTPError

        cls.get_patcher = patch("requests.get", side_effect=get_payload)
        cls.get_patcher.start()

    def test_public_repos(self):
        """Test the public_repos method."""
        self.assertEqual(
            GithubOrgClient("google").public_repos(),
            self.expected_repos,
        )

    def test_public_repos_with_license(self):
        """Test the public_repos method with a license."""
        self.assertEqual(
            GithubOrgClient("google").public_repos(license="apache-2.0"),
            self.apache2_repos,
        )

    @classmethod
    def tearDownClass(cls):
        """Remove the class fixtures after running all tests."""
        cls.get_patcher.stop()
