# Convert 1.12 commands to their 1.13 format

The program is supposed to update everything map-making related in your world automatically. This includes functions, loot tables, advancements, and all their file locations

It was made for Python 3.5 https://www.python.org/downloads/release/python-350/

It won't fix anything that doesn't already work correctly in 1.12.

It will try to optimize your execute commands as much as possible but there might be cases where you can optimize it even more with the range of new possibilities in 1.13

#### Example command:

```sh
execute @s ~ ~1 ~ detect ~ ~ ~ stone 0 setblock ~ ~1 ~ chest 3 replace {LootTable:"loot:chest"}
```

```sh
execute offset ~ ~1 ~ if block ~ ~ ~ minecraft:stone[variant=stone] then setblock ~ ~1 ~ minecraft:chest[facing=south]{LootTable:"vg:loot_tables/loot/chest"} replace
```

## How to use:

Before opening up the world in 1.13, install the repository by clicking "Clone or download" and then "Download ZIP". Unzip the file and you're ready to run the program. With python 3 installed, open run.py and type the path to the world folder into it (E.g. /home/[username]/.minecraft/saves/[world] or C:\Users\\[username]\AppData\Roaming\\.minecraft\saves\\[world] ). You also need to specify a name for the datapack that your files are going to be moved into. The name can only contain lower case letters (a-z) and underscore. Hopefully there are no errors when you run it. If there aren't, you can go ahead and open up the world in 1.13. If there were errors, you can report it in "Issues" and I'll do my best to fix it. If there are commands that were converted wrongly and thus don't work, you can also report those there.

The MCEdit filter doesn't work yet because of an issue with Python 2.7 (The version MCEdit filters are written in) which I'll have to work around. It should be finished by 1.13 though.


This is obviously untested as of now since 1.13 snapshots haven't come out yet so remember to create a backup of your world first!
