# -*- coding: utf-8 -*-

# django-lint -- Static analysis tool for Django projects and applications
# Copyright (C) 2008-2009 Chris Lamb <chris@chris-lamb.co.uk>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from logilab import astng

from pylint.interfaces import IASTNGChecker
from pylint.checkers import BaseChecker
from pylint.checkers.utils import safe_infer

class SettingsChecker(BaseChecker):
    __implements__ = IASTNGChecker

    name = 'django_settings_checker'
    msgs = {
        'W7001': ('Missing required field %r', '',),
        'W7002': ('Empty %r setting', '',),
    }

    def leave_module(self, node):
        if node.name.split('.')[-1] != 'settings':
            return

        REQUIRED_FIELDS = {
            'DEBUG': bool,
            'TEMPLATE_DEBUG': bool,
            'INSTALLED_APPS': tuple,
            'MANAGERS': tuple,
            'ADMINS': tuple,
        }

        for field, req_type in REQUIRED_FIELDS.iteritems():
            if field not in node.locals.keys():
                self.add_message('W7001', args=field, node=node)
                continue

            if req_type is tuple:
                ass = node.locals[field][-1]
                val = safe_infer(ass)

                if val and not val.nodes:
                    self.add_message('W7002', args=field, node=ass)