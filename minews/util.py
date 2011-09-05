import re


from jinja2 import Environment, PackageLoader


TEMPLATE_ENV = Environment(
    loader=PackageLoader('minews', 'templates'),
    autoescape=False)

def get_template(*args):
    return TEMPLATE_ENV.get_template(*args)

def links2html(string):
#    link_regex = re.compile(r'(?<url>(((ht|f)tp(s?))\://)?((([a-zA-Z0-9_\-]{2,}\.)+[a-zA-Z]{2,})|((?:(?:25[0-5]|2[0-4]\d|[01]\d\d|\d?\d)(?(\.?\d)\.)){4}))(:[a-zA-Z0-9]+)?(/[a-zA-Z0-9\-\._\?\,\'/\\\+&amp;%\$#\=~]*)?)')
    link_regex = re.compile(r'((https?://|www\.)[^ ,\'">\]\)]+\.[^\. ,\'\">\]\)]{2,6})(\s|$)')

    for match in link_regex.finditer(string):
        print("\n=====\n" + str(match.groups()) + "\n=====\n")

    return string

def parse_tweet(tweet):
    hash_regex = re.compile(r'#[^ ]*',re.IGNORECASE) 
    user_regex = re.compile(r'@[0-9a-zA-Z+_]*',re.IGNORECASE)

    for tt in user_regex.finditer(tweet):
        url_tweet = tt.group(0).replace('@','')
        tweet = tweet.replace(tt.group(0),
                              '<a href="http://twitter.com/'+
                              url_tweet+'" title="'+
                              tt.group(0)+'">'+
                              tt.group(0)+'</a>')

    for th in hash_regex.finditer(tweet):
        url_hash = th.group(0).replace('#','%23')
        if len ( th.group(0) ) > 2:
            tweet = tweet.replace(th.group(0),
                                  '<a href="http://search.twitter.com/search?q='+
                                  url_hash+'" title="'+
                                  th.group(0)+'">'+
                                  th.group(0)+'</a>');

    return tweet
