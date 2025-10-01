# ChipBot

Discord bot that monitors Chipotle's Twitter for promotion codes and sends alerts to Discord servers.

## Features
- Real-time Twitter monitoring
- <2s alert delay
- Serves 150+ users across 5 servers
- API rate limiting and error handling

## Setup
1. Clone the repository
2. Copy `.env.example` to `.env` and add your API keys
3. Install dependencies: `pip install -r requirements.txt`
4. Run: `python3 main.py`

## Tech Stack
- Python 3.9+
- Discord.py
- Tweepy (Twitter API)
- Pandas
