#!/usr/bin/python
# -*- coding: utf-8 -*-

FEEDS = [{'url': 'http://groups.google.com/group/unhosted/feed/atom_v1_0_topics.xml?num=50&pli=1',
          'type': 'googlegroups-rss',
          'project': 'unhosted'},
         {'url': 'http://diasporial.com/feed',
          'type': 'rss',
          'project': 'diaspora'},
         {'url': 'http://mediagoblin.org/news/index.xml',
          'type': 'rss',
          'project': 'mediagoblin'},
         {'url': 'https://joindiaspora.com/public/owncloud.atom',
          'type': 'diaspora-atom',
          'project': 'owncloud'},
         {'url': 'http://owncloudtest.blogspot.com/feeds/posts/default',
          'type': 'rss',
          'project': 'owncloud'},]

CONFIG = dict(
    entry_max_length=500)

PROJECTS = [
    dict(
        name=u'MediaGoblin',
        handle=u'mediagoblin',
        description=u'''
      <ul> 
        <li>The perfect place for your media!</li> 
        <li>A place for people to collaborate and show off original and derived creations!</li> 
        <li>Free, as in freedom. (We’re a <a href="http://gnu.org">GNU</a> project, after all.)</li> 
        <li>Aiming to make the world a better place through decentralization and (eventually, coming soon!) federation!</li> 
        <li>Built for extensibility.  (Multiple media types coming soon to the software, including video support!)</li> 
        <li>Powered by people like you.  (<a href="http://mediagoblin.org/pages/join.html">You can help us improve this software!</a>)</li> 
      </ul>''',
        logo_url=u'/static/img/mediagoblin-100.png',
        links={
            u'Website': u'http://mediagoblin.org',
            u'Tracker': u'http://bugs.foocorp.net/projects/mediagoblin',
            u'Wiki': u'http://wiki.mediagoblin.org'},
        feeds=[
            dict(
                url=u'https://gitorious.org/mediagoblin/mediagoblin/commits/master/feed.atom',
                type=u'gitorious-atom',
                audience=u'advanced'),
            dict(
                url=u'http://mediagoblin.org/news/index.xml',
                type=u'rss',
                audience=u'general')]),
    dict(
        name=u'ownCloud',
        handle=u'owncloud',
        description=u'ownCloud description...',
        logo_url=u'/static/img/owncloud-100.png',
        links={
            u'Website': u'http://mediagoblin.org',
            u'Tracker': u'http://bugs.foocorp.net/projects/mediagoblin',
            u'Wiki': u'http://wiki.mediagoblin.org'},
        feeds=[
            dict(
                url=u'https://gitorious.org/owncloud/owncloud/commits/master/feed.atom',
                type=u'gitorious-atom',
                audience=u'advanced'),
            dict(
                url=u'https://joindiaspora.com/public/owncloud.atom',
                type=u'diaspora-atom',
                audience=u'general')]),
    dict(
        name=u'Unhosted',
        handle=u'unhosted',
        description=u'''Unhosted is a project promoting and constructing the decentralized web''',
        logo_url=u'/static/img/unhosted-100.png',
        links={
            u'Website': u'http://unhosted.org',
            u'GitHub': u'http://github.com/unhosted'},
        feeds=[
            dict(
                url=u'https://github.com/unhosted/unhosted/commits/devel.atom',
                type=u'github-atom',
                audience=u'advanced'),
            dict(
                url=u'http://groups.google.com/group/unhosted/feed/atom_v1_0_topics.xml?num=50',
                type=u'googlegroups-rss',
                audience=u'general'),
            dict(
                url=u'http://identi.ca/api/statuses/user_timeline/311670.atom',
                type=u'identica-atom',
                audience=u'general')]),
    dict(
        name=u'Diaspora',
        handle=u'diaspora',
        description=u'''Diaspora (stylized DIASPORA*) is a free personal web server[3] that implements a distributed social networking service, providing a decentralized alternative to social network services like Facebook''',
        logo_url=u'/static/img/diaspora-100.png',
        links={
            u'Website': u'http://joindiaspora.com',},
        feeds=[
            dict(
                url=u'https://github.com/diaspora/diaspora/commits/devel.atom',
                type=u'github-atom',
                audience=u'advanced'),
            dict(
                url=u'https://joindiaspora.com/public/diasporahq.atom',
                type=u'diaspora-atom',
                audience=u'general'),
            dict(
                url=u'http://diasporial.com/feed',
                type=u'rss',
                audience=u'general')])]
