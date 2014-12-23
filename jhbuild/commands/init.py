# jhbuild - a tool to ease building collections of source packages
#
#   init.py: initialize a jhbuild working tree
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

from optparse import make_option
import os
import subprocess
import sys

import jhbuild.moduleset
import jhbuild.frontends
from jhbuild.errors import CommandError
from jhbuild.commands import Command, register_command
from jhbuild.utils.cmds import get_output

class cmd_init(Command):
    doc = N_('Initialize a JHBuild working tree')

    name = 'init'
    usage_args = N_('PROJECT_REPO [REVISION]')

    def __init__(self):
        Command.__init__(self)

    def run(self, config, options, args, help=None):
        try:
            cmd = ['git', 'clone']
            cmd.append(args[0])
            cmd.append('jhbuild/modulesets')
            get_output(cmd)

            cmd = ['ln', '-s', 'modulesets/default.modules', 'jhbuild/moduleset']
            get_output(cmd)

            cmd = ['cp', 'jhbuild/modulesets/default.config', 'jhbuild/config']
            get_output(cmd)
        except CommandError:
            raise FatalError(_('Failed to initialize project'))

register_command(cmd_init)
