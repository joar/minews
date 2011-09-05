import minews
import code
import server
import tornado.ioloop

code.interact(
    '''minews interactive
------------------

Variables
 - feeds: An instance of minews.Feeds
 - application: An instance of tornado.web.Application
''',
    None,
    {
        'feeds': server.feeds,
        'application': server.application})
