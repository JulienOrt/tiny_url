import os

from tiny_url.settings.settings import Settings

env_file_path = os.path.join(os.path.dirname(__file__), "settings", ".env")
APP_SETTINGS = Settings(_env_file=env_file_path)
