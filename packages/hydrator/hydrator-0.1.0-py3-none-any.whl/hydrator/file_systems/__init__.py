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

from hydrator.lib.dynafs import FsClient
from nr.databind.core import UnionType, SerializeAs, Struct
from typing import Optional


@SerializeAs(UnionType())
class FileSystem(Struct):
  """
  Base class for configurable file systems that can be mounted on a #DynaFs instance. Some
  file systems may require authorization, in which they must implement the #login() and
  #logout() method.
  """

  def is_authenticated(self, credentials: Optional[dict]) -> bool:
    """
    Return #True if the user is already authenticated with the file system using the
    specified *credentials*. The credentials are what is returned from #login(). The
    *credentials* may be `None` if #login() was never called. File systems that do not
    require authentication return always `True`.
    """

    raise NotImplementedError

  def login(self) -> dict:
    """
    Authenticate the user. This is only called if #is_authenticated() returns #False.
    Return the credentials in a JSON serializable dictionary. Raise #NotImplementedError
    if the filesystem does not support authentication.
    """

    raise NotImplementedError

  def logout(self, credentials: dict) -> None:
    """
    Revoke the *credentials*. Do not raise an error if the credentials are already revoked.
    """

    raise NotImplementedError

  def get_fs_client(self, credentials: Optional[dict]) -> FsClient:
    """
    Return the #FsClient implementation for this file system.
    """

    raise NotImplementedError


from . import nextcloud
