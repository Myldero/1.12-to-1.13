# Convert 1.12 commands to their 1.13 format

The program is supposed to update everything map-making related in your world automatically. This includes functions, loot tables, advancements, and all their file locations

It was made for Python 3, which you can get from https://www.python.org/

It will try to optimize your execute commands as much as possible but there might be cases where you can optimize it even more with the range of new possibilities in 1.13. (E.g. moving a scoreboard nbt command into the execute selector)

It's only able to convert 1.12 commands, so running this twice or running it with old or broken commands won't work!

It can't convert the stats command if you used that because the change was too big and it would require a lot of work for it to work every time. Maybe I'll make an option for successCount though since that's kind of predictable.

There might be problems with blocks if you used something like `detect ~ ~ ~ wool * ...` since wool has been split off into different blocks instead of just states.

#### Example command:

```
execute @s ~ ~1 ~ detect ~ ~ ~ stone 1 setblock ~ ~1 ~ chest 3 replace {LootTable:"loot:chest"}
```

```
execute offset ~ ~1 ~ if block ~ ~ ~ minecraft:granite then setblock ~ ~1 ~ minecraft:chest[facing=south]{LootTable:"demo:loot_tables/loot/chest"} replace
```

## How to use:

If you want to use this by only running one command at a time and converting it, you can go to https://tech.io/snippet/MmJ6djt

Install the repository by clicking "Clone or download" and then "Download ZIP". Unzip the file and you're ready to run the program. With python 3 installed, open run.py and type the path to the world folder into it (E.g. /home/[username]/.minecraft/saves/[world] or C:\Users\\[username]\AppData\Roaming\\.minecraft\saves\\[world] ). You also need to specify a name and a namespace for the datapack that your files are going to be moved into. The namespace can only contain lower case letters (a-z) and underscore. Hopefully there are no errors when you run it. If there aren't, you can go ahead and open up the world in 1.13. If there were errors or commands that haven't been converted correctly, you can report it in "Issues" and I'll do my best to fix it.

As you might know, this converter is based of the finished 1.13 so it won't work in the early snapshots.

Always remember to create a backup of your world, since this converter isn't made to convert from 1.13 snapshots to 1.13, so if you want to use it, it's most likely best to wait a bit more for all the fancy features to come out.
