import os
os.system("sudo pip install pyTelegramBotAPI")
import telebot
import requests
import json


def send_mes(text):
    if text == "":
        return False
    return bot.send_message(CHAT_ID, text)


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
    print(differences)

    if len(list(differences)) == 0:
        print("No change")
        return False
    else:
        new_commits = []
        for different in differences:
            for x in converted:
                if x['sha'] == different:
                    print(x['commit']['message'], end="\n\n")
                    new_commits.append(x['commit']['message'])
        message = ""
        for i in new_commits:
            message = message + str(i)
        return message


# Get Secrets from env
BOT_API = os.environ.get("BOT_API")
CHAT_ID = os.environ.get("CHAT_ID")
GH_TOKEN = os.environ.get("GH_TOKEN")

# Connect bot
bot = telebot.TeleBot(BOT_API, parse_mode="MARKDOWN")

if GH_TOKEN == "":
    print("Token not found")
else:
    print("Token found")

# Start of actual code
file = open("roms.txt", "w+")
repo = []

for line in file.readlines():
    print("Currently tracking : " + line)
    repo.append(line)

for rom in repo:
    # Check if new
    if not get_diff(rom):
        send_mes("New commit for " + str(rom) + "\n" + get_diff(rom))
        os.system("git add .")
        os.system("git commit -m \" Update SHAs for " + str(rom) + "\"" )

os.system("git push https://geek0609: " + GH_TOKEN + "@github.com/geek0609/rom-tracker master")