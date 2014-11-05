import tweepy, io, json

from getpass import getpass


    
# Consumer keys and access tokens, used for OAuth
consumer_key = '5NDK4avsdv9Jx1B7pFUek8paj'
consumer_secret = 'AQUNsFSJOviqGWBof8qEZ2OlIleayni2KLU9dSVY5oodY0XR03'
access_token = '2691189445-LhB8bc6NmQiamVWEYjkvlNxPfYdp5lkiLiZ1S22'
access_token_secret = 'bgC7iUbqXAvpsfEX4pQgp94FGG7Isj9RwD5Squ4MznebC'

 
# OAuth process, using the keys and tokens
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

# Creation of the actual interface, using authentication
api = tweepy.API(auth)

user_file = open('usertimeline.txt','a')

for tweet in tweepy.Cursor(api.user_timeline, id="ev", include_rts=False).items(10):
    print '%s --- aka @ %s --- at %s' % (tweet.author.name.encode('utf8'), tweet.author.screen_name.encode('utf8'), tweet.created_at)
    print "\n"
    print "Tweet:", tweet.text.encode('utf8')
    print "\n"
    tweet_text = tweet.text.encode('utf8')
    words = ''.join(c if c.isalnum() else ' ' for c in tweet_text).split()
    print 'Length: %s   Words:  %s' % (len( tweet_text), len(words))
    print 'Retweets: %s   Favorites: %s' % (tweet.retweet_count, tweet.favorite_count)
    print "\n"
    print 'Location? %s    Time Zone? %s    Geo-coding?  %s' % (tweet.user.location.encode('utf8'), tweet.user.time_zone, tweet.geo)
    print "\n"
    print "-------------------------------"
    print "\n"
    user_file.write(tweet_text + '\n')