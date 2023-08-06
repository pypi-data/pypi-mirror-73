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

from nr.fs import issub as issubpath
from nr.interface import Interface
from typing import List, IO
from urllib.parse import urlsplit
import os
import posixpath


class FsClient(Interface):

  def open(self, path: str, mode: str) -> IO:
    """
    Open the file at *path*. Raise #FileNotFoundError if the file does not exist. May
    raise #NotImplementedError if the *mode* is not supported.
    """

    pass


class LocalFsClient(FsClient):
  """
  An #FsClient implementation for the local filesystem.

  # Arguments
  directory: The directory where relative paths are resolved from.
  isolated: If enabled, access outside of the directory is denied.
  """

  def __init__(self, directory: str = None, isolated: bool = True) -> None:
    self.directory = directory
    self.isolated = isolated

  def open(self, path: str, mode: str) -> IO:
    path = os.path.normpath(os.path.join(self.directory, path)), self.directory
    if self.isolated:
      try:
        path = os.path.relpath(path, self.directory)
      except ValueError:
        # On a different drive (windows)?
        raise FileNotFoundError(path)
      if not issubpath(path):
        raise FileNotFoundError(path)
    return open(path, mode)


class DynaFs:

  def __init__(self):
    self._handlers = {}

  def mount_protocol(self, protocol: str, fs_client: FsClient) -> None:
    self._handlers[protocol] = fs_client

  def open(self, url: str, mode: str) -> IO:
    parsed = urlsplit(url)
    if not parsed.scheme:
      raise ValueError('URL requires a protocol: {!r}'.format(url))
    if parsed.scheme not in self._handlers:
      raise ValueError('no handler registered for protocol {!r}: {!r}'.format(parsed.schema, url))
    full_path = posixpath.join(parsed.netloc, parsed.path.lstrip('/'))
    return self._handlers[parsed.scheme].open(full_path, mode)
