"""
Copyright (c) 2015, 2020 Tim Waugh <tim@cyberelk.net>

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

from collections import namedtuple
from collections.abc import Iterator
import errno
from journal_brief.constants import PRIORITY_MAP
from logging import getLogger
import os
from systemd import journal


log = getLogger(__name__)


class SelectiveReader(journal.Reader):
    """
    A Reader instance with matches applied
    """

    def __init__(self, log_level=None, this_boot=None, inclusions=None,
                 explicit_inclusions=None):
        """Constructor

        :param log_level: int, LOG_* priority level
        :param this_boot: bool, process messages from this boot
        :param inclusions: dict, field -> values, PRIORITY may use value
                           instead of list
        :param explicit_inclusions: dict, field -> values, but
                                    log_level is not applied to any of
                                    these

        """
        super(SelectiveReader, self).__init__()

        log.debug("setting inclusion filters:")
        assert not inclusions or isinstance(inclusions, list)
        assert not explicit_inclusions or isinstance(explicit_inclusions, list)

        Rule = namedtuple('Rule', ('log_level', 'inclusion'))

        # 'inclusions' use 'log_level' for each disjunct
        rules = [Rule(log_level=log_level, inclusion=inclusion)
                 for inclusion in inclusions or []]

        # 'explicit_inclusions' don't. This is to allow output
        # formatters to specify their own explicit inclusions rules
        # without needing to set PRIORITY.
        rules += [Rule(log_level=None, inclusion=inclusion)
                  for inclusion in explicit_inclusions or []]

        if rules:
            self.set_filter_rules(rules, this_boot=this_boot)
        else:
            if this_boot:
                log.debug("this_boot()")
                self.this_boot()

            if log_level is not None:
                log.debug("log_level(%r)", log_level)
                self.log_level(log_level)

        log.debug("no more inclusion filters")

    def process_rule(self, rule, this_boot):  # noqa: C901
        assert isinstance(rule.inclusion, dict)
        for field, matches in rule.inclusion.items():
            if field == 'PRIORITY':
                try:
                    this_log_level = int(PRIORITY_MAP[matches])
                except (AttributeError, TypeError):
                    pass
                else:
                    # These are equivalent:
                    # - PRIORITY: 3
                    # - PRIORITY: err
                    # - PRIORITY: [0, 1, 2, 3]
                    # - PRIORITY: [emerg, alert, crit, err]
                    log.debug("log_level(%r)", this_log_level)
                    self.log_level(this_log_level)
                    continue

            assert isinstance(matches, list)
            for match in matches:
                if field == 'PRIORITY':
                    try:
                        match = PRIORITY_MAP[match]
                    except (AttributeError, TypeError):
                        pass

                log.debug("%s=%s", field, match)
                self.add_match(**{str(field): str(match)})

        if this_boot:
            log.debug("this_boot()")
            self.this_boot()

        if rule.log_level is not None:
            log.debug("log_level(%r)", rule.log_level)
            self.log_level(rule.log_level)

    def set_filter_rules(self, rules, this_boot=None):
        for index, rule in enumerate(rules):
            if index:
                log.debug("-or-")
                self.add_disjunction()

            self.process_rule(rule, this_boot)


class LatestJournalEntries(Iterator):
    """
    Iterate over new journal entries since last time
    """

    def __init__(self, cursor_file=None, reader=None, dry_run=False,
                 seek_cursor=True):
        """
        Constructor

        :param cursor_file: str, filename of cursor bookmark file
        :param reader: systemd.journal.Reader instance
        :param dry_run: bool, whether to update the cursor file
        :param seek_cursor: bool, whether to seek to bookmark first
        """
        super(LatestJournalEntries, self).__init__()

        self.cursor_file = cursor_file
        try:
            with open(self.cursor_file, "rt") as fp:
                self.cursor = fp.read()
        except IOError as ex:
            if ex.errno == errno.ENOENT:
                self.cursor = None
            else:
                raise

        if reader is None:
            reader = journal.Reader()

        if self.cursor:
            if seek_cursor:
                log.debug("Seeking to %s", self.cursor)
                reader.seek_cursor(self.cursor)
                reader.get_next()
        elif not dry_run:
            # use an unfiltered Reader to find the current 'tail'
            # of the journal and store that as the initial cursor
            # when the cursor file could not be found; this avoids
            # reading through the entire journal again on the next
            # run if the inclusions and exclusions result in zero
            # matching entries during this run
            temp_reader = journal.Reader()
            temp_reader.seek_tail()
            fields = temp_reader.get_previous()
            if fields:
                self.cursor = fields['__CURSOR']
            else:
                self.cursor = ''
            temp_reader.close()

        self.reader = reader
        self.dry_run = dry_run

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        # if an exception was thrown by the code using this
        # context manager, don't update the cursor
        if exc_type is not None:
            return

        if self.dry_run:
            return

        path = os.path.dirname(self.cursor_file)
        try:
            os.makedirs(path)
        except OSError as ex:
            if ex.errno == errno.EEXIST and os.path.isdir(path):
                pass
            else:
                raise

        with open(self.cursor_file, "wt") as fp:
            fp.write(self.cursor)

    def __next__(self):
        fields = self.reader.get_next()
        if not fields:
            raise StopIteration

        if '__CURSOR' in fields:
            self.cursor = fields['__CURSOR']

        return fields
