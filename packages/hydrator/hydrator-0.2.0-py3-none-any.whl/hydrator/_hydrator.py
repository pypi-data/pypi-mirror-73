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

from hydrator.lib.dynafs import DynaFs, LocalFsClient
from hydrator.file_systems import FileSystem
from hydrator.hydrators import Hydrator as _Hydrator
from nr.config.transform import Substitution, Transformer
from nr.config.util import merge_dicts
from nr.databind.core import Field, FieldName, ObjectMapper, Remainder, Struct
from nr.databind.json import JsonModule
from typing import Optional, Union, TextIO
import logging
import os
import yaml

logger = logging.getLogger(__name__)


def _merge_configs(a: dict, b: dict) -> dict:
  tf = Transformer(Substitution().with_vars(a, relative=True))
  return tf(merge_dicts(a, b))


class ExtensibleConfig(Struct):
  """
  Represents a YAML configuration that can declare itself extending another YAML file.
  The files will be merged using the #nr.config module, which will merge mappings and
  provide special syntax for accessing contextual data.
  """

  extends = Field(str, default=None)
  data = Field(dict, Remainder())

  def render_config(self, mapper: ObjectMapper) -> dict:
    if self.extends:
      base = self.load(self.extends)
      return _merge_configs(base.render_config(mapper), self.data)
    return self.data

  @classmethod
  def load(
    cls,
    file_: Union[str, TextIO],
    filename: str = None,
    mapper: ObjectMapper = None,
  ) -> 'ExtensibleConfig':
    if isinstance(file_, str):
      with open(file_) as fp:
        return cls.load(fp)
    filename = filename or getattr(file_, 'name', None)
    mapper = mapper or ObjectMapper(JsonModule())
    return mapper.deserialize(yaml.safe_load(file_), cls, filename=filename)


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
    fs.mount_protocol('file', LocalFsClient(os.getcwd()))
    for protocol, impl in self.filesystems.items():
      fs.mount_protocol(protocol, impl.get_fs_client(self.credentials.load(protocol)))
    return fs

  @classmethod
  def load(cls, filename: str, mapper: ObjectMapper = None) -> 'Hydrator':
    mapper = mapper or ObjectMapper(JsonModule())
    config = ExtensibleConfig.load(filename, mapper=mapper)
    data = config.render_config(mapper)
    with open(filename) as fp:
      return mapper.deserialize(data, cls, filename=filename)
