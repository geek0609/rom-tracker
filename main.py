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
from telegraph import Telegraph



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
tgraph = Telegraph()
tgraph.create_account(short_name="ROM-Tracker BOT")

open("Failing" + REPO_LIST + ".log", "w+").close()
LogFile = open("Failing" + REPO_LIST + ".log", "a")

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
    try:
        for x in converted:
            shas.append(x['sha'])
    except:
        LogFile.write( repo + "\n")
        return False
    # Reads previous commits from where it is stored
    prev_sha = []
    file = open("roms/" + file_name, "r")
    for line in file.readlines():
        prev_sha.append(line.replace("\n", ""))
    print(shas)
    print(prev_sha)
    reversed_sha = shas
    reversed_sha.reverse()
    if reversed_sha[shas.__len__()-1] in prev_sha:
        return False
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
    if rom == "\n" or rom == "" or rom == " " or rom.startswith("#"):
        continue
    rom = rom.replace("\n", "")
    file_name = rom.replace("/", "_") + ".txt"
    req = requests.get("https://api.github.com/repos/" + rom + "/commits?per_page=100").content
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
        telegraph_title = "New commit(s) in \n" + str(rom) + ""
        telegraph_commit_content = ["",]
        telegraph_page = 0
        telegraph_commit_content[0] = "<h4>GitHub Repository Link: <a href=\"https://github.com/" + \
                                       str(rom) + "\">" + str(rom) + "</a> </h4> \n"
        number = 1
        result.reverse() # Else it shows way older commits first
        for commit in result:
            if number <= 70:
                # need to be in this format <a href="http://www.example.com/">inline URL</a>
                message = message + "<a href=\"" + "https://github.com/" + str(rom) + "/commit/" + str(commit) + "\">Commit " + str(number) + "</a>\n"
            if number == 70:
                message = message + "\nThere may be more commits, only upto 70 are shown here.\n"

            for i in converted:
                if i["sha"] == commit:
                    print("Found commit")
                    try:
                        commit_message = i["commit"]["message"]
                    except Exception as e:
                        commit_message = "Unable to get info"
                    try:
                        if i["author"] is not None:
                            author = i["author"]["login"]
                        else:
                            author = i["commit"]["author"]["name"]
                    except Exception as e:
                        author = "Unable to get info"
                    try:
                        author_email = i["commit"]["author"]["email"]
                    except Exception as e:
                        author_email = "Unable to get info"
                    try:
                        if i["committer"] is not None:
                            committer = i["committer"]["login"]
                        else:
                            committer = i["commit"]["committer"]["name"]
                    except Exception as e:
                        committer = "Unable to get info"
                    try:
                        committer_email = i["commit"]["committer"]["email"]
                    except Exception as e:
                        committer_email = "Unable to get info"

                    if len(telegraph_commit_content[telegraph_page]) > 20000:
                        telegraph_page += 1
                        telegraph_commit_content.append("")

                    telegraph_commit_content[telegraph_page] = telegraph_commit_content[telegraph_page] + "<h4>Commit " + str(number) + \
                                               "</h4>" +\
                                               commit_message.replace("<", "&#60;").replace(">", "&#62;") + \
                                               "\n\n<b>Author:</b> " + author + "&#60;" + \
                                               author_email + "&#62;" + "\n<b>Committer:</b> " + \
                                               committer + "&#60;" + committer_email + \
                                               "&#62;" + "\n<b>Commit ID: </b><code>" + str(commit) + "</code>\n" + \
                                               "<b>URL: </b> <a href=\"https://github.com/" + str(rom) + "/commit/"\
                                               + str(commit) + "\"> Click Me</a>\n"
            number += 1

        print (telegraph_commit_content)
        telegraph_urls = []
        footer = ""
        last_link = None
        for page in reversed(telegraph_commit_content):

            if last_link is None:
                footer = "<br>This is the last page"
            else:
                footer = "<br><a href=\"" + last_link + "\">Next Page</a>"

            try: 
                tgraph_response = tgraph.create_page(title=telegraph_title,
                                                    html_content=page.replace("\n", " <br> ") + "<br>@ROMTracker | #" + \
                                                    str(rom).split("/")[0].replace("-", "_") + footer,
                                                    author_name="ROM Tracker BOT",
                                                    author_url="https://t.me/ROM_tracker")

                telegraph_urls.append(tgraph_response["url"])
                last_link = tgraph_response["url"]
            except:
                telegraph_urls.append("unable to get")
                last_link = "unable to get"

        send_mes(message + "\n<a href=\"" + last_link + "\">Fully Detailed History (Upto 100 New Commits)</a>" +
                 "\n\n@ROMTracker | #" + str(rom).split("/")[0].replace("-", "_"))

        time.sleep(30)
        # to not spam api 
        update(rom, converted)
    else:
        print("All up to date") # For Logging purposes
