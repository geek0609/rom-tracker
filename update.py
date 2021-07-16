import datetime
readme = open("Tracked_ROMs.MD", "w+")
# W+ to rewrite entire list everytime
content = "# The list of Repos of the ROMs that are tracked" \
          "\n\n*The list is automatically updated*" \
          "\n\n### Telegram Channel : [Click Me](https://t.me/ROM_tracker)" \
          "\n## ROMs:\n"

roms = open("roms.txt", "r")
number = 1
for rom in roms.readlines():
    content = content + str(number) + ". [" + rom.strip("\n") + "](https://github.com/" + rom.strip("\n") + ")\n"
    number += 1

roms1 = open("roms1.txt", "r")

for rom in roms1.readlines():
    content = content + str(number) + ". [" + rom.strip("\n") + "](https://github.com/" + rom.strip("\n") + ")\n"
    number += 1

roms2 = open("roms2.txt", "r")

for rom in roms2.readlines():
    content = content + str(number) + ". [" + rom.strip("\n") + "](https://github.com/" + rom.strip("\n") + ")\n"
    number += 1

roms3 = open("roms3.txt", "r")

for rom in roms3.readlines():
    content = content + str(number) + ". [" + rom.strip("\n") + "](https://github.com/" + rom.strip("\n") + ")\n"
    number += 1

roms4 = open("roms4.txt", "r")

for rom in roms4.readlines():
    content = content + str(number) + ". [" + rom.strip("\n") + "](https://github.com/" + rom.strip("\n") + ")\n"
    number += 1

content = content + "\n### Total number of repos tracked: " + str(number-1) +"\n\nLast updated on : " + str(datetime.datetime.utcnow()) + " UTC"

readme.write(content)
readme.close()
roms.close()
