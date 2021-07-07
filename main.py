import os
os.system("sudo pip install pyTelegramBotAPI")
import telebot
import requests
import json

# Get Secrets from env
# TODO: secrets arent working
BOT_API = os.environ.get("BOT_API")
CHAT_ID = os.environ.get("CHAT_ID")
GH_TOKEN = os.environ.get("GH_TOKEN")
bot = telebot.TeleBot(BOT_API, parse_mode="MARKDOWN")


def send_mes(text):
    if text == "":
        return False
    return bot.send_message(CHAT_ID, text)


def update(repo):
    file_name = "repo/" + repo.replace("/", "_") + ".txt"
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
    file_name = "repo/" + repo.replace("/", "_") + ".txt"
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
                    new_commits.append(x['commit']['message'])
        message = ""
        for i in new_commits:
            message = message + str(i)
        return message


os.system("ls")


# Connect bot


if GH_TOKEN == "":
    print("Token not found")
else:
    print("Token found")

# Start of actual code
file = open("repo/roms.txt", "r")
repo = []
for line in file.readlines():
    print("Currently tracking : " + line)
    repo.append(line.replace("\n", ""))

for rom in repo:
    # Check if new
    result = get_diff(rom)
    if result != False:
        result.replace("_", "")
        result.replace("*", "")
        result.replace("`", "")
        result.replace("/", "")
        result.replace("|", "")
        result.replace("#", "")
        result.replace("]", "")
        result.replace("(", "")
        result.replace(")", "")
        result.replace("\\", "")
        result.strip("*")
        print(result)
        send_mes("Updating")
        send_mes("New commit for " + str(rom) + "\n" + result[:2000])
        os.system("cd repo")
        os.system("git add .")
        os.system("git commit -m \" Update SHAs for " + str(rom) + "\"" )
        os.system("cd ..")

os.system("cd repo")
os.system("git push https://geek0609: " + str(GH_TOKEN) + "@github.com/geek0609/rom-tracker master")