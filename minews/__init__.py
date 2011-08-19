import feedparser
import pymongo
import logging
import datetime
import urllib
import json
import time

from minews.util import parse_tweet

logger = logging.getLogger(__name__)
logging.basicConfig()
logger.setLevel(logging.INFO)

class Feeds:
    feeds = [
        ('http://twitter.com/statuses/user_timeline/notch.json', {
                'source_type': 'twitter',
                'format': 'json'
                }),
        ('http://twitter.com/statuses/user_timeline/jeb_.json', {
                'source_type': 'twitter',
                'format': 'json'
                }),
        ('http://twitter.com/statuses/user_timeline/carlmanneh.json', {
                'source_type': 'twitter',
                'format': 'json'
                }),
        ('http://twitter.com/statuses/user_timeline/danfrisk.json', {
                'source_type': 'twitter',
                'format': 'json'
                }),
        ('http://twitter.com/statuses/user_timeline/kappische.json', {
                'source_type': 'twitter',
                'format': 'json'
                }),
        ('http://twitter.com/statuses/user_timeline/jahkob.json', {
                'source_type': 'twitter',
                'format': 'json'
                }),
        ('http://twitter.com/statuses/user_timeline/jnkboy.json', {
                'source_type': 'twitter',
                'format': 'json'
                }),
        ('http://twitter.com/statuses/user_timeline/mollstam.json', {
                'source_type': 'twitter',
                'format': 'json'
                }),
        ('http://mcupdate.tumblr.com/rss', {
                'thumbnail_url': 'http://dummyimage.com/50x50&text=mcupdate',
                'source_type': 'blog'
                }),
        ('http://mojang.com/feed/', {
                'thumbnail_url': 'http://dummyimage.com/50x50&text=mojang',
                'source_type': 'blog'
                }),
        ('http://notch.tumblr.com/rss', {
                'thumbnail_url': 'http://dummyimage.com/50x50&text=notch',
                'source_type': 'blog'
                })
        ]

    def __init__(self):
        self.connection = pymongo.Connection('localhost', 27017)
        self.db = self.connection.minews

        self.db.entries.ensure_index([
                ('updated', 1),
                ('id', 1)])

    def update_db(self):
        logger.info('== Reading data sources... ==')
        for feed_url, feed_data in self.feeds:
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
        return self.db.entries.find(
            limit=kwargs.get('limit') or 20).sort([
                ('updated', pymongo.DESCENDING)])

class FeedEntry:
    updated = False
    link = False
    title = False
    context_url = False
    context = False
    guid = False
    content = False
    thumbnail_url = False
    source = False
    source_name = False
    source_link = False
    thumbnail_url = False

    def __init__(self, **kwargs):
        for key, val in kwargs.items():
            self.__dict__[key] = val

