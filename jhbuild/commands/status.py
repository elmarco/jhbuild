# jhbuild - a tool to ease building collections of source packages
# Copyright (C) 2014  Red Hat, Inc.
#
#   status.py: status in jhbuild source code
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
import sys
import subprocess

import jhbuild.moduleset
import jhbuild.frontends
from jhbuild.errors import CommandError
from jhbuild.commands import Command, register_command


class cmd_status(Command):
    doc = _('Check branch status')

    name = 'status'
    usage_args = '[ options ... ]'

    def __init__(self):
        Command.__init__(self)

    def run(self, config, options, args, help=None):
        module_set = jhbuild.moduleset.load(config)
        module_list = module_set.get_module_list(config.modules, config.skip)

        for module in module_list[:]:
            if module.branch is None:
                continue

            status = module.branch.status()
            if status == "":
                continue
            print module.branch.get_checkoutdir()
            print status

register_command(cmd_status)
