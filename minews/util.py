import re


from jinja2 import Environment, PackageLoader


TEMPLATE_ENV = Environment(
    loader=PackageLoader('minews', 'templates'),
    autoescape=False)

def get_template(*args):
    return TEMPLATE_ENV.get_template(*args)

def parse_tweet(tweet):
    hash_regex = re.compile(r'#[0-9a-zA-Z+_]*',re.IGNORECASE) 
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
