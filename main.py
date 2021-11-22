import thiccbot
from webserver import keep_alive
import os

keep_alive()
TOKEN = os.environ.get("DISCORD_BOT_SECRET")
thiccbot.client.run(TOKEN)