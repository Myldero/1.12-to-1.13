Convert 1.12 mcfunctions to their 1.13 format

The program is not finished but it will convert most of the commands and make your life easier when 1.13 comes out and changes everything

It was made for Python 3.5

The program won't fix anything that doesn't already work in 1.12. There's a lot of heuristics in this but it does what it needs to do right.

The program won't optimize your commands much either. You'll have to go through and change some things by yourself.

Example command:

`execute @s ~ ~1 ~ detect ~ ~ ~ stone 0 setblock ~ ~1 ~ chest 3 {Items:[{id:"minecraft:stone"}]}`

`as @s at @s offset ~ ~1 ~ detect ~ ~ ~ minecraft:stone setblock ~ ~1 ~ minecraft:chest[facing=south]{Items:[{id:"minecraft:stone"}]}`
