import minews.parsers
import feedparser

class RSSIterator:
    def __init__(self, db, feed_data):
        self.data = feedparser.parse(
            feed_data['url'])


        self.db = db

        self.feed_data = feed_data

        self.index = 0

        self._set_parser_object()

    def __iter__(self):
        return self

    def _set_parser_object(self):
        self.parser_object = minews.parsers.RSSParser

    def next(self):
        try:
            item = self.data.entries[self.index]
            self.index += 1

            entry, was_parsed, existed = self.parser_object(self.db, item).parse()

            if was_parsed:
                entry['project'] = unicode(self.feed_data['project'])
                entry['type'] = unicode(self.feed_data['type'])
                entry['source'] = {
                    'name': unicode(self.data.feed.title),
                    'link': unicode(self.data.feed.link)}

                if existed:
                    entry.update()
                else:
                    entry.save()

            return entry, was_parsed, existed
        except IndexError:
            raise StopIteration


class GoogleGroupsRSSIterator(RSSIterator):
    def next(self):
        try:
            item = self.data.entries[self.index]
            self.index += 1

            entry, was_parsed, existed = self.parser_object(self.db, item).parse()

            if was_parsed:
                entry['project'] = unicode(self.feed_data['project'])
                entry['type'] = unicode(self.feed_data['type'])
                entry['source'] = {
                    'name': unicode(self.data.feed.title),
                    'link': unicode(self.data.feed.id)}

                if existed:
                    entry.update()
                else:
                    entry.save()

            return entry, was_parsed, existed
        except IndexError:
            raise StopIteration

class IdenticaRSSIterator(RSSIterator):
    def _set_parser_object(self):
        self.parser_object = minews.parsers.IdenticaRSSParser


class DiasporaAtomIterator(RSSIterator):
    def _set_parser_object(self):
        self.parser_object = minews.parsers.DiasporaAtomParser
