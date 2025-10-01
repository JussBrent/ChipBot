# Discord Configuration
CHANNEL_IDS = [
    123456789012345678,  # Server 1 - General alerts
    234567890123456789,  # Server 2 - Promotions
    345678901234567890,  # Server 3 - Deals
    456789012345678901,  # Server 4 - Community
    567890123456789012,  # Server 5 - Bot testing
]

# Twitter Configuration
CHIPOTLE_USERNAME = "ChipotleTweets"
CHIPOTLE_USER_ID = "141341662"

# Search query for Chipotle promotion tweets
SEARCH_QUERY = "from:ChipotleTweets (code OR promo OR free OR deal OR discount OR bogo OR offer) -is:retweet -is:reply"

# Monitoring settings
MONITORING_INTERVAL = 30  # seconds - Check every 30 seconds
MAX_TWEETS_PER_CHECK = 10  # Number of recent tweets to check
ALERT_DELAY_THRESHOLD = 2  # seconds - Target alert delay

# Promotion keywords to look for
PROMOTION_KEYWORDS = [
    'code',
    'promo',
    'free',
    'deal',
    'discount',
    'bogo',
    'buy one get one',
    'offer',
    'save',
    'percent off',
    '%',
    'limited time',
    'expires',
    'coupon'
]

# Rate limiting settings
TWITTER_RATE_LIMIT = 300  # requests per 15-minute window
RATE_LIMIT_WINDOW = 900   # 15 minutes in seconds
REQUEST_DELAY = 1         # seconds between requests

# Discord embed settings
EMBED_COLOR = 0x8B4513  # Chipotle brown color
BOT_EMOJI = "🌯"

# File paths
SENT_ALERTS_FILE = "data/sent_alerts.json"
LOG_FILE = "data/logs/bot.log"

# Error handling
MAX_RETRIES = 3
RETRY_DELAY = 5  # seconds

# Discord message settings
MAX_EMBED_DESCRIPTION_LENGTH = 2048
THUMBNAIL_URL = "https://logo.clearbit.com/chipotle.com"