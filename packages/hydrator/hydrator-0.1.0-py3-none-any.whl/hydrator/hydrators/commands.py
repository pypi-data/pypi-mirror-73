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

from collections import namedtuple
from contextlib import ExitStack
from hydrator.lib.dynafs import DynaFs
from hydrator.hydrators import Context, Hydrator
from nr.databind.core import Field, Struct, UnionType, make_struct
from typing import Dict, List
from shutil import copyfileobj
import logging
import nr.fs
import os
import posixpath
import shlex
import subprocess

logger = logging.getLogger(__name__)
PreparedCommand = namedtuple('PreparedCommand', 'original,arglist,substitute_map')


def expand_matrix(string: str) -> List[str]:
  """
  Expands a string that contains matrix elements into a list of its elements. A matrix
  element is enclosed in curly braces and separates values by commas. Example: `a{b,c}`
  represents the strings `ab` and `ac`.
  """

  start_index = string.find('{')
  if start_index < 0:
    return [string]
  end_index = string.find('}', start_index)
  if end_index < 0:
    return [string]

  prefix = string[:start_index]
  values = string[start_index+1:end_index].split(',')
  result = []
  for value in values:
    element = prefix + value
    for suffix in expand_matrix(string[end_index+1:]):
      result.append(element + suffix)

  return result


def prepare_command(command: str) -> PreparedCommand:
  arglist: List[str] = []
  substitute_map: Dict[int, List[str]] = {}
  for arg in shlex.split(command):
    if arg.startswith('[[') and arg.endswith(']]'):
      arg = arg[2:-2].strip()
      substitute_map[len(arglist)] = expand_matrix(arg)
      arglist.append('<subst:{}>'.format(len(arglist)))
    else:
      arglist.append(arg)
  return PreparedCommand(command, arglist, substitute_map)


@UnionType.extend(Hydrator, 'commands')
class Commands(Hydrator):
  """
  This Hydrator allows you to run arbitrary shell commands, while taking files from the
  configured file systems as inputs.

  Example:

  ```yml
  type: commands
  commands:
  - gpg --import [[nextcloud://path/to/master.key]]
  ``

  The argument enclosed in `[[...]]`` will be replaced with the location of the temporary
  file that will be created after downloading it from the `nextcloud://` filesystem (as
  configured in the ``file-systems.yml`` configuraton file).

  Note that it also supports argument matrices in a bash-like fastion. For example,
  `[[nextcloud:://ida_rsa{,pub}]]` actually refers to two files and will expand into two
  arguments.
  ```
  """

  #: A list of shell commands that will be executed by this Hydrator. Arguments that are
  #: enclosed in double brackets (i.e. [[argvalue]]) are treated as files that will be
  #: read from the configured file systems into a temporary location.
  commands = Field([str])

  #: Environment variables for the commands.
  environment = Field(dict(value_type=str), default=dict)

  # Hydrator Overrides

  def execute(self, context: Context) -> None:
    commands: List[PreparedCommand] = list(map(prepare_command, self.commands))
    for command in commands:
      print('$', command.original)
      arglist = command.arglist[:]
      with ExitStack() as stack:
        for index, values in command.substitute_map.items():
          local_files = []
          for source_file in values:
            tmpdir = stack.enter_context(nr.fs.tempdir())
            with open(os.path.join(tmpdir.name, posixpath.basename(source_file)), 'wb') as fp:
              logger.info('Downloading "%s" to "%s"', source_file, fp.name)
              copyfileobj(context.fs.open(source_file, 'rb'), fp)
              local_files.append(fp.name)
          arglist[index] = local_files
        arglist = [y for x in arglist for y in ([x] if isinstance(x, str) else x)]

        def _quote(x):
          if ' ' in x:
            return '"{}"'.format(x)
          return x

        shell = os.getenv('SHELL', 'bash')
        command = [shell, '-c', ' '.join(map(_quote, arglist))]
        logger.info('Executing command %s (dry: %s)', command, context.dry)
        if context.dry:
          continue

        subprocess.check_call(command)
