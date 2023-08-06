# -*- coding: utf-8 -*-
"""CloudFunctions class file."""

import requests
from google.auth.transport.requests import AuthorizedSession


class CloudFunctions(object):
    """CloudFunctions class."""

    def __init__(self, project, region, auth=None, verbose=None):
        """Initialize a CloudFunctions instance."""
        self.project = project
        self.region = region

        self.auth = auth
        self.verbose = verbose

        # create base url for HTTP functions
        self.base_url = 'https://%s-%s.cloudfunctions.net' % (
            self.region,
            self.project,
        )

    def runWorkdayPeopleFeed(self):
        """Get People from Workday API."""
        settings = self.auth.settings
        # get username and password from auth settings
        username = settings['workday']['feed_username']
        password = settings['workday']['feed_password']
        # create url
        url = '%s/runWorkdayPeopleFeed' % (self.base_url)
        # create body
        body = {
            'username': username,
            'password': password,
        }
        # run workday people feed and return response
        if self.verbose:
            print('URL: %s' % (url))
        return requests.post(url, json=body).text

    def tokenInfo(self):
        """Get info for access_token."""
        g = self.auth.google()
        scopes = [
            'https://www.googleapis.com/auth/cloud-platform',
            'https://www.googleapis.com/auth/admin.directory.user',
        ]
        # create credentials
        g.auth_service_account(scopes, g.subject)
        requests = AuthorizedSession(g.credentials)
        # create headers
        headers = {}
        # create url
        url = '%s/tokenInfo' % (self.base_url)
        # check tokenInfo
        if self.verbose:
            print('URL: %s' % (url))
        return requests.get(url, headers=headers).json()
