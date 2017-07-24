import os
import shutil
import re

#Set values
effect_id = ('speed', 'slowness', 'haste', 'mining_fatigue', 'strength', 'instant_health', 'instant_damage', 'jump_boost', 'nausea', 'regeneration', 'resistance', 'fire_resistance', 'water_breathing', 'invisibility', 'blindness', 'night_vision', 'hunger', 'weakness', 'poison', 'wither', 'health_boost', 'absorption', 'saturation', 'glowing', 'levitation', 'luck', 'unluck')

color = ("white","orange","magenta","light_blue","yellow","lime","pink","gray","silver","cyan","purple","blue","brown","green","red","black")
facing = ("north","north","north","south","west","east","north","north","north","south","west","east","north","north","north","south")
leaves = ("check_decay=false,decayable=true","check_decay=false,decayable=false","check_decay=true,decayable=true","check_decay=true,decayable=false")
door = ("half=lower,open=false,facing=east","half=lower,open=false,facing=south","half=lower,open=false,facing=west","half=lower,open=false,facing=north","half=lower,open=true,facing=east","half=lower,open=true,facing=south","half=lower,open=true,facing=west","half=lower,open=true,facing=north","half=upper,hinge=left,powered=false","half=upper,hinge=right,powered=false","half=upper,hinge=left,powered=true","half=upper,hinge=right,powered=true","half=upper,hinge=left,powered=false","half=upper,hinge=right,powered=false","half=upper,hinge=left,powered=true","half=upper,hinge=right,powered=true") #Doors are confusing
button = ("powered=false,facing=down","powered=false,facing=east","powered=false,facing=west","powered=false,facing=south","powered=false,facing=north","powered=false,facing=up","powered=false,facing=up","powered=false,facing=up","powered=true,facing=down","powered=true,facing=east","powered=true,facing=west","powered=true,facing=south","powered=true,facing=north","powered=true,facing=up","powered=true,facing=up","powered=true,facing=up")


def change_block(block, data, nbt, filename):
    if data.isdigit():
        data = int(data)
    elif len(data) == 0:
        data = 0


    if data in ['-1','*']:
        pass

    elif isinstance( data, int ):
        if block in ("wool","stained_glass","stained_hardened_clay","concrete","concrete_powder","stained_glass_pane","carpet"):
            block = "{0}_{1}".format(color[data], block)
        elif block in ("chest","furnace","ladder","ender_chest","trapped_chest","wall_sign","wall_banner"):
            block += "[facing={}]".format( facing[data] )
        elif block in ("water", "lava"):
            block += "[level={}]".format(data % 8) #This is not entirely correct but unless someone uses "water 15" to place regular water, it's going to work
        elif block == "leaves":
            block = "{0}_leaves[{1}]".format( ("oak","spruce","birch","jungle")[data % 4], leaves[int(data / 4)] )
        elif block == "leaves2":
            block = "{0}_leaves[{1}]".format( ("acacia","dark_oak")[data % 2], leaves[int(data / 4)] )
        elif block in ("redstone_wire","heavy_weighted_pressure_plate","light_weighted_pressure_plate"):
            block += "[power={}]".format(data)
        elif block in ("standing_sign","standing_banner"):
            block += "[rotation={}]".format(data)
        elif block in ("wooden_door","iron_door","spruce_door","birch_door","jungle_door","acacia_door","dark_oak_door"):
            block += "[{}]".format(door[data])
        elif block in ("stone_button","wooden_button"):
            block += "[{}]".format(button[data])

        elif data > 0:
            print("[Error] Some data was lost: {} {} in {}".format(block, data, filename))

    else:
        arg = data.split("=")
        if arg[0] == "color":
            block = "{0}_{1}".format(arg[1], block)
        else:
            block += "[{}]".format(data)

    if len(nbt) > 0:
        block += nbt

    return block

def convert_command(command, filename):


    if not command.startswith("#"):
        try:

            #Gamemode Selector
            command = re.sub(r'm=0',r'm=survival',command)
            command = re.sub(r'm=1',r'm=creative',command)
            command = re.sub(r'm=2',r'm=adventure',command)
            command = re.sub(r'm=3',r'm=spectator',command)

            #Gamemode
            command = re.sub(r'gamemode 0',r'gamemode survival',command)
            command = re.sub(r'gamemode 1',r'gamemode creative',command)
            command = re.sub(r'gamemode 2',r'gamemode adventure',command)
            command = re.sub(r'gamemode 3',r'gamemode spectator',command)

            #Difficulty
            command = re.sub(r'difficulty (0|p)',r'difficulty peaceful',command)
            command = re.sub(r'difficulty (1|e)',r'difficulty easy',command)
            command = re.sub(r'difficulty (2|n)',r'difficulty normal',command)
            command = re.sub(r'difficulty (3|h)',r'difficulty hard',command)


            #dx dy dz
            tmp = re.findall(r'@([a-z])\[([A-Za-z0-9=\.,_\-\!]*)\]', command)
            command = re.sub(r'@([a-z])\[([A-Za-z0-9=\.,_\-\!]*)\]', r'@\1[pl@ceh0ld3r]', command)
            for match in tmp:
                selector = match[1].split(",")

                if any(i in match[1] for i in ["dx","dy","dz"]):
                    if not "dx" in match[1]:
                        selector += ["dx=0"]
                    if not "dy" in match[1]:
                        selector += ["dy=0"]
                    if not "dz" in match[1]:
                        selector += ["dz=0"]

                if "dx" in match[1]:

                    for i in range(len(selector)):
                        arg = selector[i].split("=")
                        if arg[0] in ["dx","dy","dz"]:

                            selector[i] = "{}={}".format(arg[0],int(arg[1]) + 1)

                else:
                    #Int coordinates to floats if needed
                    for i in range(len(selector)):
                        arg = selector[i].split("=")
                        if arg[0] in ["x","y","z"]:
                            selector[i] = "{}={}".format(arg[0],float(arg[1]) + 0.5)



                command = re.sub(r'pl@ceh0ld3r', ",".join(selector), command, count=1)



            #Effect command
            if "effect" in command:

                #Effect ID's
                tmp = re.findall(r'effect @([a-z])([A-Za-z0-9=\.,_\-\!\[\]]*) (?:minecraft\:)?(speed|slowness|haste|mining_fatigue|strength|instant_health|instant_damage|jump_boost|nausea|regeneration|resistance|fire_resistance|water_breathing|invisibility|blindness|night_vision|hunger|weakness|poison|wither|health_boost|absorption|saturation|glowing|levitation|luck|unluck)', command)
                command = re.sub(r'effect @([a-z])([A-Za-z0-9=\.,_\-\!\[\]]*) (?:minecraft\:)?(speed|slowness|haste|mining_fatigue|strength|instant_health|instant_damage|jump_boost|nausea|regeneration|resistance|fire_resistance|water_breathing|invisibility|blindness|night_vision|hunger|weakness|poison|wither|health_boost|absorption|saturation|glowing|levitation|luck|unluck)', r'effect @\1\2 pl@ceh0ld3r', command)
                if tmp:
                    command = re.sub(r'pl@ceh0ld3r', str(effect_id.index(tmp[0][2]) + 1), command)


                #Effect clear
                command = re.sub(r'effect @([a-z])([A-Za-z0-9=\.,_\-\!\[\]]*) clear', r'effect clear @\1\2', command)
                command = re.sub(r'effect @([a-z])([A-Za-z0-9=\.,_\-\!\[\]]*) ([0-9]+) 0(.*)', r'effect clear @\1\2 \3', command)
                #Effect give
                command = re.sub(r'effect @([a-z])([A-Za-z0-9=\.,_\-\!\[\]]*) ([0-9]+) ([1-9][0-9]*)', r'effect give @\1\2 \3 \4', command)
                command = re.sub(r'effect @([a-z])([A-Za-z0-9=\.,_\-\!\[\]]*) ([0-9]+)$', r'effect give @\1\2 \3 30 0', command)

                #Effect ID's
                tmp = re.findall(r'effect (give|clear) @([a-z])([A-Za-z0-9=\.,_\-\!\[\]]*) ([0-9]+)', command)
                command = re.sub(r'effect (give|clear) @([a-z])([A-Za-z0-9=\.,_\-\!\[\]]*) ([0-9]+)', r'effect \1 @\2\3 pl@ceh0ld3r', command)
                if tmp:
                    command = re.sub(r'pl@ceh0ld3r', 'minecraft:' + effect_id[int(tmp[0][3]) - 1], command)



            #Function, advancement and loot table file locations
            command = re.sub(r'function ([A-Za-z_]+):([A-Za-z_/]+)', r'function {}:functions/\1/\2'.format(datapack), command)
            command = re.sub(r'advancement (.*) ([A-Za-z_]+):([A-Za-z_/]+)', r'advancement \1 {}:advancements/\2/\3'.format(datapack), command)
            command = re.sub(r'LootTable:"([A-Za-z_]+):([A-Za-z_/]+)"', r'LootTable:"{}:loot_tables/\1/\2"'.format(datapack), command)

            command = re.sub(r'structure_block(.+)name:(?:")?([A-Za-z]+):([A-Za-z_/]+)(?:")?', r'structure_block\1name:"\2/\3"', command)
            command = re.sub(r'structure_block(.+)name:(?:")?([A-Za-z_/]+)(?:")?', r'structure_block\1name:"{}:structures/\2"'.format(datapack), command)



            #Scoreboard NBT
            if "scoreboard" in command:


                #scoreboard players tag
                tmp = re.findall(r'scoreboard players tag @([a-z])([A-Za-z0-9=\.,_\-\!\[\]]*) (add|remove) ([\S]+) ({.*})', command)
                command = re.sub(r'scoreboard players tag @([a-z])([A-Za-z0-9=\.,_\-\!\[\]]*) (add|remove) ([\S]+) ({.*})', r'scoreboard players tag @\1pl@ceh0ld3r \3 \4', command)
                if tmp:
                    if len(tmp[0][1]) > 0:
                    	command = re.sub(r'pl@ceh0ld3r', "[{0},nbt={1}]".format(tmp[0][1][1:-1], tmp[0][4]), command)
                    else:
                        command = re.sub(r'pl@ceh0ld3r', "[nbt={0}]".format(tmp[0][4]), command)

                #scoreboard players set/add/remove
                tmp = re.findall(r'scoreboard players (set|add|remove) @([a-z])([A-Za-z0-9=\.,_\-\!\[\]]*) ([\S]+) ([0-9]+) ({.*})', command)
                command = re.sub(r'scoreboard players (set|add|remove) @([a-z])([A-Za-z0-9=\.,_\-\!\[\]]*) ([\S]+) ([0-9]+) ({.*})', r'scoreboard players \1 @\2pl@ceh0ld3r \4 \5', command)
                if tmp:
                    if len(tmp[0][2]) > 0:
                        command = re.sub(r'pl@ceh0ld3r', "[{0},nbt={1}]".format(tmp[0][2][1:-1], tmp[0][5]), command)
                    else:
                        command = re.sub(r'pl@ceh0ld3r', "[nbt={0}]".format(tmp[0][5]), command)

            #testfor NBT
            if "testfor" in command:

                tmp = re.findall(r'testfor @([a-z])([A-Za-z0-9=\.,_\-\!\[\]]*) ({.*})', command)
                command = re.sub(r'testfor @([a-z])([A-Za-z0-9=\.,_\-\!\[\]]*) ({.*})', r'testfor @\1pl@ceh0ld3r', command)
                if tmp:
                    if len(tmp[0][1]) > 0:
                        command = re.sub(r'pl@ceh0ld3r', "[{0},nbt={1}]".format(tmp[0][1][1:-1], tmp[0][2]), command)
                    else:
                        command = re.sub(r'pl@ceh0ld3r', "[nbt={0}]".format(tmp[0][2]), command)

            #Remove forward slashes in execute
            command = re.sub(r'execute @([a-z])([A-Za-z0-9=\.,_\-\!\[\]]*) ([~\-0-9\.]+ [~\-0-9\.]+ [~\-0-9\.]+) /', r'execute @\1\2 \3 ', command)
            command = re.sub(r'detect ([~\-0-9\.]+ [~\-0-9\.]+ [~\-0-9\.]+) ([a-zA-Z\:]+) ([0-9]+) /', r'detect \1 \2 \3 ', command)



            #Execute to "as" and "at". This also tries to optimize it a little
            tmp = re.findall(r'execute @([a-z])([A-Za-z0-9=\.,_\-\!\[\]]*) ([~\-0-9\.]+ [~\-0-9\.]+ [~\-0-9\.]+) (.*)', command)
            for match in tmp:
                execute = match[3]
                useas = True

                if re.findall(r'([~0]+ [~0]+ [~0]+)', match[2]):
                    offset = False
                    useat = False
                else:
                    offset = True
                    useat = True



                if re.findall(r'(~|dx=|dy=|dz=|c=|r=|rm=)', execute):
                    useat = True
                elif execute.startswith("function"):
                    useat = True



                if re.findall(r'@s', execute):
                    useas = True

                if any(execute.startswith(i) for i in ("setblock","fill","clone","blockdata","summon")):
                    useas = False



                if useas == False and useat == False and len(match[1]) > 2:
                    useat = True



                if useas == False and useat == False:
                    command = re.sub(r'execute @([a-z])([A-Za-z0-9=\.,_\-\!\[\]]*) ([~\-0-9\.]+ [~\-0-9\.]+ [~\-0-9\.]+) ',r'', command) #Remove execute if it was only used for detecting a block for example

                elif useas == True and useat == False:
                    command = re.sub(r'execute @([a-z])([A-Za-z0-9=\.,_\-\!\[\]]*) ([~\-0-9\.]+ [~\-0-9\.]+ [~\-0-9\.]+) ', r'as @\1\2 ', command) #No at if relative coordinates weren't used

                elif useas == False and useat == True:

                    if offset == False:
                        command = re.sub(r'execute @([a-z])([A-Za-z0-9=\.,_\-\!\[\]]*) ([~\-0-9\.]+ [~\-0-9\.]+ [~\-0-9\.]+) ', r'at @\1\2 ', command) #No at if relative coordinates weren't used
                    else:
                        command = re.sub(r'execute @([a-z])([A-Za-z0-9=\.,_\-\!\[\]]*) ([~\-0-9\.]+ [~\-0-9\.]+ [~\-0-9\.]+) ', r'at @\1\2 offset \3 ', command) #Same with offset

                elif useas == True and useat == True:

                    if offset == False:
                        command = re.sub(r'execute @([a-z])([A-Za-z0-9=\.,_\-\!\[\]]*) ([~\-0-9\.]+ [~\-0-9\.]+ [~\-0-9\.]+) ', r'as @\1\2 at @s ', command) #Use everything. Not always needed but makes sure that it works for function commands for example.
                    else:
                        command = re.sub(r'execute @([a-z])([A-Za-z0-9=\.,_\-\!\[\]]*) ([~\-0-9\.]+ [~\-0-9\.]+ [~\-0-9\.]+) ', r'as @\1\2 at @s offset \3 ', command) #Same with offset






            #Block states instead of data values (Only for some blocks). It will just copy states over if they were already used
            if "setblock" in command:
                tmp = re.findall(r'setblock ([~\-0-9\.]+ [~\-0-9\.]+ [~\-0-9\.]+) (?:minecraft\:)?([A-Za-z_]+)(?: )?([\S]+)?(?: )?(destroy|keep|replace)?(?: )?(.+)?', command)
                command = re.sub(r'setblock ([~\-0-9\.]+ [~\-0-9\.]+ [~\-0-9\.]+) (?:minecraft\:)?([A-Za-z_]+)(?: )?([\S]+)?(?: )?(destroy|keep|replace)?(?: )?(.+)?', r'setblock \1 minecraft:pl@ceh0ld3r \4', command)
                if tmp:
                    command = re.sub(r'pl@ceh0ld3r', change_block(tmp[0][1], tmp[0][2], tmp[0][4], filename), command)

            if "detect" in command:
                tmp = re.findall(r'detect ([~\-0-9\.]+ [~\-0-9\.]+ [~\-0-9\.]+) (?:minecraft\:)?([A-Za-z_]+) ([\S]+)', command)
                command = re.sub(r'detect ([~\-0-9\.]+ [~\-0-9\.]+ [~\-0-9\.]+) (?:minecraft\:)?([A-Za-z_]+) ([\S]+)', r'detect \1 minecraft:pl@ceh0ld3r', command)
                if tmp:
                    command = re.sub(r'pl@ceh0ld3r', change_block(tmp[0][1], tmp[0][2], "", filename), command)

            if "testforblock " in command:
                tmp = re.findall(r'testforblock ([~\-0-9\.]+ [~\-0-9\.]+ [~\-0-9\.]+) (?:minecraft\:)?([A-Za-z_]+)(?: )?([\S]+)?(?: )?({[.*]})?', command)
                command = re.sub(r'testforblock ([~\-0-9\.]+ [~\-0-9\.]+ [~\-0-9\.]+) (?:minecraft\:)?([A-Za-z_]+)(?: )?([\S]+)?(?: )?({[.*]})?', r'testforblock \1 minecraft:pl@ceh0ld3r', command)
                if tmp:
                    command = re.sub(r'pl@ceh0ld3r', change_block(tmp[0][1], tmp[0][2], tmp[0][3], filename), command)

            if "fill" in command:
                #Fill replace
                tmp = re.findall(r'fill ([~\-0-9\.]+ [~\-0-9\.]+ [~\-0-9\.]+ [~\-0-9\.]+ [~\-0-9\.]+ [~\-0-9\.]+) (?:minecraft\:)?([A-Za-z_]+) ([\S]+) replace (?:minecraft\:)?([A-Za-z_]+)(?: )?([\S]+)?', command)
                command = re.sub(r'fill ([~\-0-9\.]+ [~\-0-9\.]+ [~\-0-9\.]+ [~\-0-9\.]+ [~\-0-9\.]+ [~\-0-9\.]+) (?:minecraft\:)?([A-Za-z_]+) ([\S]+) replace (?:minecraft\:)?([A-Za-z_]+)(?: )?([\S]+)?', r'fill \1 minecraft:pl@ceh0ld3r replace minecraft:pl@ceh0ld2r', command)
                if tmp:
                    command = re.sub(r'pl@ceh0ld3r', change_block(tmp[0][1], tmp[0][2], "", filename), command)
                    command = re.sub(r'pl@ceh0ld2r', change_block(tmp[0][3], tmp[0][4], "", filename), command)
                else:
                    #Fill normal
                    tmp = re.findall(r'fill ([~\-0-9\.]+ [~\-0-9\.]+ [~\-0-9\.]+ [~\-0-9\.]+ [~\-0-9\.]+ [~\-0-9\.]+) (?:minecraft\:)?([A-Za-z_]+) ([\S]+)(?: )?(destroy|hollow|keep|outline|replace)?(?: )?({.+})?', command)
                    command = re.sub(r'fill ([~\-0-9\.]+ [~\-0-9\.]+ [~\-0-9\.]+ [~\-0-9\.]+ [~\-0-9\.]+ [~\-0-9\.]+) (?:minecraft\:)?([A-Za-z_]+) ([\S]+)(?: )?(destroy|hollow|keep|outline|replace)?(?: )?({.+})?', r'fill \1 minecraft:pl@ceh0ld3r \4', command)
                    if tmp:
                        command = re.sub(r'pl@ceh0ld3r', change_block(tmp[0][1], tmp[0][2], tmp[0][4], filename), command)

            #Filtered clone
            tmp = re.findall(r'clone ([~\-0-9\.]+ [~\-0-9\.]+ [~\-0-9\.]+ [~\-0-9\.]+ [~\-0-9\.]+ [~\-0-9\.]+ [~\-0-9\.]+ [~\-0-9\.]+ [~\-0-9\.]+) (filtered|replace|masked) (force|move|normal) (?:minecraft\:)?([A-Za-z_]+)(?: )?([\S]+)?', command)
            command = re.sub(r'clone ([~\-0-9\.]+ [~\-0-9\.]+ [~\-0-9\.]+ [~\-0-9\.]+ [~\-0-9\.]+ [~\-0-9\.]+ [~\-0-9\.]+ [~\-0-9\.]+ [~\-0-9\.]+) (filtered|replace|masked) (force|move|normal) (?:minecraft\:)?([A-Za-z_]+)(?: )?([\S]+)?', r'clone \1 filtered \3 minecraft:pl@ceh0ld3r', command)
            if tmp:
                command = re.sub(r'pl@ceh0ld3r', change_block(tmp[0][3], tmp[0][4], "", filename), command)



        except:
            print("A command had an error")

    return command








worldpath = input("Path to world folder: ")
datapack = input("Datapack name (Alphanumeric): ")

while not datapack.isalnum():
    datapack = input("Datapack name (Alphanumeric): ")


print("Moving directories")

try:
    shutil.move(os.path.join(worldpath, "data", "functions"), os.path.join(worldpath, "data", datapack, "functions"))
except:
    pass

try:
    shutil.move(os.path.join(worldpath, "data", "advancements"), os.path.join(worldpath, "data", datapack, "advancements"))
except:
    pass

try:
    shutil.move(os.path.join(worldpath, "data", "loot_tables"), os.path.join(worldpath, "data", datapack, "loot_tables"))
except:
    pass

try:
    shutil.move(os.path.join(worldpath, "structures"), os.path.join(worldpath, "data", datapack, "structures"))
except:
    pass


#Convert functions
print("Converting functions")

for path, dirs, files in os.walk( os.path.join(worldpath, "data", datapack, "functions") ):
    for file in files:
        if file.endswith(".mcfunction"):
            fullpath = os.path.join(path, file)

            memory = ""

            with open(fullpath, 'r') as f:
                linenumber = 0
                for line in f:
                    linenumber += 1
                    memory += convert_command(line, "{} line {}".format(fullpath[len(worldpath+"data")+2:-len(".mcfunction")], linenumber))

            with open(fullpath, 'w') as f:
                f.write(memory)

print("Done")
input()
