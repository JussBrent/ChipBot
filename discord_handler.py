import discord
import asyncio

class DiscordHandler:
    def __init__(self, bot):
        self.bot = bot
    
    async def send_promotion_alert(self, tweet):
        embed = discord.Embed(
            title="🌯 Chipotle Promotion Alert!",
            description=tweet.text,
            color=0x8B4513,
            timestamp=tweet.created_at
        )
        embed.add_field(name="Tweet Link", value=f"https://twitter.com/ChipotleTweets/status/{tweet.id}", inline=False)
        
        # Send to configured channels
        from config import CHANNEL_IDS
        for channel_id in CHANNEL_IDS:
            try:
                channel = self.bot.get_channel(channel_id)
                if channel:
                    await channel.send(embed=embed)
                    await asyncio.sleep(0.1)
            except Exception as e:
                print(f"Error sending to channel {channel_id}: {e}")
    
    async def send_test_alert(self, channel):
        embed = discord.Embed(title="🌯 Test Alert", description="ChipBot is working!", color=0x8B4513)
        await channel.send(embed=embed)
