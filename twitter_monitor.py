import tweepy
import asyncio
import logging
from datetime import datetime, timezone
from typing import List, Optional
from config import *
from rate_limiter import RateLimiter
import os

logger = logging.getLogger(__name__)

class TwitterMonitor:
    def __init__(self):
        self.setup_twitter_api()
        self.rate_limiter = RateLimiter()
        self.last_check_time = datetime.now(timezone.utc)
        
    def setup_twitter_api(self):
        """Initialize Twitter API clients"""
        try:
            # Twitter API v2 client (primary)
            self.client = tweepy.Client(
                bearer_token=os.getenv('TWITTER_BEARER_TOKEN'),
                consumer_key=os.getenv('TWITTER_API_KEY'),
                consumer_secret=os.getenv('TWITTER_API_SECRET'),
                access_token=os.getenv('TWITTER_ACCESS_TOKEN'),
                access_token_secret=os.getenv('TWITTER_ACCESS_TOKEN_SECRET'),
                wait_on_rate_limit=True
            )
            
            # Verify credentials
            user = self.client.get_me()
            logger.info(f"Twitter API authenticated as: {user.data.username}")
            
        except Exception as e:
            logger.error(f"Failed to setup Twitter API: {e}")
            raise
    
    async def check_for_promotions(self) -> List:
        """Check for new promotional tweets from Chipotle"""
        try:
            await self.rate_limiter.wait_if_needed()
            
            # Search for recent tweets
            tweets = await self._search_recent_tweets()
            
            if not tweets:
                return []
            
            # Filter for promotional content
            promotional_tweets = []
            for tweet in tweets.data or []:
                if self._is_promotional_tweet(tweet):
                    promotional_tweets.append(tweet)
                    logger.info(f"Found promotional tweet: {tweet.id}")
            
            return promotional_tweets
            
        except tweepy.TooManyRequests:
            logger.warning("Twitter rate limit hit")
            return []
        except Exception as e:
            logger.error(f"Error checking for promotions: {e}")
            return []
    
    async def _search_recent_tweets(self):
        """Search for recent tweets using Twitter API v2"""
        try:
            # Use asyncio to make the API call non-blocking
            loop = asyncio.get_event_loop()
            tweets = await loop.run_in_executor(
                None,
                lambda: self.client.search_recent_tweets(
                    query=SEARCH_QUERY,
                    max_results=MAX_TWEETS_PER_CHECK,
                    tweet_fields=['created_at', 'public_metrics', 'context_annotations', 'source'],
                    user_fields=['username', 'name', 'verified'],
                    expansions=['author_id']
                )
            )
            
            self.rate_limiter.record_request()
            return tweets
            
        except Exception as e:
            logger.error(f"Error searching tweets: {e}")
            raise
    
    def _is_promotional_tweet(self, tweet) -> bool:
        """Check if a tweet contains promotional content"""
        tweet_text = tweet.text.lower()
        
        # Check for promotion keywords
        has_keywords = any(keyword.lower() in tweet_text for keyword in PROMOTION_KEYWORDS)
        
        # Additional checks
        has_code_pattern = any(word in tweet_text for word in ['code:', 'use code', 'promo code'])
        has_discount_pattern = any(word in tweet_text for word in ['%', 'percent', 'off', '$'])
        has_urgency = any(word in tweet_text for word in ['limited', 'expires', 'today only', 'hurry'])
        
        # Only consider recent tweets (within last hour for real-time alerts)
        tweet_age = datetime.now(timezone.utc) - tweet.created_at
        is_recent = tweet_age.total_seconds() < 3600  # 1 hour
        
        return (has_keywords or has_code_pattern or has_discount_pattern) and is_recent
    
    async def get_tweet_details(self, tweet_id: str) -> Optional[dict]:
        """Get detailed information about a specific tweet"""
        try:
            await self.rate_limiter.wait_if_needed()
            
            loop = asyncio.get_event_loop()
            tweet = await loop.run_in_executor(
                None,
                lambda: self.client.get_tweet(
                    tweet_id,
                    tweet_fields=['created_at', 'public_metrics', 'source', 'lang'],
                    user_fields=['username', 'name', 'verified', 'profile_image_url'],
                    expansions=['author_id']
                )
            )
            
            self.rate_limiter.record_request()
            
            if tweet.data:
                return {
                    'id': tweet.data.id,
                    'text': tweet.data.text,
                    'created_at': tweet.data.created_at,
                    'metrics': tweet.data.public_metrics,
                    'source': tweet.data.source,
                    'author': tweet.includes['users'][0] if tweet.includes else None
                }
            
            return None
            
        except Exception as e:
            logger.error(f"Error getting tweet details: {e}")
            return None
    
    def get_tweet_url(self, tweet_id: str) -> str:
        """Generate Twitter URL for a tweet"""
        return f"https://twitter.com/{CHIPOTLE_USERNAME}/status/{tweet_id}"