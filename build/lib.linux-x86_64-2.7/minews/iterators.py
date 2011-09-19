# minews - Information aggregator and parser
# Copyright (C) 2011  Joar Wandborg
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
# 
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import minews.parsers
import feedparser
import urllib
import json

from bson import ObjectId

class JSONIterator:
    def __init__(self, db, feed_data):
        request = urllib.urlopen(
            feed_data['url'])

        self.data = json.load(request)

        self.db = db

        self.feed_data = feed_data

        self.index = 0

        self._set_parser_object()

    def __iter__(self):
        return self

    def _set_parser_object(self):
        self.parser_object = minews.parsers.JSONParser

    def next(self):
        try:
            item = self.data[self.index]
            self.index += 1

            entry, was_parsed, existed = self.parser_object(self.db, item).parse()

            if was_parsed:
                entry['project'] = self.feed_data['project']['_id']
                entry['type'] = unicode(self.feed_data['type'])
                entry['audience'] = self.feed_data['audience']
                entry['source'] = {}

                if existed:
                    entry.update()
                else:
                    entry.save()

            return entry, was_parsed, existed
        except IndexError:
            raise StopIteration


class TwitterJSONIterator(JSONIterator):
    def _set_parser_object(self):
        self.parser_object = minews.parsers.TwitterJSONParser


class RSSIterator:
    def __init__(self, db, feed_data):
        self.data = feedparser.parse(
            feed_data['url'])

        self.db = db

        self.feed_data = feed_data

        self.index = 0

        self._set_parser_object()

    def __iter__(self):
        return self

    def _set_parser_object(self):
        self.parser_object = minews.parsers.RSSParser

    def next(self):
        try:
            item = self.data.entries[self.index]
            self.index += 1

            entry, was_parsed, existed = self.parser_object(self.db, item).parse()

            if was_parsed:
                entry['project'] = self.feed_data['project']['_id']
                entry['type'] = unicode(self.feed_data['type'])
                entry['audience'] = self.feed_data['audience']
                entry['source'] = {
                    'name': unicode(self.data.feed.title),
                    'link': unicode(self.data.feed.link)}

                if existed:
                    entry.update()
                else:
                    entry.save()

            return entry, was_parsed, existed
        except IndexError:
            raise StopIteration


class GoogleGroupsRSSIterator(RSSIterator):
    def next(self):
        try:
            item = self.data.entries[self.index]
            self.index += 1

            entry, was_parsed, existed = self.parser_object(self.db, item).parse()

            if was_parsed:
                entry['project'] = self.feed_data['project']['_id']
                entry['type'] = unicode(self.feed_data['type'])
                entry['audience'] = self.feed_data['audience']
                entry['source'] = {
                    'name': unicode(self.data.feed.title),
                    'link': unicode(self.data.feed.id)}

                if existed:
                    entry.update()
                else:
                    entry.save()

            return entry, was_parsed, existed
        except IndexError:
            raise StopIteration

class IdenticaRSSIterator(RSSIterator):
    def _set_parser_object(self):
        self.parser_object = minews.parsers.IdenticaRSSParser


class DiasporaAtomIterator(RSSIterator):
    def _set_parser_object(self):
        self.parser_object = minews.parsers.DiasporaAtomParser
