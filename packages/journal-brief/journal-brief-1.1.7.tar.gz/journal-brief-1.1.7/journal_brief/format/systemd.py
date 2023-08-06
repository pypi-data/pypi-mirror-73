"""
Copyright (c) 2015 Tim Waugh <tim@cyberelk.net>

## This program is free software; you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation; either version 2 of the License, or
## (at your option) any later version.

## This program is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU General Public License for more details.

## You should have received a copy of the GNU General Public License
## along with this program; if not, write to the Free Software
## Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
"""

from collections import defaultdict
from journal_brief.format import EntryFormatter
from locale import strxfrm


class SystemdFormatter(EntryFormatter):
    """
    Show failed systemd units
    """

    FORMAT_NAME = "systemd"
    FILTER_INCLUSIONS = [
        {
            # New session
            '_COMM': ['systemd'],
            'CODE_FUNCTION': ['unit_notify'],
        },
    ]

    def __init__(self, *args, **kwargs):
        super(SystemdFormatter, self).__init__(*args, **kwargs)
        self.failed = defaultdict(int)

    def format(self, entry):
        try:
            message = entry['MESSAGE']
            unit = entry['UNIT']
        except KeyError:
            return ''

        if 'entered failed state' in message:
            self.failed[unit] += 1

        return ''

    def flush(self):
        if not self.failed:
            return ''

        ret = '\nFailed systemd units:\n\n'
        units = sorted(self.failed.items(),
                       key=lambda item: strxfrm(item[0]))
        for unit, count in units:
            ret += '{count:>5} x {unit}\n'.format(count=count, unit=unit)

        return ret
