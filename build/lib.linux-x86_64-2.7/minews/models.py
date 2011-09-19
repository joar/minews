from mongokit import Document
from bson import ObjectId
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
        'project': ObjectId,
        'categories': [ObjectId],
        'type': unicode,
        'audience': unicode,
        'parsed': bool,
        'raw': unicode}

    required_fields = [
        'guid',
        'imported',
        'posted',
        'permalink',
        'type',
        'audience']

    default_values = {
        'imported': datetime.datetime.utcnow}

class StatisticsEntry(Document):
    __collection__ = 'statistics'

    structure = {
        'created': datetime.datetime,
        'in_progress': bool,
        'updated': list,  # List of guids
        'fetched': list,  # List of guids
        'errors': list}

    required_fields = [
        'created']

    default_values = {
        'created': datetime.datetime.utcnow,
        'in_progress': True}


class ProjectEntry(Document):
    __collection__ = 'projects'

    structure = dict(
        created=datetime.datetime,
        name=unicode,
        handle=unicode,
        description=unicode,
        logo_url=unicode,
        links=dict,
        feeds=list(
            dict(
                url=unicode,
                type=unicode,
                audience=unicode)))

    required_fields = [
        'created',
        'name',
        'handle']

    default_values = dict(
        created=datetime.datetime.utcnow)


REGISTER_MODELS = [
    FeedEntry,
    StatisticsEntry,
    ProjectEntry]

def register_models(connection):
    connection.register(REGISTER_MODELS)
