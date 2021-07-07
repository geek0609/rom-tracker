import os

GH_TOKEN = ""
BOT_API = os.environ.get("BOT_API")
CHAT_ID = os.environ.get("CHAT_ID")
GH_TOKEN = os.environ.get("GH_TOKEN")


print(BOT_API)
print(CHAT_ID)
if GH_TOKEN == "":
    print("Token not found")
else:
    print("Token found")