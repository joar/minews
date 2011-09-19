import tornado.ioloop
import tornado.web
import minews
import minews.util as util
import pymongo

from minews.util import get_template

feeds = minews.Feeds()

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

if __name__ == "__main__":
    application.listen(8080)
    tornado.ioloop.IOLoop.instance().start()
