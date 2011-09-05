import tornado.ioloop
import tornado.web
import minews

from minews.util import get_template

feeds = minews.Feeds()

class MainHandler(tornado.web.RequestHandler):
    def initialize(self, feeds):
        self.feeds = feeds

    def get(self):
        template = get_template('index.html')

        self.write(
            template.render({
                    'entries': self.feeds.get_compiled(limit=100)
                    }))

class ProjectHandler(tornado.web.RequestHandler): 
    def initialize(self, feeds):
        self.feeds = feeds

    def get(self, project):
        template = get_template('index.html')

        self.write(
            template.render({
                    'entries': self.feeds.db.FeedEntry.find({'project': project})}))

application = tornado.web.Application([
        (r"/", MainHandler, dict(feeds=feeds)),
        (r"/p/([a-z]*)", ProjectHandler, dict(feeds=feeds)),
        (r"/static/(.*)", tornado.web.StaticFileHandler, {'path': './minews/static/'})
    ],
    debug=True
    )

if __name__ == "__main__":
    application.listen(8080)
    tornado.ioloop.IOLoop.instance().start()
