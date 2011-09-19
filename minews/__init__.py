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

''' For serve() '''
import tornado.ioloop
import tornado.web
import minews
import minews.util as util
import pymongo

from minews.util import get_template
''' end '''

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

def serve():
    feeds = Feeds()

    class FeedsRequestHandler(tornado.web.RequestHandler):
        def initialize(self, feeds):
            self.feeds = feeds
            self.context = dict(
                reverse_url=self.reverse_url)

        def get(self):
            self.write('Not implemented')

        def render(self, template_name, data = {}):
            data['context'] = self.context

            template = get_template(template_name)
            self.write(
                template.render(data))


    class MainHandler(FeedsRequestHandler):
        def get(self):
            self.render('index.html', {
                    'entries': util.generate_entries(
                        query=self.feeds.db.FeedEntry.find(
                            {'audience': 'general'},
                            limit=100).sort([
                                ('posted', pymongo.DESCENDING)]),
                        db=self.feeds.db)})


    class ProjectHandler(FeedsRequestHandler):
        def get(self, project):
            project = self.feeds.db.ProjectEntry.find_one({
                    'handle': project})

            self.render('project.html', {
                    'entries_general': util.generate_entries(
                        query=self.feeds.db.FeedEntry.find({
                                'project': project['_id'],
                                'audience': 'general'}, limit=10).sort([
                                ('posted', pymongo.DESCENDING)]),
                        project=project),
                    'entries_advanced': util.generate_entries(
                        query=self.feeds.db.FeedEntry.find({
                                'project': project['_id'],
                                'audience': 'advanced'}, limit=10).sort([
                                ('posted', pymongo.DESCENDING)]),
                        project=project),
                    'project': project,
                    'no_logo': True,
                    'request': self.request})


    class ProjectsPageHandler(FeedsRequestHandler):
        def get(self):
            self.render('projects.html', dict(
                    projects=self.feeds.db.ProjectEntry.find()))


    class StatsHandler(tornado.web.RequestHandler):
        def initialize(self, feeds):
            self.feeds = feeds

            def get(self):
                cursor = feeds.db.StatisticsEntry.find().sort('created', pymongo.DESCENDING)

                self.set_header('Content-Type', 'text/plain; charset=UTF-8')

                for stats in cursor:
                    self.write(u'{time}'.format(
                            time=stats['created']))

                    if stats['in_progress']:
                        self.write(u' - In progress\n')
                    else:
                        self.write(u'\n')

                    if stats['fetched'] or stats['updated'] or stats['errors']:
                        self.write(u'\tUPDATED:\n\t\t{updated}\n'.format(
                                updated=u'\n\t\t'.join(stats['updated']) if len(stats['updated']) else 'None'))
                        
                        self.write(u'\tFETCHED:\n\t\t{fetched}\n'.format(
                                fetched='\n\t\t'.join(
                                    stats['fetched']) if stats['fetched'] else 'None'))
                    else:
                        self.write('\tNOTHING\n')

    application = tornado.web.Application([
            (r'/', MainHandler, dict(feeds=feeds)),
            (r'/p/([a-z]*)', ProjectHandler, dict(feeds=feeds)),
            (r'/static/(.*)', tornado.web.StaticFileHandler, {'path': './minews/static/'}),
            (r'/stats', StatsHandler, dict(feeds=feeds)),
            (r'/projects', ProjectsPageHandler, dict(feeds=feeds))
            ],
                                          debug=True
                                          )
    
    application.listen(8080)
    tornado.ioloop.IOLoop.instance().start()
