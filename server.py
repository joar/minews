import tornado.ioloop
import tornado.web
import minews

from minews.util import get_template

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        f = minews.Feeds()

        template = get_template('index.html')

        self.write(
            template.render({
                    'entries': f.get_compiled(limit=100)
                    }))

application = tornado.web.Application([
        (r"/", MainHandler),
        (r"/static/(.*)", tornado.web.StaticFileHandler, {'path': './static/'})
    ],
    debug=True
    )

if __name__ == "__main__":
    application.listen(8080)
    tornado.ioloop.IOLoop.instance().start()
