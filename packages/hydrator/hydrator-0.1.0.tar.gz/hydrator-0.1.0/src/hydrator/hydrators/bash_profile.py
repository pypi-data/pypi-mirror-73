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
from nr.databind.core import Field, FieldName, Struct, UnionType
from typing import BinaryIO, Iterable
import enum
import io
import os

#: This snippet of Bash code is rendered into the RC file to ensure that an
#: SSH agent is running the environment is initialized for that agent.
SSH_AGENT_SNIPPET = '''
# -------------------------
# $.builtins.ssh-agent = on
# -------------------------
if [ -d "$HOME/.ssh" ] && [[ $- == *i* ]]; then
  SSH_ENV="$HOME/.ssh/environment"
  function _start_ssh_agent {
    >&2 echo ".profile: Initialising new SSH agent..."
    ssh-agent | sed 's/^echo/#echo/' > "${SSH_ENV}"
    chmod 600 "${SSH_ENV}"
    . "${SSH_ENV}" > /dev/null
    ssh-add;
  }
  # Source SSH settings, if applicable
  if [ -f "${SSH_ENV}" ]; then
    . "${SSH_ENV}" > /dev/null
    #ps ${SSH_AGENT_PID} doesn't work under cywgin
    ps -ef | grep ${SSH_AGENT_PID} | grep ssh-agent > /dev/null || {
        _start_ssh_agent;
    }
  else
    _start_ssh_agent;
  fi
elif [[ $- != *i* ]]; then
  >&2 echo "note: Not a login shell. Skipping ssh-agent"
else
  >&2 echo "note: $HOME/.ssh does'nt exist. Skipping ssh-agent"
fi
'''

#: This bash snippet is rendered if #Builtins.venv_function is enabled.
VENV_SNIPPET = '''
# -----------------------------
# $.builtins.venv-function = on
# -----------------------------
function venv() {
  local COMMAND="$1"; shift
  local ENVNAME="$1"; shift
  local PYTHON="${PYTHON:-python3}"
  local ENVPATH=~/.local/venvs/"$ENVNAME"
  if [[ $ENVNAME == /* ]] || [[ $ENVNAME == ./* ]]; then
    ENVPATH="$ENVNAME"
  fi
  case "$COMMAND" in
    create)
      "$PYTHON" -m venv "$ENVPATH"
      venv python "$ENVNAME" -m pip install wheel
      venv activate "$ENVNAME"
      return $?
      ;;
    rm)
      if [ ! -d "$ENVPATH" ]; then
        >&2 echo "error: $ENVPATH does not exist"
        return 1
      else
        rm -rf "$ENVPATH"
        echo "$ENVPATH removed"
      fi
      ;;
    ls)
      ls -1a ~/.local/venvs | grep -v '^\.$' | grep -v '^\.\.$'
      ;;
    activate)
      source "$ENVPATH/bin/activate"
      ;;
    python)
      "$ENVPATH/bin/python" "$@"
      return $?
      ;;
    *)
      >&2 echo "usage: venv {create,activate,python}"
      >&2 echo "error: unexpected command \"$1\""
      return 1
      ;;
  esac
}
'''

#: This bash snippet is rendered if #Builtins.ggp_tty_variable is enabled.
GPG_TTY_SNIPPET = '''
# --------------------------------
# $.builtins.gpg-tty-variable = on
# --------------------------------
export GPG_TTY=$(tty)
'''

#: This bash snippet is rendered if #Builtins.ggp_tty_variable is enabled.
LOCAL_BIN_SNIPPET = '''
# -------------------------
# $.builtins.local-bin = on
# -------------------------
export PATH="$PATH:~/.local/bin"
'''


class Shell(enum.Enum):
  BASH = 0


class Builtins(Struct):
  #: Render code into the shell script that ensures that an SSH agent is active
  #: and the environment variables are set in the current shell.
  ssh_agent = Field(bool, FieldName('ssh-agent'), default=False)

  #: Render a `venv` function into the bash profile that can be used to manage
  #: virtual environment in ~/.local/venvs`.
  venv_function = Field(bool, FieldName('venv-function'), default=False)

  #: Sets the `GPG_TTY` environment variable. This is needed in WSL and enabled by default.
  ggp_tty_variable = Field(bool, FieldName('gpg-tty-variable'), default=True)

  #: Adds `~/.local/bin` to the `PATH` environment variable. Enabled by default.
  local_bin = Field(bool, FieldName('local-bin'), default=True)


@UnionType.extend(Hydrator, 'bash_profile')
class BashProfile(Hydrator):
  """
  Renders a `~/.bash_profile` file into your home directory from a YAML configuration.
  """

  shell = Field(Shell, default=Shell.BASH)

  #: A mapping for shell aliases.
  aliases = Field(dict(value_type=str), default=dict)

  #: A mapping that allows you to turn certain built-in feature on an off.
  #: See the #Builtins documentation for more information.
  builtins = Field(Builtins, default=Field.DEFAULT_CONSTRUCT)

  #: A mapping of environment variables to set unconditionally.
  environment = Field(dict(value_type=str), default=dict)

  #: A list of paths to add to the #PATH environment variable.
  path = Field([str], default=list)

  #: A mapping of code blocks to render into the profile. Leveraging the
  #: configuration preprocessing that dotconfig employs, blocks can be
  #: inherited, overwritten or excluded from a base configuration.
  blocks = Field(dict(value_type=str), default=dict)

  #: The encoding for the generated file. Defaults to `utf-8`.
  encoding = Field(str, default='utf-8')

  # Hydrator Overrides

  def execute(self, context: Context) -> None:
    filename = os.path.expanduser('~/.bash_profile')
    print('render "{}"'.format(filename))
    if context.dry:
      return
    with open(filename, 'w') as fp:
      for key, value in self.environment.items():
        fp.write('export {}="{}"\n'.format(key, value))
      if self.path:
        fp.write('export PATH="$PATH:{}"\n'.format(':'.join(self.path)))
      fp.write('\n')
      for key, value in self.aliases.items():
        fp.write('alias {}="{}"\n'.format(key, value))
      fp.write('\n')
      for value in self.blocks.values():
        fp.write(value)
        fp.write('\n')
      if self.builtins.ssh_agent:
        fp.write(SSH_AGENT_SNIPPET)
      if self.builtins.venv_function:
        fp.write(VENV_SNIPPET)
      if self.builtins.ggp_tty_variable:
        fp.write(GPG_TTY_SNIPPET)
      if self.builtins.local_bin:
        fp.write(LOCAL_BIN_SNIPPET)
