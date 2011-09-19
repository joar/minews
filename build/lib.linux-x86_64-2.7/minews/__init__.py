import feedparser
import pymongo
import logging
import datetime
import urllib
import json
import time
import mongokit
from minews.config import FEEDS, PROJECTS

import minews.iterators

import minews.models

logger = logging.getLogger(__name__)
logging.basicConfig()
logger.setLevel(logging.DEBUG)


class Feeds:
    def __init__(self):
        self.connection = mongokit.Connection('localhost', 27017)

        minews.models.register_models(self.connection)

        self.db = self.connection.minews

        self.db.entries.ensure_index([
                ('posted', 1),
                ('guid', 1),
                ('type', 1),
                ('project', 1),
                ('category', 1)])

    def get_compiled(self, **kwargs):
        return self.db.FeedEntry.find(
            limit=kwargs.get('limit') or 20).sort([
                ('posted', pymongo.DESCENDING)])

    def update(self):
        stats = self.db.StatisticsEntry()
        stats.save()

        self.ITERATOR_MAP = {
            'rss': minews.iterators.RSSIterator,
            'identica-atom': minews.iterators.IdenticaRSSIterator,
            'diaspora-atom': minews.iterators.DiasporaAtomIterator,
            'gitorious-atom': minews.iterators.RSSIterator,
            'github-atom': minews.iterators.RSSIterator,
            'googlegroups-rss': minews.iterators.GoogleGroupsRSSIterator,
            'twitter-json': minews.iterators.TwitterJSONIterator}

        for project in self.db.ProjectEntry.find():
            for feed_data in project['feeds']:
                feed_data['project'] = project
                iterator = self.ITERATOR_MAP[
                    feed_data['type']]

                for entry, was_parsed, existed in iterator(self.db, feed_data):
                    if not entry['source']['name'] in stats['fetched']:
                        stats['fetched'].append(entry['source']['name'])
                        stats.save()

                    if not entry:
                        stats['errors'].append((feed_data, was_parsed, existed))
                        logger.error((feed_data, was_parsed, existed))
                        continue

                    if was_parsed:
                        stats['updated'].append(entry['guid'])
                        stats.save()

                        logger.debug('{action} {guid}'.format(
                                guid=entry['guid'],
                                action='UPDATED' if existed and was_parsed else\
                                    'Did NOTHING to' if existed and not was_parsed else\
                                    'INSERTED data ' if not existed and was_parsed else 'ERROR'))

        stats['in_progress'] = False
        stats.save()

    def update_projects(self):
        for project in PROJECTS:
            entry = self.db.ProjectEntry.find_one({'handle': project['handle']})
            logger.debug('==== Found entry: {0}'.format(entry))

            if not entry:
                entry = self.db.ProjectEntry()

            order = list()
            for key, val in project.items():
                order.append(key)

            for key, val in project.items():
                logger.debug(u'{0} => {1}'.format(key, val))
                logger.debug(order)
                entry[key] = val

            entry.save()
