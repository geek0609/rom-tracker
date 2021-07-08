import os
import telebot
import sys
import requests
import json


def send_mes(text):
    if text == "":
        text = " "
    return bot.send_message(CHAT_ID, text)


BOT_API = sys.argv[2]
CHAT_ID = sys.argv[1]


bot = telebot.TeleBot(BOT_API, parse_mode="MARKDOWN")


send_mes("Sys Argv is working")