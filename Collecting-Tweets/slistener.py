# import packages
from tweepy.streaming import StreamListener
import json
import time
import sys
# inherit from StreamListener class
class SListener(StreamListener):
    def __init__(self, api = None, fprefix = 'streaming_retweet'):
        # define the filename with time as prefix
        self.api = api or API()
        self.counter = 0
        self.fprefix = fprefix
        self.output  = open('%s_%s.json' % (self.fprefix, time.strftime('%Y%m%d-%H%M%S')), 'w')
    def on_data(self, data):
        if  'in_reply_to_status' in data:
            self.on_status(data)
        elif 'delete' in data:
            delete = json.loads(data)['delete']['status']
            if self.on_delete(delete['id'], delete['user_id']) is False:
                return False
        elif 'limit' in data:
            if self.on_limit(json.loads(data)['limit']['track']) is False:
                return False
        elif 'warning' in data:
            warning = json.loads(data)['warnings']
            print("WARNING: %s" % warning['message'])
            return
    def on_status(self, status):
        # if the number of tweets reaches 10000
        # create a new file
        self.output.write(status)
        #tweet = status._json
        #json.dump(tweet, self.output)
        #self.output.write('\n')
        self.counter += 1 
        if self.counter >= 10000:
            print(self.counter)
            self.output.close()
            self.output  = open('%s_%s.json' % (self.fprefix, time.strftime('%Y%m%d-%H%M%S')), 'w')
            self.counter = 0
            
        return
    def on_delete(self, status_id, user_id):
        print("Delete notice")
        return
    def on_limit(self, track):
        print("WARNING: Limitation notice received, tweets missed: %d" % track)
        return
    def on_error(self, status_code):
        print('Encountered error with status code:', status_code)
        return 
    def on_timeout(self):
        print("Timeout, sleeping for 60 seconds...")
        time.sleep(60)
        return 
