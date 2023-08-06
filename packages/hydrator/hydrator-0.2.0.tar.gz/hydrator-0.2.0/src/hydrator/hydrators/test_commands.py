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

from .commands import expand_matrix, prepare_command, PreparedCommand


def test_expand_matrix():
  assert expand_matrix('abc') == ['abc']
  assert expand_matrix('a{b,c}') == ['ab', 'ac']
  assert expand_matrix('a{b,c}d{e,f,g}') == ['abde', 'abdf', 'abdg', 'acde', 'acdf', 'acdg']


def test_prepare_command():
  command = 'cp [[nextcloud://id_rsa{,.pub}]] ~/.ssh'
  assert prepare_command(command) == PreparedCommand(
    command,
    ['cp', '<subst:1>', '~/.ssh'],
    {1: ['nextcloud://id_rsa', 'nextcloud://id_rsa.pub']})
