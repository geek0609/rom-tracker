import datetime

with open("roms.txt", "r") as f:
    roms = f.read().splitlines()

tracked_list = '\n'.join(
    f"{i}. [{rom}](https://github.com/{rom})" for i, rom in enumerate(roms)
)

content = '\n\n'.join(
    (
        '# The list of Repos of the ROMs that are tracked',
        '*The list is automatically updated*',
        '### Telegram Channel : [Click Me](https://t.me/ROM_tracker)',
        '## ROMs:',
        tracked_list,
        f'### Total number of repos tracked: {len(roms)}',
        f"Last updated on : {datetime.datetime.utcnow()} UTC"
    )
)

with open("Tracked_ROMs.MD", "w+") as readme:
    readme.write(content)
