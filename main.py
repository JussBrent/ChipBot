import discord
from discord.ext import commands, tasks
import asyncio
import logging
from config import *
from twitter_monitor import TwitterMonitor
from discord_handler import DiscordHandler
from alert_tracker import AlertTracker

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('data/logs/bot.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class ChipBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(command_prefix='!', intents=intents)
        
        self.twitter_monitor = TwitterMonitor()
        self.discord_handler = DiscordHandler(self)
        self.alert_tracker = AlertTracker()
        
    async def setup_hook(self):
        """Called when the bot is starting up"""
        self.monitor_tweets.start()
        logger.info("ChipBot setup complete")
    
    @tasks.loop(seconds=MONITORING_INTERVAL)
    async def monitor_tweets(self):
        """Main monitoring loop"""
        try:
            new_promotions = await self.twitter_monitor.check_for_promotions()
            
            for tweet in new_promotions:
                if not self.alert_tracker.is_already_sent(tweet.id):
                    await self.discord_handler.send_promotion_alert(tweet)
                    self.alert_tracker.mark_as_sent(tweet.id)
                    logger.info(f"Sent alert for tweet {tweet.id}")
                    
        except Exception as e:
            logger.error(f"Monitoring error: {e}")
    
    @monitor_tweets.before_loop
    async def before_monitor_tweets(self):
        """Wait until the bot is ready before starting monitoring"""
        await self.wait_until_ready()
        logger.info("Starting tweet monitoring...")
    
    async def on_ready(self):
        """Called when the bot has successfully connected to Discord"""
        logger.info(f'{self.user} has connected to Discord!')
        logger.info(f'Serving {len(self.guilds)} servers')
        
        # Log connected servers
        for guild in self.guilds:
            logger.info(f'Connected to: {guild.name} (ID: {guild.id})')
    
    async def on_command_error(self, ctx, error):
        """Handle command errors"""
        logger.error(f"Command error: {error}")
        await ctx.send("An error occurred while processing your command.")

# Bot commands
@commands.command(name='status')
async def status(ctx):
    """Check bot status"""
    embed = discord.Embed(
        title="ChipBot Status",
        description="Bot is running and monitoring Chipotle tweets!",
        color=0x8B4513
    )
    embed.add_field(name="Servers", value=len(ctx.bot.guilds), inline=True)
    embed.add_field(name="Monitoring", value="Active", inline=True)
    await ctx.send(embed=embed)

@commands.command(name='test')
async def test_alert(ctx):
    """Test the alert system (admin only)"""
    if not ctx.author.guild_permissions.administrator:
        await ctx.send("You need admin permissions to use this command.")
        return
    
    await ctx.bot.discord_handler.send_test_alert(ctx.channel)

if __name__ == "__main__":
    import os
    from dotenv import load_dotenv
    
    load_dotenv()
    
    bot = ChipBot()
    bot.add_command(status)
    bot.add_command(test_alert)
    
    try:
        bot.run(os.getenv('DISCORD_TOKEN'))
    except Exception as e:
        logger.error(f"Failed to start bot: {e}")