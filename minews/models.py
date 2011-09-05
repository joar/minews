from mongokit import Document
import datetime

class FeedEntry(Document):
    __collection__ = 'feed_entries'

    structure = {
        'guid': unicode,
        'imported': datetime.datetime,
        'posted': datetime.datetime,
        'permalink': unicode,
        'title': unicode,
        'content': unicode,
        'context': dict, # dict(label, name)
        'source': dict, # dict(link, name)
        'project': unicode,
        'category': unicode,
        'type': unicode,
        'parsed': bool,
        'raw': str}

    required_fields = [
        'guid',
        'imported',
        'posted',
        'permalink',
        'type']

    default_values = {
        'imported': datetime.datetime.utcnow}


REGISTER_MODELS = [
    FeedEntry]

def register_models(connection):
    connection.register(REGISTER_MODELS)
