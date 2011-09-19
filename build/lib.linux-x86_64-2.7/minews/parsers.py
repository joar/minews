import json
import datetime
import lxml.html
import markdown
import django.utils.text
import minews.config


class JSONParser:
    '''
    Parse JSON feeds
    '''

    ''' Parse needed, either *not in db* or *not entry.parsed* '''
    needs_parse = True

    ''' Exists in db already '''
    exists = False

    ''' FeedEntry '''
    entry = None

    def __init__(self, db, item, entry = None):
        self.db = db
        self.item = item

        self.entry = entry

        self._check_needs_parse()

    def _check_needs_parse(self):
        '''
        Check status for a remote feed item's local database entry.

        If it exists, sets self.entry, if it does not need parsing, sets
        self.needs_parse = True
        '''
        entries = [i for i in self.db.FeedEntry.find({
                'guid': self.get_guid()})]

        if entries:
            self.exists = True
            self.entry = entries[0]

        if entries and entries[0]['parsed']:
            self.needs_parse = False

        return self.needs_parse

    def get_entry(self):
        '''
        Should be called after self._check_needs_parse()
        '''
        if not self.exists:
            return self.db.FeedEntry()

        return self.entry

    def get_guid(self):
        '''
        Returns the guid for the current self.item
        '''
        return self._get_link()

    def _get_link(self):
        '''
        Twitter-specific, returns a link to the item
        '''
        return u'http://twitter.com/{user}/statuses/{item_id}'.format(
            user=self.item['user']['screen_name'],
            item_id=item['id'])

    def parse(self):
        entry = self.get_entry()
        item = self.item

        if self._check_needs_parse():
            entry['guid'] = self.get_guid()
            entry['posted'] = datetime.datetime(
                *(item.updated_parsed)[0:6])
            entry['permalink'] = unicode(item.link)

            summary = item.summary

            if len(summary) > minews.config.CONFIG['entry_max_length']:
                summary = django.utils.text.Truncator(summary).words(
                    50,
                    truncate=' ... <a href="{0}">Read more</a>'.format(
                        entry['permalink']
                        ),
                    html=True)

            entry['content'] = unicode(summary)
            entry['title'] = unicode(item.title)
            entry['context'] = {
                u'label': u'Read more',
                u'link': unicode(item.link)}
            entry['parsed'] = True
            # entry['raw'] = json.dumps(item)

        return self._format_parse_result(entry)

    def _format_parse_result(self, entry):
        return entry, self.needs_parse, self.exists


class TwitterJSONParser(JSONParser):
    pass


class RSSParser:
    '''
    Parse RSS feeds
    '''

    ''' Parse needed, either not in db or entry.parsed == False '''
    needs_parse = True
 
    ''' Exists in db already '''
    exists = False

    ''' FeedEntry '''
    entry = None

    def __init__(self, db, item, entry = None):
        self.db = db
        self.item = item

        self.entry = entry

        self._check_needs_parse()

    def _check_needs_parse(self):
        '''
        Check status for a remote feed item's local database entry.

        If it exists, sets self.entry, if it does not need parsing, sets
        self.needs_parse = True
        '''
        entries = [i for i in self.db.FeedEntry.find({
                'guid': self.get_guid()})]

        if entries:
            self.exists = True
            self.entry = entries[0]

        if entries and entries[0]['parsed']:
            self.needs_parse = False

        return self.needs_parse

    def get_entry(self):
        '''
        Should be called after self._check_needs_parse()
        '''
        if not self.exists:
            return self.db.FeedEntry()

        return self.entry

    def get_guid(self):
        '''
        Returns the guid for the current self.item
        '''
        return unicode(self.item.id)

    def parse(self):
        entry = self.get_entry()
        item = self.item

        if self._check_needs_parse():
            entry['guid'] = self.get_guid()
            entry['posted'] = datetime.datetime(
                *(item.updated_parsed)[0:6])
            entry['permalink'] = unicode(item.link)

            summary = item.summary

            if len(summary) > 500:
                summary = django.utils.text.Truncator(summary).words(
                    50,
                    truncate=' ... <a href="{0}">Read more</a>'.format(
                        entry['permalink']
                        ),
                    html=True)

            entry['content'] = unicode(summary)
            entry['title'] = unicode(item.title)
            entry['context'] = {
                u'label': u'Read more',
                u'link': unicode(item.link)}
            entry['parsed'] = True
            # entry['raw'] = json.dumps(item)

        return self._format_parse_result(entry)

    def _format_parse_result(self, entry):
        return entry, self.needs_parse, self.exists


class GoogleGroupsRSSParser(RSSParser):
    '''
    Parse Google Groups RSS feeds
    '''
    def parse(self):
        entry = self.get_entry()
        item = self.item

        if self._check_needs_parse():
            entry['guid'] = self.get_guid()
            entry['posted'] = datetime.datetime(
                *(item.updated_parsed)[0:6])
            entry['permalink'] = unicode(item.link)
            entry['content'] = unicode(item.summary)
            entry['title'] = unicode(item.title)
            entry['context'] = {
                u'label': u'Read more',
                u'link': unicode(item.link)}
            entry['parsed'] = True
            # entry['raw'] = json.dumps(item)

        return self._format_parse_result(entry)


class IdenticaRSSParser(RSSParser):
    '''
    Parse Identi.ca RSS feeds
    '''
    def parse(self):
        entry = self.get_entry()
        item = self.item

        if self._check_needs_parse():
            entry['guid'] = self.get_guid()
            entry['posted'] = datetime.datetime(
                *(item.updated_parsed)[0:6])
            entry['permalink'] = unicode(item.link)
            entry['content'] = unicode(item.title)
            # entry['title'] = unicode(item.title)
            entry['context'] = {
                u'label': u'Read more',
                u'link': unicode(item.link)}
            entry['parsed'] = True
            # entry['raw'] = json.dumps(item)

        return self._format_parse_result(entry)


class DiasporaAtomParser(RSSParser):
    '''
    Parse Diaspora Atom feeds
    '''
    def parse(self):
        entry = self.get_entry()
        item = self.item

        if self._check_needs_parse():
            md = markdown.Markdown()

            entry['guid'] = self.get_guid()
            entry['posted'] = datetime.datetime(
                *(item.updated_parsed)[0:6])
            entry['permalink'] = unicode(item.link)

            entry['content'] = unicode(
                md.convert(item.summary))
            # entry['title'] = unicode(item.title)
            entry['context'] = {
                u'label': u'Read more',
                u'link': unicode(item.link)}
            entry['parsed'] = True
            # entry['raw'] = json.dumps(item)

        return self._format_parse_result(entry)


class TwitterParser():
    def __init__(self, db, feed_data):
        self.feed_data = feed_data
        self.db = db

        logger.debug(self.__class__.__name__ + ': Fetching data...')
        request = urllib.urlopen(
            feed_data['url'])

        self.data = json.load(request)
        logger.debug(self.__class__.__name__ + ': Done')

        self.index = 0

    def __iter__(self):
        return self

    def parse(self):
        pass

    def parse_tweet(self, content):
        return parse_tweet(
            links2html(content))

    def next(self):
        try:
            item = self.data[self.index]
            self.index += 1

            entry = self.db.FeedEntry()

            entry['guid'] = u'http://twitter.com/{0}/statuses/{1}'.format(
                item['user']['screen_name'],
                item['id'])

            entry['permalink'] = u'http://twitter.com/{0}/statuses/{1}'.format(
                item['user']['screen_name'],
                item['id'])

            entry['content'] = self.parse_tweet(
                item['text'])

            entry['source'] = {
                'name': item['user']['screen_name'],
                'link': u'http://twitter.com/{0}'.format(
                    item['user']['screen_name'])}

            #entry['raw'] = json.dumps(item)

            entry['parsed'] = True

            #entry.save()

            return entry
        except IndexError:
            raise StopIteration
