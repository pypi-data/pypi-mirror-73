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
from hydrator.hydrators import Context, Hydrator
from nr.databind.core import Field, FieldName, Remainder, UnionType
import os


@UnionType.extend(Hydrator, 'gitconfig')
class GitConfig(Hydrator):
  """
  Renders a Git configuration from a YAML representation of the same. Leveraging
  the configuration preprocessing that dotconfig employs, sections of the Git
  configuration can be inherited, overwritten or excluded from a base configuration.
  """

  #: A mapping of a mapping to string values. This translates directly to the
  #: INI-style Git configuration format.
  fields = Field(dict(value_type=dict(value_type=str)), Remainder())

  #: The encoding for the generated file. Defaults to `utf-8`.
  encoding = Field(str, default='utf-8')

  # Hydrator Overrides

  def execute(self, context: Context) -> None:
    filename = os.path.expanduser('~/.gitconfig')
    print('rendering "{}"'.format(filename))
    if context.dry:
      return
    with open(filename, 'w') as fp:
      for section, values in self.fields.items():
        fp.write('[{}]\n'.format(section))
        for key, value in values.items():
          fp.write('  {} = "{}"\n'.format(key, value))
