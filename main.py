#!/usr/bin/env python
#
# Python code which automatically sends a Message in a Telegram Channel if
# any new commit is found in the specified repos See README.MD for more
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
    return bot.send_message(CHAT_ID, text or "NO/EMPTY TEXT GIVEN TO SEND")


# Send a message

timeout = random.randint(0, 60)

for i in range(timeout):
    print(
        f"Waiting for {timeout}s before starting, this random wait helps avoid "
        f"conflicts during push at same time\n\nTime remaining : {timeout - i} "
    )

# Init telegram bot
CHAT_ID = sys.argv[1]
BOT_API = sys.argv[2]
REPO_LIST = sys.argv[3]
bot = telebot.TeleBot(BOT_API)


def update(repo, converted):
    file_name = repo.replace("/", "_") + ".txt"
    # Sends a request to github api to get the latest commits
    # req = requests.get(f"https://api.github.com/repos/{repo}/commits").content
    # converted = json.loads(req)
    sha_list = '\n'.join(map(str, (x['sha'] for x in converted)))

    if os.path.isfile(file_name):
        os.remove(file_name)

    with open(f'roms/{file_name}', "w+") as f:
        f.write(sha_list)

    return True


def get_diff(repo, converted):
    file_name = repo.replace("/", "_") + ".txt"

    # req = requests.get(f"https://api.github.com/repos/{repo}/commits").content
    # converted = json.loads(req)

    # Fetches new commits (if any) from API
    sha_list = [x['sha'] for x in converted]

    # Reads previous commits from where it is stored
    with open(file_name) as f:
        prev_sha = [line.replace("\n", "") for line in f.read().splitlines()]

    print(sha_list)
    print(prev_sha)

    if sha_list == prev_sha:
        return False

    differences = set(sha_list) - set(prev_sha)
    print(differences)

    # TODO: Remove this useless logic

    if len(list(differences)) != 0:
        return list(differences)
    print("No change")

    return False


def send_rom(rom):
    file_name = rom.replace("/", "_") + ".txt"

    req = requests.get("https://api.github.com/repos/{rom}/commits").content
    converted = json.loads(req)

    if os.path.isfile(file_name):
        print(file_name, "Exists")

    else:
        # In case the file is just added to the list,
        # it needs to be updated first,
        # before it can compare for new commits
        print("Not exist")
        update(rom, converted)

    # Check if new commit
    result = get_diff(rom, converted)

    if not result:
        print("All up to date")  # For Logging purposes
        return

    # need to be in this format :
    # <a href="http://www.example.com/">inline URL</a>

    result.reverse()  # Else it shows way older commits first
    message = f"New commit(s) in \n<a href=\"https://github.com/{rom}\">{rom}</a>\n\n\n"

    for number, commit in enumerate(result):
        if number > 10:
            break

    # need to be in this format :
    # <a href="http://www.example.com/">inline URL</a>
    message += f"<a href=\"https://github.com/{rom}/commit/{commit}\">Click me for commit {number}</a>\n"

    send_mes(message)
    time.sleep(30)
    # to not spam api
    update(rom, converted)


# Start of actual code
def main():
    with open(REPO_LIST) as f:
        repo = f.read().splitlines()

    # Read roms from roms.txt
    for rom in repo:
        send_rom(rom)


if __name__ == '__main__':
    main()
