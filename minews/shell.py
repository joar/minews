from . import *
import code

def run():
    feeds = Feeds()

    code.interact(
        'minews interactive\n'
        '------------------\n'
        '\n'
        'Variables\n'
        ' - feeds: An instance of minews.Feeds',
        None,
        {
            'feeds': feeds})
