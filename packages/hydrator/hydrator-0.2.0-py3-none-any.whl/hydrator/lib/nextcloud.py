# -*- coding: utf-8 -*-
# The MIT License (MIT)
#
# Copyright (c) 2020 Niklas Rosenstein
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""
Implements the Nextcloud login flow.
"""

import collections
import requests
import time
import webbrowser
import sys
from urllib.parse import quote as urlquote
from typing import Any, Callable

Credentials = collections.namedtuple('Credentials', 'username,password')
OpenURLType = Callable[[str], bool]


class Timeout(Exception):
  pass


def prompt_open_url(url: str):
  print(file=sys.stderr)
  print('Please visit the below URL to authenticate with Nextcloud.', file=sys.stderr)
  print(file=sys.stderr)
  print('  ' + url, file=sys.stderr)
  print(file=sys.stderr)


class NextcloudClient:

  def __init__(self, server_url: str, credentials: Credentials = None):
    self.server_url = server_url.rstrip('/')
    self.credentials = credentials

  def request(self, *args, check=True, **kwargs):
    response = requests.request(*args, auth=self.credentials, **kwargs)
    if check:
      response.raise_for_status()
    return response

  def login(
    self,
    open_url: OpenURLType = None,
    open_url_fallback: OpenURLType = None,
    timeout: float = None,
    poll_interval: float = 0.5,
    user_agent: str = None,
  ) -> Credentials:
    """
    Users the Nextcloud Login flow v2 to authenticate with the Nextcloud server.

    # Arguments
    open_url: A function that will be called to open the browser. If not specified,
      it will use #webbrowser.open() or use #open_url_fallback if that failed.
    open_url_fallback: The fallback to use if #webbrowser.open() returned `False`.
      The default fallback is #prompt_open_url().
    timeout: The maximum number of seconds to poll for the successful authentication
      of the user with the session token. If set to `None` it will poll forever until
      successfully authenticated.
    poll_intervall: The number of seconds to sleep between polls.

    # Raises
    Timeout: If the login timed out.

    # Returns
    Credentials: The Nextcloud login credentials.
    """

    if open_url_fallback is None:
      open_url_fallback = prompt_open_url

    headers = {}
    if user_agent:
      headers['User-agent'] = user_agent

    response = requests.post(self.server_url.rstrip('/') + '/index.php/login/v2', headers=headers)
    response.raise_for_status()
    login_data = response.json()

    if open_url:
      open_url(login_data['login'])
    else:
      opened_browser = webbrowser.open(login_data['login'])
      if not opened_browser:
        open_url_fallback(login_data['login'])

    start_time = time.perf_counter()
    while True:
      time.sleep(poll_interval)

      if timeout is not None and time.perf_counter() - start_time >= timeout:
        raise Timeout('User did not authenticate within the timeout (= {} seconds)'.format(timeout))

      response = requests.post(login_data['poll']['endpoint'],
        data={'token': login_data['poll']['token']}, headers=headers)
      if response.status_code == 404:
        continue

      if response.status_code == 200:
        data = response.json()
        self.credentials = Credentials(data['loginName'], data['appPassword'])
        return self.credentials

      response.raise_for_status()

    assert False, "This code should not be reached."

  def is_authenticated(self) -> bool:
    if not self.credentials:
      return False
    # TODO (@NiklasRosenstein): Is there a better URL to check for the authentication status?
    response = self.request('HEAD', self.server_url + '/settings/user/security', check=False)
    if response.status_code == 401:
      return False
    if response.status_code == 200:
      return True
    response.raise_for_status()
    raise RuntimeError('unexpected response status code: {}'.format(response.status_code))

  def get_file(self, file_path: str, stream: bool = True) -> requests.Response:
    """
    Gets a file under *file_path* from the Nextcloud instance.
    """

    url = self.server_url + '/remote.php/webdav/' + urlquote(file_path)
    return self.request('GET', url, stream=stream)
