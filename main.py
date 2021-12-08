import vestalbot
from webserver import keep_alive
import os

keep_alive()
TOKEN = os.environ.get("DISCORD_BOT_SECRET")
vestalbot.client.run(TOKEN)