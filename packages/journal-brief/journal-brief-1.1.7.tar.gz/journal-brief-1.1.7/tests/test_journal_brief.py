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

from flexmock import flexmock
from inspect import getsourcefile
from tests.util import Watcher
import journal_brief
from journal_brief import SelectiveReader, LatestJournalEntries
from systemd import journal
import os
import pytest
import re


class TestSelectiveReader(object):
    def watch_reader(self):
        (flexmock(journal.Reader)
            .should_receive('get_next')
            .and_return({}))
        watcher = Watcher()
        for func in ['add_match',
                     'add_conjunction',
                     'add_disjunction',
                     'log_level',
                     'this_boot']:
            (flexmock(journal.Reader)
                .should_receive(func)
                .replace_with(watcher.watch_call(func)))

        return watcher

    def test_inclusions(self):
        watcher = self.watch_reader()
        inclusions = [{'PRIORITY': ['emerg', 'alert', 'crit', 'err']},
                      {'PRIORITY': ['4', '5', '6'],
                       '_SYSTEMD_UNIT': ['myservice.service']}]
        SelectiveReader(log_level=0, this_boot=True, inclusions=inclusions)

        # Should add matches for all of the first group
        assert set(watcher.calls[:4]) == set([
            ('add_match', (), "{'PRIORITY': '0'}"),
            ('add_match', (), "{'PRIORITY': '1'}"),
            ('add_match', (), "{'PRIORITY': '2'}"),
            ('add_match', (), "{'PRIORITY': '3'}"),
        ])

        # Then a this_boot() match
        assert watcher.calls[4][0] == 'this_boot'

        # Then a log_level() match
        assert watcher.calls[5] == ('log_level', (0,), '{}')

        # Then a disjunction
        assert watcher.calls[6][0] == 'add_disjunction'

        # Then matches for all of the second group
        assert set(watcher.calls[7:11]) == set([
            ('add_match', (), "{'PRIORITY': '4'}"),
            ('add_match', (), "{'PRIORITY': '5'}"),
            ('add_match', (), "{'PRIORITY': '6'}"),
            ('add_match', (), "{'_SYSTEMD_UNIT': 'myservice.service'}"),
        ])

        # Then a this_boot() match
        assert watcher.calls[11][0] == 'this_boot'

        # Then a log_level() match
        assert watcher.calls[12] == ('log_level', (0,), '{}')

        # No more
        assert len(watcher.calls) == 13

    def test_inclusion_log_level(self):
        watcher = self.watch_reader()
        inclusions = [{'PRIORITY': '0'},  # no effect, log_level==1
                      {'PRIORITY': '2'}]
        SelectiveReader(log_level=1, inclusions=inclusions)

        # Matches for {'PRIORITY': '0'}
        assert set(watcher.calls[0:2]) == set([
            ('log_level', (0,), '{}'),
            ('log_level', (1,), '{}'),
        ])

        # A disjunction
        assert watcher.calls[2] == ('add_disjunction', (), '{}')

        # Matches for {'PRIORITY': '2'}
        assert set(watcher.calls[3:5]) == set([
            ('log_level', (2,), '{}'),
            ('log_level', (1,), '{}'),
        ])

        # No more
        assert len(watcher.calls) == 5

    def test_no_inclusions(self):
        watcher = self.watch_reader()
        SelectiveReader(log_level=0, this_boot=True)

        # Should have two matches
        assert len(watcher.calls) == 2

        # A this_boot() match
        assert watcher.calls[0][0] == 'this_boot'

        # And a log_level() match
        assert watcher.calls[1] == ('log_level', (0,), '{}')


@pytest.fixture
def cursor_file_path(tmp_path):
    return os.path.join(str(tmp_path), 'cursor')


@pytest.fixture
def cursor_file(cursor_file_path):
    with open(cursor_file_path, 'w+t') as fp:
        yield fp


@pytest.fixture
def missing_or_empty_cursor():
    (flexmock(journal.Reader)
        .should_receive('seek_tail')
        .once())
    (flexmock(journal.Reader)
        .should_receive('get_previous')
        .and_return({'__CURSOR': '0'}))


class TestLatestJournalEntries(object):
    def test_without_cursor(self, cursor_file_path, missing_or_empty_cursor):
        final_cursor = '2'
        (flexmock(journal.Reader)
            .should_receive('seek_cursor')
            .never())
        (flexmock(journal.Reader)
            .should_receive('get_next')
            .and_return({'__CURSOR': '1'})
            .and_return({'__CURSOR': final_cursor})
            .and_return({}))

        with LatestJournalEntries(cursor_file=cursor_file_path) as entries:
            e = list(entries)

        assert len(e) == 2
        with open(cursor_file_path, 'rt') as fp:
            assert fp.read() == final_cursor

    def test_empty_cursor(self, cursor_file, missing_or_empty_cursor):
        final_cursor = '2'
        (flexmock(journal.Reader)
            .should_receive('seek_cursor')
            .never())
        (flexmock(journal.Reader)
            .should_receive('get_next')
            .and_return({'__CURSOR': '1'})
            .and_return({'__CURSOR': final_cursor})
            .and_return({}))

        with LatestJournalEntries(cursor_file=cursor_file.name) as entries:
            e = list(entries)

        assert len(e) == 2

        cursor_file.seek(0)
        assert cursor_file.read() == final_cursor

    def test_with_cursor(self, cursor_file):
        last_cursor = '2'
        final_cursor = '4'
        results = [{'__CURSOR': last_cursor},
                   {'__CURSOR': '3'},
                   {'__CURSOR': final_cursor}]
        (flexmock(journal.Reader)
            .should_receive('seek_cursor')
            .with_args(last_cursor)
            .once())
        (flexmock(journal.Reader)
            .should_receive('get_next')
            .and_return(results[0])
            .and_return(results[1])
            .and_return(results[2])
            .and_return({}))

        cursor_file.write(last_cursor)
        cursor_file.flush()

        with LatestJournalEntries(cursor_file=cursor_file.name) as entries:
            e = list(entries)

        assert e == results[1:]

        cursor_file.seek(0)
        assert cursor_file.read() == final_cursor

    def test_no_seek_cursor(self, cursor_file):
        last_cursor = '2'
        final_cursor = '3'
        results = [{'__CURSOR': '1'},
                   {'__CURSOR': last_cursor},
                   {'__CURSOR': final_cursor}]

        (flexmock(journal.Reader)
            .should_receive('seek_cursor')
            .never())
        (flexmock(journal.Reader)
            .should_receive('get_next')
            .and_return(results[0])
            .and_return(results[1])
            .and_return(results[2])
            .and_return({}))

        cursor_file.write(last_cursor)
        cursor_file.flush()

        with LatestJournalEntries(cursor_file=cursor_file.name,
                                  seek_cursor=False) as entries:
            e = list(entries)

        assert e == results

        cursor_file.seek(0)
        assert cursor_file.read() == final_cursor


def test_version():
    """
    Check the version numbers agree
    """
    this_file = getsourcefile(test_version)
    regexp = re.compile(r"\s+version='([0-9.]+)',  # also update")
    topdir = os.path.dirname(os.path.dirname(this_file))
    with open(os.path.join(topdir, 'setup.py')) as fp:
        matches = map(regexp.match, fp.readlines())
        matches = [match for match in matches if match]
        assert len(matches) == 1
        assert matches[0].groups()[0] == journal_brief.__version__

    regexp = re.compile(r"^Version:\s+([0-9.]+)")
    with open(os.path.join(topdir, 'python-journal-brief.spec')) as fp:
        matches = map(regexp.match, fp.readlines())
        matches = [match for match in matches if match]
        assert len(matches) == 1
        assert matches[0].groups()[0] == journal_brief.__version__
