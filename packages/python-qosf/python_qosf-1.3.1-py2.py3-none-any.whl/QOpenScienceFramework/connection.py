# -*- coding: utf-8 -*-
"""
This module handles the OAuth2 authentication process and maintains the
session (/token) information that is required to communicate with the OSF API

It is also responsible for constructing the correct API calls/uris as specified by the
OSF for the various types of information that can be requested.

.. Note:: A lot of the functions that are available here have equivalents in the
	ConnectionManager class. It is recommended to use those functions instead as they are
	executed asynchronously and are used throughout the rest of the application.
"""

# Python3 compatibility
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from QOpenScienceFramework.compat import *
from QOpenScienceFramework import dirname

# Import basics
import os
import time
import logging
import json

# Module for easy OAuth2 usage, based on the requests library,
# which is the easiest way to perform HTTP requests.

# OAuth2Session
import requests_oauthlib
# Mobile application client that does not need a client_secret
from oauthlib.oauth2 import MobileApplicationClient
# Easier function decorating
from functools import wraps


# Load settings file containing required OAuth2 parameters
with open(os.path.join(dirname, 'settings.json')) as fp:
    settings = json.load(fp)
base_url = settings['base_url']
api_base_url = settings['api_base_url']
scope = settings['scope']
website_url = settings['website_url']

# Convenience reference
TokenExpiredError = requests_oauthlib.oauth2_session.TokenExpiredError


class OSFInvalidResponse(Exception):
    pass


session = None


def create_session():
    """ Creates/resets and OAuth 2 session, with the specified data. """
    global session
    global settings

    try:
        client_id = settings['client_id']
        redirect_uri = settings['redirect_uri']
    except KeyError as e:
        raise KeyError("The OAuth2 settings dictionary is missing the {} entry. "
                       "Please add it to the QOpenScienceFramework.connection.settings "
                       "dicationary before trying to create a new session".format(e))

    # Set up requests_oauthlib object
    mobile_app_client = MobileApplicationClient(client_id)

    # Create an OAuth2 session for the OSF
    session = requests_oauthlib.OAuth2Session(
        client_id,
        mobile_app_client,
        scope=scope,
        redirect_uri=redirect_uri,
    )
    return session


# Generate correct URLs
auth_url = base_url + "oauth2/authorize"
token_url = base_url + "oauth2/token"
logout_url = base_url + "oauth2/revoke"

# API configuration settings
api_calls = {
    "logged_in_user": "users/me/",
    "projects": "users/me/nodes/",
    "project_repos": "nodes/{}/files/",
    "repo_files": "nodes/{}/files/{}/",
    "file_info": "files/{}/",
}


def api_call(command, *args):
    """ generates and api endpoint. If arguments are required to build the endpoint
    , they can be specified as extra arguments.

    Parameters
    ----------
    command : {'logged_in_user', 'projects', 'project_repos', 'repo_files', 'file_info'}
            The key of the endpoint to look up in the api_calls dictionary

            Extra arguments passed to this function will be integrated into the API call
            at specified positions (marked by \{\}). The formats of the calls are as follows:

                    ``logged_in_user: "users/me/"``

                    ``projects: "users/me/nodes/"``

                    ``project_repos: "nodes/{}/files/"``

                    ``repo_files: "nodes/{}/files/{}/"``

                    ``file_info: "files/{}/"``

    *args : various (optional)
            Optional extra data which is needed to construct the correct api endpoint uri.
            Check the OSF API documentation for a list of variables that each type of
            call expects.

    Returns
    -------
    string : The complete uri for the api endpoint.
    """

    return api_base_url + api_calls[command].format(*args)


def check_for_active_session():
    """ Checks if a session object has been created and raises a RuntimeError otherwise."""
    if session is None:
        raise RuntimeError("Session is not yet initialized, use connection."
                           "session = connection.create_session()")


# %--------------------------- Oauth communiucation ----------------------------

def get_authorization_url():
    """ Generate the URL at which an OAuth2 token for the OSF can be requested
    with which OpenSesame can be allowed access to the user's account.

    Returns
    -------
    str
        The complete uri for the api endpoint.

    Raises
    ------
    RuntimeError
            When there is no active OAuth2 session.
    """
    check_for_active_session()
    return session.authorization_url(auth_url)


def parse_token_from_url(url):
    """ Parses token from url fragment

    Parameters
    ----------
    url : str
        The url to parse. Should have a hass fragment (#) after which the token
        information is found.

    Returns
    -------
    str
        The currently used OAuth2 access token.

    Raises
    ------
    RuntimeError
        When there is no active OAuth2 session.
    """
    check_for_active_session()
    token = session.token_from_fragment(url)
    # Call logged_in function to notify event listeners that user is logged in
    if is_authorized():
        return token
    else:
        logging.debug("ERROR: Token received, but user not authorized")


def is_authorized():
    """ Convenience function simply returning OAuth2Session.authorized.

    Returns
    -------
    bool
        True is the user is authorized, False if not
    """
    check_for_active_session()
    return session.authorized


def token_valid():
    """ Checks if OAuth token is present, and if so, if it has not expired yet.

    Returns
    -------
    bool
        True if the token is present and is valid, False otherwise

    """
    check_for_active_session()
    if not hasattr(session, "token") or not session.token:
        return False
    return session.token["expires_at"] > time.time()
