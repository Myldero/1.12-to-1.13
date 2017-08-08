# Convert 1.12 commands to their 1.13 format

The program is supposed to update everything map-making related in your world automatically. This includes functions, loot tables, advancements, and all their file locations

It was made for Python 3.5 https://www.python.org/downloads/release/python-350/

It won't fix anything that doesn't already work correctly in 1.12.

It won't optimize your commands much either. You'll have to go through and change some things by yourself.

#### Example command:

```sh
execute @s ~ ~1 ~ detect ~ ~ ~ stone 0 setblock ~ ~1 ~ chest 3 replace {Items:[{Slot:0b,id:"minecraft:stone",Count:1b}]}
```

```sh
execute at @s offset ~ ~1 ~ execute if block ~ ~ ~ minecraft:stone[variant=stone] setblock ~ ~1 ~ minecraft:chest[facing=south]{Items:[{Slot:0b,id:"minecraft:stone",Count:1b}] replace
```

## How to use:

If you don't need to change anything within the actual map itself, you'll only need to install run.py. When you have that installed, you can open run.py and type the path to the world into it. You also need to specify a name for the datapack that your files are going to be moved into.

If you want to use the MCEdit filter too (You'll usually want to run run.py first), you'll want to move mcedit_1.13.py into the stock-filters folder for mcedit. Once you've done that, you can open up MCEdit and select all the blocks you need filtered, select the datapack name that you used before, and then run it.

Remember that you also need to change the gameLoopFunction gamerule so it points to the new location of the function.

This is obviously untested as of now since 1.13 snapshots haven't come out yet so remember to create a backup of your world first!
