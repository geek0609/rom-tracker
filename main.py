import os
import telebot
import sys
import requests
import json


def send_mes(text):
    if text == "":
        text = " "
    return bot.send_message(CHAT_ID, text)


# Init telegram bot
BOT_API = sys.argv[2]
CHAT_ID = sys.argv[1]
bot = telebot.TeleBot(BOT_API, parse_mode="MARKDOWN")


def update(repo):
    file_name = repo.replace("/", "_") + ".txt"
    req = requests.get("https://api.github.com/repos/" + repo + "/commits").content
    converted = json.loads(req)
    shas = []
    for x in converted:
        shas.append(x['sha'])
    os.remove(file_name)
    with open(file_name, "w+") as f:
        for s in shas:
            f.write(str(s) + "\n")
    return True


def get_diff (repo):
    file_name = repo.replace("/", "_") + ".txt"
    req = requests.get("https://api.github.com/repos/" + repo + "/commits").content
    converted = json.loads(req)
    shas = []
    for x in converted:
        shas.append(x['sha'])

    prev_sha = []
    with open(file_name, "w+") as f:
        for line in f:
            prev_sha.append(str(line.strip()))

    first_set = set(shas)
    sec_set = set(prev_sha)
    differences = (first_set - sec_set).union(sec_set - first_set)
    return list(differences)


# Start of actual code
file = open("roms.txt", "r")
repo = file.readlines()
for rom in repo:
    # Check if new
    rom = rom.replace("\n", "")
    result = get_diff(rom)
    if result:
        message = "New commit(s) in " + str(rom)
        number = 0
        for commit in result:
            if number <= 10:
                message = message + "https://github.com/" + str(rom) + "/commit/" + str(commit) + "\n"
                number = number + 1
            else:
                break
        send_mes(message)
        update(rom)
