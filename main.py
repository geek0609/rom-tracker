import os
os.system("sudo pip install pyTelegramBotAPI")
import telebot


def send_mes(text):
    if text == "":
        text = " "
    return bot.send_message(CHAT_ID, text)

GH_TOKEN = ""
BOT_API = os.environ.get("BOT_API")
CHAT_ID = os.environ.get("CHAT_ID")
GH_TOKEN = os.environ.get("GH_TOKEN")


bot = telebot.TeleBot(BOT_API, parse_mode="MARKDOWN")

print(CHAT_ID)
if GH_TOKEN == "":
    print("Token not found")
else:
    print("Token found")
os.system("sudo git clone https://github.com/ProjectSakura/android track && cd track && sudo git log | tee log.txt")
file = open("track/log.txt")
message = ""
for line in file.readlines():
    message = message + line.strip("/n")

message = message.replace("_" "")
message = message.replace("*" "")
message = message.replace("`" "")
message = message.replace("[" "")
message = message.replace("]" "")
send_mes(message[:2000])
send_mes("It is working")