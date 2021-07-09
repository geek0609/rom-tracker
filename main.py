import os
import telebot
import sys
import requests
import json
import time


def send_mes(text):
    if text == "":
        text = " "
    return bot.send_message(CHAT_ID, text)


# Init telegram bot
BOT_API = sys.argv[2]
CHAT_ID = sys.argv[1]
bot = telebot.TeleBot(BOT_API, parse_mode="HTML")


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
    file = open(file_name, "r")
    for line in file.readlines():
        prev_sha.append(line.replace("\n", ""))

    print(shas)
    print(prev_sha)
    if shas == prev_sha:
        return False

    first_set = set(shas)
    sec_set = set(prev_sha)
    differences = first_set - sec_set
    if len(list(differences)) == 0:
        print("No change")
        return False
    else:
        return list(differences)


# Start of actual code
file = open("roms.txt", "r")
repo = file.readlines()
for rom in repo:
    # Check if new
    rom = rom.replace("\n", "")
    result = get_diff(rom)
    if result != False:
        message = "New commit(s) in " + str(rom) + "\n\n"
        number = 1
        result.reverse()
        for commit in result:
            if number <= 10:
                # need to be in this format <a href="http://www.example.com/">inline URL</a>
                message = message + "<a href=\"" + "https://github.com/" + str(rom) + "/commit/" + str(commit) + "\">Click me for commit " + str(number) + "</a>\n"
                number = number + 1
            else:
                break
        send_mes(message)
        time.sleep(30)
        # to not spam api 
        update(rom)
        os.system("ls")
    else:
        print("All up to date")