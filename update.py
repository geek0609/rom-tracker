import datetime
readme = open("Tracked_ROMs.MD", "w+")
content = "# The list of Manifest Repo of the ROMs that are tracked" \
          "\n\n*The list is automatically updated*" \
          "\n\n*Project is still work in progress*" \
          "\n\n### Telegram Channel : [Click Me](https://t.me/ROM_tracker)" \
          "\n## ROMs:\n"

roms = open("roms.txt", "r")

for rom in roms.readlines():
    content = content + " * [" + rom.strip("\n") + "](https://github.com/" + rom.strip("\n") + ")\n"

content = content + "\n\nLast updated on : " + str(datetime.datetime.utcnow()) + " UTC"

readme.write(content)
readme.close()
roms.close()
