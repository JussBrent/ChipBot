import json
import os

class AlertTracker:
    def __init__(self):
        self.sent_tweets = set()
        os.makedirs('data/logs', exist_ok=True)
    
    def mark_as_sent(self, tweet_id):
        self.sent_tweets.add(str(tweet_id))
    
    def is_already_sent(self, tweet_id):
        return str(tweet_id) in self.sent_tweets
