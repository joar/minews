import feedparser
import pymongo
import logging
import datetime
import urllib
import json
import time
import mongokit
from minews.config import FEEDS

from minews.util import parse_tweet, links2html

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
                ('updated', 1),
                ('id', 1)])

    def update_db(self):
        logger.info('== Reading data sources... ==')
        for feed_url, feed_data in FEEDS:
            if feed_data.get('source_type') == 'twitter' and feed_data.get('format') == 'json':
                r = urllib.urlopen(feed_url)
                d = json.load(r)
                for item in d:
                    if not self.db.entries.find({
                            'guid': 'http://twitter.com/%s/statuses/%s' % (item['user']['screen_name'], item['id'])
                            }).count():
                        data = dict(
                            updated=datetime.datetime.strptime(
                                        item['created_at'],
                                        '%a %b %d %H:%M:%S +0000 %Y'),  # Thu Aug 06 17:08:06 +0000 2009
                            link='http://twitter.com/%s/statuses/%s' % (item['user']['screen_name'], item['id']),
                            guid='http://twitter.com/%s/statuses/%s' % (item['user']['screen_name'], item['id']),
                            content=parse_tweet(
                                item['text']),
                            source='twitter',
                            source_name='@%s' % item['user']['screen_name'],
                            source_link='http://twitter.com/%s' % item['user']['screen_name'],
                            thumbnail_url=item['user']['profile_image_url'])

                        if item['in_reply_to_screen_name']:
                            data['context'] ='In reply to @%s' % item['in_reply_to_screen_name']
                            data['context_url'] = 'http://twitter.com/%s/statuses/%s' % (item['in_reply_to_screen_name'], item['in_reply_to_status_id'])
                        data = FeedEntry(**data)
                        logger.info('Inserted as %s' % data.__dict__)

                        self.db.entries.insert(
                            data.__dict__)
            else:
                d = feedparser.parse(feed_url)
                for entry in d.entries:
                    if not self.db.entries.find({
                            'guid': entry.id }).count():
                        print(entry)
                        data = dict(
                            updated=datetime.datetime(
                                *(entry.updated_parsed)[0:6]),
                            content=entry.summary,
                            title=entry.title,
                            context='Read more',
                            context_url=entry.link,
                            link=entry.link,
                            guid=entry.id,
                            thumbnail_url=feed_data.get('thumbnail_url') or '',
                            source=feed_data.get('source_type') or '',
                            source_name=d.feed.title,
                            source_link=d.feed.link,
                            )
                        data = FeedEntry(**data)

                        logger.info('Inserted %s' % data.__dict__)

                        self.db.entries.insert(data.__dict__)
                    else:
                        logger.debug('%s already exists in db' % entry['id'])

        logger.info('== Read all data sources ==')

    def get_compiled(self, **kwargs):
        return self.db.FeedEntry.find(
            limit=kwargs.get('limit') or 20).sort([
                ('posted', pymongo.DESCENDING)])

    def update(self):
        self.ITERATOR_MAP = {
            'rss': minews.iterators.RSSIterator,
            'identica-rss': minews.iterators.IdenticaRSSIterator,
            'diaspora-atom': minews.iterators.DiasporaAtomIterator,
            'googlegroups-rss': minews.iterators.GoogleGroupsRSSIterator}

        for feed_data in FEEDS:
            iterator = self.ITERATOR_MAP[
                feed_data['type']]

            for entry, was_parsed, existed in iterator(self.db, feed_data):
                if not entry:
                    logger.error((feed_data, was_parsed, existed))
                    continue

                logger.debug('{action} {guid}'.format(
                        guid=entry['guid'],
                        action='UPDATED' if existed and was_parsed else\
                            'Did NOTHING to' if existed and not was_parsed else\
                            'INSERTED data ' if not existed and was_parsed else 'ERROR'))

