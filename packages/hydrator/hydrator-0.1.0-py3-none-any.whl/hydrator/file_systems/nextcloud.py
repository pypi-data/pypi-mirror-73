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

from . import FileSystem
from hydrator.lib.dynafs import FsClient
from hydrator.lib.nextcloud import Credentials, NextcloudClient
from nr.databind.core import Field, FieldName, Struct, UnionType
from nr.interface import implements, override
from typing import IO, Optional
import io
import logging
import sys

logger = logging.getLogger(__name__)


@UnionType.extend(FileSystem, 'nextcloud')
class Nextcloud(FileSystem):
  """
  Provides a file system to access files in Nextcloud over it's REST API. The Nextcloud Login
  Flow v2 will be used if the user is not currently authenticated.
  """

  server_url = Field(str, FieldName('server-url'))

  # FileSystem Overrides

  def is_authenticated(self, credentials: Optional[dict]) -> bool:
    if credentials:
      client = NextcloudClient(self.server_url, Credentials(**credentials))
      return client.is_authenticated()
    return False

  def login(self) -> dict:
    client = NextcloudClient(self.server_url)
    return dict(client.login()._asdict())

  def logout(self, credentials: dict) -> None:
    logger.warning('Nextcloud does not support logout through the API, '
                   'you may want to manually revoke the app password.')
    #client = NextcloudClient(self.server_url, Credentials(**credentials))
    #client.logout()

  def get_fs_client(self, credentials: Optional[dict]):
    creds = Credentials(**credentials) if credentials else None
    return NextcloudFsClient(NextcloudClient(self.server_url, creds))


@implements(FsClient)
class NextcloudFsClient:
  """
  Implements the #FsClient interface for a Nextcloud server.
  """

  def __init__(self, client: NextcloudClient) -> None:
    self.client = client

  @override
  def open(self, path: str, mode: str) -> IO:
    if 'w' in mode:
      raise NotImplementedError('NextcloudFsClient does not support writing')
    response = self.client.get_file(path, stream=True)
    if 'b' not in mode:
      encoding = response.headers.get('Content-Encoding') or sys.getdefaultencoding()
      return io.TextIOWrapper(response.raw, encoding=encoding)
    return response.raw
