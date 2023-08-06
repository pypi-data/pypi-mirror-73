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

from hydrator.lib.dynafs import DynaFs
from hydrator.file_systems import FileSystem
from hydrator.hydrators import Hydrator as _Hydrator
from nr.databind.core import Field, FieldName, ObjectMapper, Struct
from nr.databind.json import JsonModule
from typing import Optional
import logging
import os
import yaml

logger = logging.getLogger(__name__)


class CredentialStore(Struct):
  filename = Field(str, default='~/.local/hydrator/credentials.yml')

  def _load(self) -> dict:
    filename = os.path.expanduser(self.filename)
    if os.path.isfile(filename):
      with open(filename) as fp:
        try:
          return yaml.safe_load(fp)
        except yaml.YAMLError:
          logger.exception('Unable to load JSON credentials file "%s"', filename)
    return {}

  def _save(self, data: dict) -> None:
    filename = os.path.expanduser(self.filename)
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    yaml_repr = yaml.safe_dump(data)
    with open(filename, 'w') as fp:
      fp.write(yaml_repr)

  def load(self, filesystem: str) -> [dict]:
    return self._load().get(filesystem)

  def save(self, filesystem: str, creds: dict) -> None:
    data = self._load()
    data[filesystem] = creds
    self._save(data)

  def delete(self, filesystem: str) -> bool:
    data = self._load()
    if filesystem in data:
      del data[filesystem]
      self._save(data)
      return True
    return False


class Hydrator(Struct):
  """
  Represents a Hydrator configuration.
  """

  credentials = Field(CredentialStore, default=Field.DEFAULT_CONSTRUCT)
  filesystems = Field(dict(value_type=FileSystem), default=dict)
  hydrators = Field(dict(value_type=_Hydrator))

  def init_dyna_fs(self) -> DynaFs:
    """
    Initializes a #DynaFs instance from the configured #filesystems.
    """

    fs = DynaFs()
    for protocol, impl in self.filesystems.items():
      fs.mount_protocol(protocol, impl.get_fs_client(self.credentials.load(protocol)))
    return fs

  @classmethod
  def load(cls, filename: str, mapper: ObjectMapper = None) -> 'Hydrator':
    mapper = mapper or ObjectMapper(JsonModule())
    with open(filename) as fp:
      return mapper.deserialize(yaml.safe_load(fp), cls, filename=filename)
