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

from hydrator import Context, Hydrator
from nr.proxy import Proxy
import click
import logging
import os
import sys

config = Proxy(lambda: click.get_current_context().obj['config'])
logger = logging.getLogger(__name__)


@click.group(invoke_without_command=True)
@click.option('-c', '--config', metavar='path', help='The config file to load. Defaults to "hydrator.yml"')
@click.option('-v', '--verbose', count=True)
@click.option('--dry', is_flag=True, help='Do not commit changes to disk.')
@click.option('--select', help='Select a subset of hydrators to run (comma separated).')
@click.pass_context
def hydrator(ctx, config, verbose, dry, select):
  """
  Hydrate your development environment.

  Without arguments, all hydrators will be run.
  """

  if verbose >= 2:
    level = logging.DEBUG
  elif verbose >= 1:
    level = logging.INFO
  else:
    level = logging.WARNING
  logging.basicConfig(
    format='[%(levelname)s - %(name)s - %(asctime)s]: %(message)s',
    level=level)

  ctx.ensure_object(dict)
  ctx.obj['config'] = config = Hydrator.load(config or 'hydrator.yml')

  if not ctx.invoked_subcommand:
    if select:
      try:
        hydrators = [config.hydrators[k] for k in select.split(',')]
      except KeyError as exc:
        sys.exit('error: {} is not a known hydrator'.format(exc))
    else:
      hydrators = config.hydrators.values()

    context = Context(config.init_dyna_fs(), dry)
    for hydrator in hydrators:
      hydrator.execute(context)


@hydrator.command()
@click.argument('filesystem', required=False)
def auth_status(filesystem):
  """
  Check the filesystem authentication status.
  """

  if filesystem:
    fs = config.filesystems.get(filesystem)
    if not fs:
      sys.exit('error: {} is not a known filesystem'.format(filesystem))
    filesystems = {filesystem: fs}
  else:
    filesystems = config.filesystems

  for key, value in sorted(filesystems.items(), key=lambda x: x[0]):
    creds = config.credentials.load(key)
    status = 'ok' if value.is_authenticated(creds) else 'not authenticated'
    print('{}: {}'.format(key, status))


@hydrator.command()
@click.argument('filesystem')
def login(filesystem):
  """
  Authenticate for a filesystem.
  """

  fs = config.filesystems.get(filesystem)
  if not fs:
    sys.exit('error: {} is not a known filesystem'.format(filesystem))

  creds = config.credentials.load(filesystem)
  if creds:
    fs.logout(creds)
    config.credentials.delete(filesystem)

  try:
    creds = fs.login()
  except NotImplementedError:
    sys.exit('error: {} does not require authentication'.format(filesystem))

  config.credentials.save(filesystem, creds)
  print('authenticated.')


@hydrator.command()
@click.argument('filesystem')
def logout(filesystem):
  """
  Revoke existing credentials for a filesystem.
  """

  fs = config.filesystems.get(filesystem)
  if not fs:
    sys.exit('error: {} is not a known filesystem'.format(filesystem))

  creds = config.credentials.load(filesystem)
  if creds:
    fs.logout(creds)
    config.credentials.delete(filesystem)
    print('logged out.')
  else:
    print('no credentials saved.')
