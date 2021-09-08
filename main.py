#!/usr/bin/env python
#
# Python code which automatically sends a Message in a Telegram Channel if any new commit is found in the specified repos
# See README.MD for more
#
# Copyright (C) 2021 Ashwin DS <astroashwin@outlook.com>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation;
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, see <http://www.gnu.org/licenses/>.

import os
import telebot
import sys
import requests
import json
import time
import random


def send_mes(text):
    if text == "":
        text = "NO/EMPTY TEXT GIVEN TO SEND"
    return bot.send_message(CHAT_ID, text, disable_web_page_preview=True)
# Send a message

timeout = random.randint(0,60)

for i in range(timeout):
    print ("Waiting for " + str(timeout) + " before starting, this random wait helps avoid conflicts during push at same time\n\nTime remaining : " + str(timeout - i))
    time.sleep(1)

# Init telegram bot
BOT_API = sys.argv[2]
CHAT_ID = sys.argv[1]
REPO_LIST = sys.argv[3]
bot = telebot.TeleBot(BOT_API, parse_mode="HTML")


def update(repo, converted):
    file_name = repo.replace("/", "_") + ".txt"
    # Sends a request to github api to get the latest commits
    # req = requests.get("https://api.github.com/repos/" + repo + "/commits").content
    # converted = json.loads(req)
    shas = []
    for x in converted:
        shas.append(x['sha'])
    if os.path.isfile(file_name):
        os.remove(file_name)
    with open(f'roms/{file_name}', "w+") as f:
        for s in shas:
            f.write(str(s) + "\n")
    return True


def get_diff (repo, converted):
    file_name = repo.replace("/", "_") + ".txt"
    # req = requests.get("https://api.github.com/repos/" + repo + "/commits").content
    # converted = json.loads(req)
    # Fetches new commits (if any) from API
    shas = []
    for x in converted:
        shas.append(x['sha'])
    # Reads previous commits from where it is stored
    prev_sha = []
    file = open("roms/" + file_name, "r")
    for line in file.readlines():
        prev_sha.append(line.replace("\n", ""))
    print(shas)
    print(prev_sha)
    if shas == prev_sha:
        return False
    first_set = set(shas)
    sec_set = set(prev_sha)
    differences = first_set - sec_set
    # TODO: Remove this useless logic
    if len(list(differences)) == 0:
        print("No change")
        return False
    else:
        return list(differences)


# Start of actual code
file = open(REPO_LIST, "r")
repo = file.readlines()
# Read roms from roms.txt
for rom in repo:
    rom = rom.replace("\n", "")
    file_name = rom.replace("/", "_") + ".txt"
    req = requests.get("https://api.github.com/repos/" + rom + "/commits").content
    converted = json.loads(req)
    if os.path.isfile("roms/" + file_name):
        print(file_name + " Exists")
    else:
        # In case the file is just added to the list, it needs to be updated first,
        # before it can compare for new commits
        print("Not exist")
        update(rom, converted)
    # Check if new commit
    result = get_diff(rom, converted)
    # I can use if result but i choose to do this for sake of my understanding
    if result != False:
        # need to be in this format <a href="http://www.example.com/">inline URL</a>
        message = "New commit(s) in \n" + "<a href=\"" + "https://github.com/" + str(rom) + "\">" + str(rom) + "</a>\n\n"
        number = 1
        result.reverse() # Else it shows way older commits first
        for commit in result:
            if number <= 10:
                # need to be in this format <a href="http://www.example.com/">inline URL</a>
                message = message + "<a href=\"" + "https://github.com/" + str(rom) + "/commit/" + str(commit) + "\">Click me for commit " + str(number) + "</a>\n"
                number = number + 1
            else:
                break
        send_mes(message + "\n@rom_tracker | #" + str(rom).split("/")[0].replace("-", "_"))
        time.sleep(30)
        # to not spam api 
        update(rom, converted)
    else:
        print("All up to date") # For Logging purposes