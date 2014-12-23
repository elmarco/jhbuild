# jhbuild - a tool to ease building collections of source packages
# Copyright (C) 2014  Red Hat, Inc.
#
#   grep.py: grep in jhbuild source code
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


class cmd_grep(Command):
    doc = _('Grep all modules')

    name = 'grep'
    usage_args = '[ options ... ]'

    def __init__(self):
        Command.__init__(self)

    def run(self, config, options, args, help=None):
        module_set = jhbuild.moduleset.load(config)
        module_list = module_set.get_module_list(config.modules, config.skip)
        buildscript = jhbuild.frontends.get_buildscript(config, module_list)

        # remove modules that are not marked as installed
        packagedb = module_set.packagedb
        for module in module_list[:]:
            if module.branch is None:
                continue
            try:
                files = module.branch.list_files()
                prefix = os.path.commonprefix(files).rpartition(os.path.sep)[0]
                path = os.path.dirname(prefix)
                files = [os.path.relpath(x, path) for x in files]
                color = "--color=never"
                if sys.stdout.isatty():
                    color = "--color=always"
                p = subprocess.Popen([ "grep", color, args[0] ] + files, cwd=path)
                p.wait()
            except OSError:
                pass

register_command(cmd_grep)
