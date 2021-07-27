import datetime
with open("Tracked_ROMs.MD", "w+") as readme:
    # W+ to rewrite entire list everytime
    content = "# The list of Repos of the ROMs that are tracked" \
              "\n\n*The list is automatically updated*" \
              "\n\n### Telegram Channel : [Click Me](https://t.me/ROM_tracker)" \
              "\n## ROMs:\n"

    with open("roms.txt", "r") as roms:
        number = 1
        for rom in roms.readlines():
            content = content + str(number) + ". [" + rom.strip("\n") + "](https://github.com/" + rom.strip("\n") + ")\n"
            number += 1

    content = content + "\n### Total number of repos tracked: " + str(number-1) +"\n\nLast updated on : " + str(datetime.datetime.utcnow()) + " UTC"
    readme.write(content)
