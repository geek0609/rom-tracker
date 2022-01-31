import datetime
readme = open("Tracked_ROMs.MD", "w+")
# W+ to rewrite entire list everytime
content = "# The list of Repos of the ROMs that are tracked" \
          "\n\n*The list is automatically updated*" \
          "\n\n### Telegram Channel : [Click Me](https://t.me/ROM_tracker)" \
          "\n## ROMs:\n"

number = 1

REPO_LIST = ["roms.txt", "roms1.txt", "roms2.txt",
             "roms3.txt", "roms4.txt", "roms5.txt",
             "roms6.txt", "roms7.txt", "roms8.txt"]

for LIST in REPO_LIST:

    roms = open(LIST, "r")

    for rom in roms.readlines():
        if rom == "\n" or rom == "" or rom == " " or rom.startswith("#"):
            continue
        else:
            content = content + str(number) + ". [" + rom.strip("\n") + "](https://github.com/" + rom.strip("\n") + ")\n"
            number += 1

content = content + "\n### Total number of repos tracked: " + str(number-1) +"\n\nLast updated on : " + str(datetime.datetime.utcnow()) + " UTC"

readme.write(content)
readme.close()
