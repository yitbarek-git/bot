import os

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

BOT_TOKEN = os.getenv("BOT_TOKEN", "").strip()
ADMIN_ID_RAW = os.getenv("ADMIN_ID", "0").strip()
GROUP_ID_RAW = os.getenv("GROUP_ID", "0").strip()

try:
    ADMIN_ID = int(ADMIN_ID_RAW) if ADMIN_ID_RAW else 0
except ValueError:
    ADMIN_ID = 0

try:
    GROUP_ID = int(GROUP_ID_RAW) if GROUP_ID_RAW else 0
except ValueError:
    GROUP_ID = 0

# Database Configuration (SQLite)
# Default is 'aplus_academy.db' in the root directory
DB_PATH = os.getenv("DB_PATH", "aplus_academy.db").strip()

# Webhook Configuration (Vercel)
WEBHOOK_URL = os.getenv("WEBHOOK_URL", "").strip()
WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET", "").strip()

# Bot Constants
DEFAULT_COURSE = "freshman"
DEFAULT_LANGUAGE = "en"
SUPPORTED_LANGUAGES = ["en", "am"]
