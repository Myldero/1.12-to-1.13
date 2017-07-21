import re
import os


#Set values
effect_id = ['speed', 'slowness', 'haste', 'mining_fatigue', 'strength', 'instant_health', 'instant_damage', 'jump_boost', 'nausea', 'regeneration', 'resistance', 'fire_resistance', 'water_breathing', 'invisibility', 'blindness', 'night_vision', 'hunger', 'weakness', 'poison', 'wither', 'health_boost', 'absorption', 'saturation', 'glowing', 'levitation', 'luck', 'unluck']
color = ["white","orange","magenta","light_blue","yellow","lime","pink","gray","silver","cyan","purple","blue","brown","green","red","black"]
facing = ["north","north","north","south","west","east","north","north","north","south","west","east","north","north","north","south"]

def change_block(block, data, nbt):
    if data.isdigit():
        data = int(data)
    elif len(data) == 0:
        data = 0


    if data in ['-1','*']:
        pass

    elif isinstance( data, int ):
        if block in ["wool","stained_glass","stained_hardened_clay","concrete","concrete_powder","stained_glass_pane","carpet"]:
            block = "{0}_{1}".format(color[data], block)
        elif block in ["chest","furnace","ladder","ender_chest"]:
            block += "[facing={}]".format( facing[data] )
    else:
        tmp = data.split("=")
        if tmp[0] == "color":
            block = "{0}_{1}".format(tmp[1], block)
        else:
            block += "[{}]".format(data)

    if len(nbt) > 0:
        block += nbt

    return block

def to_113(command):
    global effect_id
    global color
    global facing

    #try:
    if True:

        #Gamemode Selector
        command = re.sub(r'm=0',r'm=survival',command)
        command = re.sub(r'm=1',r'm=creative',command)
        command = re.sub(r'm=2',r'm=adventure',command)
        command = re.sub(r'm=3',r'm=spectator',command)

        #Gamemode
        command = re.sub(r'gamemode 0',r'gamemode survival',command)
        command = re.sub(r'gamemode 1',r'gamemode creative',command)
        command = re.sub(r'gamemode 2',r'gamemode adeventure',command)
        command = re.sub(r'gamemode 3',r'gamemode spectator',command)

        #Difficulty
        command = re.sub(r'difficulty (0|p)',r'difficulty peaceful',command)
        command = re.sub(r'difficulty (1|e)',r'difficulty easy',command)
        command = re.sub(r'difficulty (2|n)',r'difficulty normal',command)
        command = re.sub(r'difficulty (3|h)',r'difficulty hard',command)


        #Int coordinates to .5
        command = re.sub(r'(x|y|z)=([0-9]+)(\,|\])',r'\1=\2.5\3',command)



        #Effect command
        if "effect" in command:

            #Effect ID's
            tmp = re.findall(r'effect @([a-zA-Z])([A-Za-z0-9=\.,_\-\!\[\]]*) (?:minecraft\:)?(speed|slowness|haste|mining_fatigue|strength|instant_health|instant_damage|jump_boost|nausea|regeneration|resistance|fire_resistance|water_breathing|invisibility|blindness|night_vision|hunger|weakness|poison|wither|health_boost|absorption|saturation|glowing|levitation|luck|unluck)', command)
            command = re.sub(r'effect @([a-zA-Z])([A-Za-z0-9=\.,_\-\!\[\]]*) (?:minecraft\:)?(speed|slowness|haste|mining_fatigue|strength|instant_health|instant_damage|jump_boost|nausea|regeneration|resistance|fire_resistance|water_breathing|invisibility|blindness|night_vision|hunger|weakness|poison|wither|health_boost|absorption|saturation|glowing|levitation|luck|unluck)', r'effect @\1\2 pl@ceh0ld3r', command)
            if tmp:
                command = re.sub(r'pl@ceh0ld3r', str(effect_id.index(tmp[0][2]) + 1), command)


            #Effect clear
            command = re.sub(r'effect @([a-zA-Z])([A-Za-z0-9=\.,_\-\!\[\]]*) clear', r'effect clear @\1\2', command)
            command = re.sub(r'effect @([a-zA-Z])([A-Za-z0-9=\.,_\-\!\[\]]*) ([0-9]+) 0(.*)', r'effect clear @\1\2 \3', command)
            #Effect give
            command = re.sub(r'effect @([a-zA-Z])([A-Za-z0-9=\.,_\-\!\[\]]*) ([0-9]+) ([1-9][0-9]*)', r'effect give @\1\2 \3 \4', command)
            command = re.sub(r'effect @([a-zA-Z])([A-Za-z0-9=\.,_\-\!\[\]]*) ([0-9]+)$', r'effect give @\1\2 \3', command)

            #Effect ID's
            tmp = re.findall(r'effect (give|clear) @([a-zA-Z])([A-Za-z0-9=\.,_\-\!\[\]]*) ([0-9]+)', command)
            command = re.sub(r'effect (give|clear) @([a-zA-Z])([A-Za-z0-9=\.,_\-\!\[\]]*) ([0-9]+)', r'effect \1 @\2\3 pl@ceh0ld3r', command)
            if tmp:
                command = re.sub(r'pl@ceh0ld3r', 'minecraft:' + effect_id[int(tmp[0][3]) - 1], command)

        #Function, advancement and loot table file locations
        if usenamespace.lower() in ["y","yes","true","on"]:
            command = re.sub(r'function ([A-Za-z_]+):([A-Za-z_/]+)', r'function \1:functions/\2', command)
            command = re.sub(r'advancement (.*) ([A-Za-z_]+):([A-Za-z_/]+)', r'advancement \1 \2:advancements/\3', command)
            command = re.sub(r'LootTable:"([A-Za-z_]+):([A-Za-z_/]+)"', r'LootTable:"\1:loot_tables/\2"', command)


        elif usenamespace.lower() in ["n","no","false","off"]:
            command = re.sub(r'function ([A-Za-z_]+):([A-Za-z_/]+)', r'function {}:functions/\1/\2'.format(datapack), command)
            command = re.sub(r'advancement (.*) ([A-Za-z_]+):([A-Za-z_/]+)', r'advancement \1 {}:advancements/\2/\3'.format(datapack), command)
            command = re.sub(r'LootTable:"([A-Za-z_]+):([A-Za-z_/]+)"', r'LootTable:"{}:loot_tables/\1/\2"'.format(datapack), command)



        #Scoreboard and testfor NBT
        if "scoreboard" in command:


            #scoreboard players tag
            tmp = re.findall(r'scoreboard players tag @([a-zA-Z])([A-Za-z0-9=\.,_\-\!\[\]]*) (add|remove) ([\S]+) ([\S]+)', command)
            command = re.sub(r'scoreboard players tag @([a-zA-Z])([A-Za-z0-9=\.,_\-\!\[\]]*) (add|remove) ([\S]+) ([\S]+)', r'scoreboard players tag @\1pl@ceh0ld3r \3 \4', command)
            if tmp:
                if len(tmp[0][1]) > 0:
                    command = re.sub(r'pl@ceh0ld3r', "[{0},nbt={1}]".format(tmp[0][1][1:-1], tmp[0][4]), command)
                else:
                    command = re.sub(r'pl@ceh0ld3r', "[nbt={0}]".format(tmp[0][4]), command)

            #scoreboard players set/add/remove
            tmp = re.findall(r'scoreboard players (set|add|remove) @([a-zA-Z])([A-Za-z0-9=\.,_\-\!\[\]]*) ([\S]+) ([0-9]+) ([\S]+)', command)
            command = re.sub(r'scoreboard players (set|add|remove) @([a-zA-Z])([A-Za-z0-9=\.,_\-\!\[\]]*) ([\S]+) ([0-9]+) ([\S]+)', r'scoreboard players \1 @\2pl@ceh0ld3r \4 \5', command)
            if tmp:
                if len(tmp[0][2]) > 0:
                    command = re.sub(r'pl@ceh0ld3r', "[{0},nbt={1}]".format(tmp[0][2][1:-1], tmp[0][5]), command)
                else:
                    command = re.sub(r'pl@ceh0ld3r', "[nbt={0}]".format(tmp[0][5]), command)

            #testfor
            tmp = re.findall(r'testfor @([a-zA-Z])([A-Za-z0-9=\.,_\-\!\[\]]*) ([\S]+)', command)
            command = re.sub(r'testfor @([a-zA-Z])([A-Za-z0-9=\.,_\-\!\[\]]*) ([\S]+)', r'testfor @\2pl@ceh0ld3r', command)
            if tmp:
                if len(tmp[0][1]) > 0:
                    command = re.sub(r'pl@ceh0ld3r', "[{0},nbt={1}]".format(tmp[0][1][1:-1], tmp[0][2]), command)
                else:
                    command = re.sub(r'pl@ceh0ld3r', "[nbt={0}]".format(tmp[0][2]), command)

        #Execute remove slashes
        command = re.sub(r'execute @([a-zA-Z])([A-Za-z0-9=\.,_\-\!\[\]]*) ([~\-0-9\.]+ [~\-0-9\.]+ [~\-0-9\.]+) /', r'execute @\1\2 \3 ', command)
        command = re.sub(r'detect ([~\-0-9\.]+ [~\-0-9\.]+ [~\-0-9\.]+) ([a-zA-Z\:]+) ([0-9]+) /', r'detect \1 \2 \3 ', command)

        #Execute to "as"
        command = re.sub(r'execute @([a-zA-Z])([A-Za-z0-9=\.,_\-\!\[\]]*) ([~0]+ [~0]+ [~0]+) (.*)(x=[0-9]+,y=[0-9]+,z=[0-9]+)', r'as @\1\2 \4\5', command)
        command = re.sub(r'execute @([a-zA-Z])([A-Za-z0-9=\.,_\-\!\[\]]*) ([~0]+ [~0]+ [~0]+) (.*)(~|dx=|dy=|dz=|c=|r=|rm=)', r'as @\1\2 at @s \4\5', command)
        command = re.sub(r'execute @([a-zA-Z])([A-Za-z0-9=\.,_\-\!\[\]]*) ([~0]+ [~0]+ [~0]+) ', r'as @\1\2 ', command)
        command = re.sub(r'execute @([a-zA-Z])([A-Za-z0-9=\.,_\-\!\[\]]*) ([~\-0-9\.]+ [~\-0-9\.]+ [~\-0-9\.]+) ', r'as @\1\2 at @s offset \3 ', command)

       	#New block data (Only for some blocks) for setblock, detect, fill
        if "setblock" in command:
            tmp = re.findall(r'setblock ([~\-0-9\.]+ [~\-0-9\.]+ [~\-0-9\.]+) (?:minecraft\:)?([A-Za-z_]+)(?: )?([\S]+)?(?: )?(destroy|keep|replace)?(?: )?(.+)?', command)
            command = re.sub(r'setblock ([~\-0-9\.]+ [~\-0-9\.]+ [~\-0-9\.]+) (?:minecraft\:)?([A-Za-z_]+)(?: )?([\S]+)?(?: )?(destroy|keep|replace)?(?: )?(.+)?', r'setblock \1 minecraft:pl@ceh0ld3r \4', command)
            if tmp:
                command = re.sub(r'pl@ceh0ld3r', change_block(tmp[0][1], tmp[0][2], tmp[0][4]), command)

        if "detect" in command:
            tmp = re.findall(r'detect ([~\-0-9\.]+ [~\-0-9\.]+ [~\-0-9\.]+) (?:minecraft\:)?([A-Za-z_]+) ([\S]+)', command)
            command = re.sub(r'detect ([~\-0-9\.]+ [~\-0-9\.]+ [~\-0-9\.]+) (?:minecraft\:)?([A-Za-z_]+) ([\S]+)', r'detect \1 minecraft:pl@ceh0ld3r', command)
            if tmp:
                command = re.sub(r'pl@ceh0ld3r', change_block(tmp[0][1], tmp[0][2], ""), command)

        if "fill" in command:
            #Fill replace
            tmp = re.findall(r'fill ([~\-0-9\.]+ [~\-0-9\.]+ [~\-0-9\.]+ [~\-0-9\.]+ [~\-0-9\.]+ [~\-0-9\.]+) (?:minecraft\:)?([A-Za-z_]+) ([\S]+) replace (?:minecraft\:)?([A-Za-z_]+)(?: )?([\S]+)?', command)
            command = re.sub(r'fill ([~\-0-9\.]+ [~\-0-9\.]+ [~\-0-9\.]+ [~\-0-9\.]+ [~\-0-9\.]+ [~\-0-9\.]+) (?:minecraft\:)?([A-Za-z_]+) ([\S]+) replace (?:minecraft\:)?([A-Za-z_]+)(?: )?([\S]+)?', r'fill \1 minecraft:pl@ceh0ld3r replace minecraft:pl@ceh0ld2r', command)
            if tmp:
                command = re.sub(r'pl@ceh0ld3r', change_block(tmp[0][1], tmp[0][2], ""), command)
                command = re.sub(r'pl@ceh0ld2r', change_block(tmp[0][3], tmp[0][4], ""), command)
            else:
                #Fill normal
                tmp = re.findall(r'fill ([~\-0-9\.]+ [~\-0-9\.]+ [~\-0-9\.]+ [~\-0-9\.]+ [~\-0-9\.]+ [~\-0-9\.]+) (?:minecraft\:)?([A-Za-z_]+) ([\S]+)(?: )?(destroy|hollow|keep|outline|replace)?(?: )?({.+})?', command)
                command = re.sub(r'fill ([~\-0-9\.]+ [~\-0-9\.]+ [~\-0-9\.]+ [~\-0-9\.]+ [~\-0-9\.]+ [~\-0-9\.]+) (?:minecraft\:)?([A-Za-z_]+) ([\S]+)(?: )?(destroy|hollow|keep|outline|replace)?(?: )?({.+})?', r'fill \1 minecraft:pl@ceh0ld3r \4', command)
                if tmp:
                    command = re.sub(r'pl@ceh0ld3r', change_block(tmp[0][1], tmp[0][2], tmp[0][4]), command)



    #except:
    #    print("A command had an error")

    return command

usenamespace = input("Use namespaces as datapack names? (y/n): ")
if usenamespace.lower() in ["n","no","false","off"]:
    datapack = input("Datapack name: ")


while True:
    print(to_113(input()))

"""
path = input("Path to functions file: ")

print("Changing stuff")

for path, dirs, files in os.walk(path):
    for filename in files:
        fullpath = os.path.join(path, filename)

        memory = ""

        with open(fullpath, 'r') as f:
            for line in f:
                memory += to_113(line)

        with open(fullpath, 'w') as f:
            f.write(memory)
"""
