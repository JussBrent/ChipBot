import asyncio
from datetime import datetime

class RateLimiter:
    def __init__(self):
        self.request_count = 0
        self.window_start = datetime.now()
        self.last_request = datetime.now()
    
    async def wait_if_needed(self):
        await asyncio.sleep(0.1)
    
    def record_request(self):
        self.request_count += 1
        self.last_request = datetime.now()
