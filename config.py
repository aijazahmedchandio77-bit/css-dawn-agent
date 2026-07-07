"""
Central config. All secrets come from environment variables, which are
injected by GitHub Actions from repo secrets (Settings -> Secrets -> Actions).
Never hardcode real tokens/keys in this file.
"""
import os

ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID", "6345421988")

MODEL_NAME = "claude-sonnet-5"

# Dawn RSS feeds (official, stable, far more reliable than scraping the homepage HTML)
DAWN_EDITORIAL_FEED = "https://www.dawn.com/feeds/editorial"
DAWN_HOME_FEED = "https://www.dawn.com/feeds/home"
DAWN_PAKISTAN_FEED = "https://www.dawn.com/feeds/pakistan"
DAWN_WORLD_FEED = "https://www.dawn.com/feeds/world"

OUTPUT_DIR = "output"
