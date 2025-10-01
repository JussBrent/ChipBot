#!/usr/bin/env python3
import os

print("Checking files...")
files = ['main.py', 'config.py', 'twitter_monitor.py', 'rate_limiter.py', 'alert_tracker.py', 'discord_handler.py', '.env']
for f in files:
    print(f"{f}: {'✅' if os.path.exists(f) else '❌ MISSING'}")

print("\nChecking directories...")
dirs = ['data', 'data/logs']
for d in dirs:
    print(f"{d}: {'✅' if os.path.exists(d) else '❌ MISSING'}")
