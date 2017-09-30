import shutil
import json
import os
import re

#Set values
effect_id = ('speed', 'slowness', 'haste', 'mining_fatigue', 'strength', 'instant_health', 'instant_damage', 'jump_boost', 'nausea', 'regeneration', 'resistance', 'fire_resistance', 'water_breathing', 'invisibility', 'blindness', 'night_vision', 'hunger', 'weakness', 'poison', 'wither', 'health_boost', 'absorption', 'saturation', 'glowing', 'levitation', 'luck', 'unluck')

def change_block(block, data="", nbt=""):
	if data.isdigit():
		data = int(data)
	elif len(data) == 0:
		data = 0

	elif data not in ['-1','*']: #Just to take everything where there's already been used something like color=red
		tmp = data
		data = 0

		with open(os.path.join(".", "blockstates_other.txt"), 'r') as f:
			for line in f:
				if re.findall(r'^{} '.format(block), line):

					block, default, *states = line.split()

					if tmp == "default": #Just so it gets the right default value if data is "default"
						tmp = default

					block_args = {}

					for arg in tmp.split(","):
						key,value = arg.split("=")
						block_args[key] = value

					for arg in default.split(","):
						key,value = arg.split("=")
						if key not in block_args:
							block_args[key] = value



					for state in states:
						state,state_data = state.split(":")
						other_args = {}

						for arg in state.split(","):
							key,value = arg.split("=")
							other_args[key] = value

						if block_args == other_args:
							data = int(state_data)
							break

					break

	#Block State
	if data in ['-1','*']:
		#This will change if it becomes a possibility in 1.13. So far, it isn't.
		pass
	elif isinstance(data, int):
		with open(os.path.join(".", "blockstates.txt"), 'r') as f:
			for line in f:
				if re.findall(r'^{}:'.format(block), line): #Find block in blockstates.txt
					states = line.rstrip().split(":")[1].split(" ") #Gets list of block states
					if states[data % len(states)].isdigit():
						block = states[ int(states[data % len(states)]) ]
					else:
						block = states[data % len(states)] #This picks the correct block state
					break






	#NBT data
	if len(nbt) > 0:
		block += nbt

	return block

def change_item(item, data, nbt):
	if data.isdigit():
		data = int(data)
	elif len(data) == 0:
		data = 0

	if len(nbt) > 0:
		nbt = new_nbt(nbt)


	if any(item.endswith(i) for i in ("sword","shovel","pickaxe","axe","flint_and_steel","helmet","chestplate","leggings","boots","bow","fishing_rod","shears")):
		item += "{Damage:"+str(data)

		if len(nbt) > 0:
			item += ","+nbt[1:]
		else:
			item += "}"

		return item
	elif data > 0:
		with open(os.path.join(".", "itemvalues.txt"), 'r') as f:
			for line in f:
				if re.findall(r'^{}:'.format(item), line): #Find block in itemvalues.txt
					values = line.rstrip().split(":")[1].split(" ") #Gets list of block states

					return values[data % len(values)] + nbt #Returns the correct item and nbt concatenated

	return item + nbt #Returns the item and nbt concatenated


#Don't ask me about this NBT part here. It's really confusing and I was half asleep when I made it
def get_item_nbt(nbt, nbt_type):

	match_count = len([i for i in range(1, len(nbt)-len(nbt_type)) if re.findall(r'(?:\{|\,|\[|^)' + nbt_type + r'{$', nbt[i-1:i+len(nbt_type)+1])])

	for match_number in range(match_count):

		match_index = [i for i in range(1, len(nbt)-len(nbt_type)) if re.findall(r'(?:\{|\,|\[|^)' + nbt_type + r'{$', nbt[i-1:i+len(nbt_type)+1])][match_number]

		par_index = 1
		item_nbt = {'id': '', 'Damage': '0', 'tag': ''}
		other_nbt = []

		arg = ""
		val = ""
		tmp1 = False
		in_quotes = False
		end_index = 0

		for i in range(match_index+len(nbt_type)+1, len(nbt)-1):
			if nbt[i] in ("{","["):
				par_index += 1
			elif nbt[i] in ("}","]"):
				par_index -= 1

			if par_index == 0:
				end_index = i
				break

			elif nbt[i] == ":" and par_index == 1 and not in_quotes:
				tmp1 = True
			elif nbt[i] == "," and par_index == 1 and not in_quotes:

				if arg in ("id", "Damage", "tag"):
					item_nbt[arg] = val
				else:
					other_nbt += [arg+":"+val]

				tmp1 = False
				arg = ""
				val = ""
			elif nbt[i] == "\"":
				in_quotes = not in_quotes

				if tmp1 == True and arg == "tag":
					val += "\""

			else:
				if tmp1 == False:
					arg += nbt[i]
				elif tmp1 == True:
					val += nbt[i]
		if len(arg) > 0 and len(val) > 0:
			if arg in ("id", "Damage", "tag"):
				item_nbt[arg] = val
			else:
				other_nbt += [arg+":"+val]

		if re.findall(r'[a-z]$', item_nbt["Damage"]):
			item_nbt["Damage"] = item_nbt["Damage"][:-1]

		item_nbt["id"] = re.sub(r'^minecraft(?:\:)?([a-zA-Z_]+)', r'\1', item_nbt["id"])




		item, start_nbt, end_nbt = change_item(item_nbt["id"], item_nbt["Damage"], item_nbt["tag"]), match_index+len(nbt_type)+1, end_index

		output_nbt = nbt[:start_nbt]

		tmp_list = []


		tag = re.findall(r'[a-z]({.*})$', item)
		item = re.findall(r'(^[a-zA-Z_]+)', item)

		if len(item) > 0:
			tmp_list += ["id:\"minecraft:" + item[0] + "\""]

		if len(tag) > 0:
			tmp_list += ["tag:" + tag[0]]


		if len(other_nbt) > 0:
			tmp_list += [",".join(other_nbt)]

		if len(tmp_list) > 0:
			output_nbt += ",".join(tmp_list)

		nbt = output_nbt + nbt[end_nbt:]

	return nbt


def get_nbt_list(nbt, nbt_type):

	match_count = len([i for i in range(1, len(nbt)-len(nbt_type)) if re.findall(r'(?:\{|\,|\[|^)' + nbt_type + r'$', nbt[i-1:i+len(nbt_type)])])

	for match_number in range(match_count):

		match_index = [i for i in range(1, len(nbt)-len(nbt_type)) if re.findall(r'(?:\{|\,|\[|^)' + nbt_type + r'$', nbt[i-1:i+len(nbt_type)])][match_number]


		par_index = 1
		nbt_list = []

		val = ""
		in_quotes = False
		end_index = 0


		for i in range(match_index+len(nbt_type)+1, len(nbt)):
			if nbt[i] in ("{","["):
				par_index += 1
			elif nbt[i] in ("}","]"):
				par_index -= 1
			elif nbt[i] == "\"":
				in_quotes = not in_quotes


			if par_index == 0:
				end_index = i
				break

			elif nbt[i] == "," and par_index == 1 and not in_quotes:

				nbt_list += [val]
				val = ""
			else:
				val += nbt[i]
		if len(val) > 0:
			nbt_list += [val]

		if nbt_type in ("HandItems:","Items:","ArmorItems:","Inventory:","EnderItems:"):

			for i in range(len(nbt_list)):

				nbt_list[i] = get_item_nbt("{Item:" + nbt_list[i] + "}", "Item:")[6:-1]



		start_nbt, end_nbt = match_index+len(nbt_type)+1, end_index

		output_nbt = nbt[:start_nbt]

		if len(nbt_list) > 0:
			output_nbt += ",".join(nbt_list)

		nbt = output_nbt + nbt[end_nbt:]

	return nbt

def new_nbt(nbt):

	for i in ["HandItems:","Items:","ArmorItems:","Inventory:","EnderItems:"]:
		nbt = get_nbt_list(nbt, i)

	for i in ["Item:","buy:","sell:","SaddleItem:","SelectedItem:"]:
		nbt = get_item_nbt(nbt, i)

	return nbt



def get_executes(command):
	global executelist

	if command.startswith("/"):
		command = command[1:]

	if command.startswith("execute"):
		tmp = re.findall(r'^execute (@[a-z][A-Za-z0-9=\.,_\-\!\[\]]*|[a-zA-Z0-9_\-\#]+) ([~\-0-9\.]+ [~\-0-9\.]+ [~\-0-9\.]+) (.+)', command)
		executelist += [re.findall(r'^execute (?:@[a-z][A-Za-z0-9=\.,_\-\!\[\]]*|[a-zA-Z0-9_\-\#]+) [~\-0-9\.]+ [~\-0-9\.]+ [~\-0-9\.]+',command)[0]]
		if tmp:
			get_executes(tmp[0][2])

	elif command.startswith("detect"):

		tmp = re.findall(r'^detect ([~\-0-9\.]+ [~\-0-9\.]+ [~\-0-9\.]+) (?:minecraft\:)?([a-zA-Z_]+) ([\S]+) (.+)', command)
		executelist += [re.findall(r'^detect [~\-0-9\.]+ [~\-0-9\.]+ [~\-0-9\.]+ (?:minecraft\:)?[a-zA-Z_]+ [\S]+', command)[0]]
		if tmp:
			get_executes(tmp[0][3])
	elif re.findall(r'^tp(.*)~', command):
		tmp = re.findall(r'tp (@[a-z][A-Za-z0-9=\.,_\-\!\[\]]*|[a-zA-Z0-9_\-\#]+) ([~\-0-9\.]+ [~\-0-9\.]+ [~\-0-9\.]+)', command)[0]
		if tmp[0]+tmp[1] != "s":
			executelist += ["execute {0} ~ ~ ~".format(tmp[0])]
		executelist += ["tp @s {0}".format(tmp[1])]
	else:
		executelist += [command]

def convert_command(gets, filename):
	command = gets
	#try:
	if True:

		#Toggledownfall to weather clear
		command = re.sub(r'^toggledownfall', r'weather clear', command)

		#Gamemode
		command = re.sub(r'^gamemode (0|s)',r'gamemode survival',command)
		command = re.sub(r'^gamemode (1|c)',r'gamemode creative',command)
		command = re.sub(r'^gamemode (2|a)',r'gamemode adventure',command)
		command = re.sub(r'^gamemode (3|sp)',r'gamemode spectator',command)

		#Difficulty
		command = re.sub(r'^difficulty (0|p)',r'difficulty peaceful',command)
		command = re.sub(r'^difficulty (1|e)',r'difficulty easy',command)
		command = re.sub(r'^difficulty (2|n)',r'difficulty normal',command)
		command = re.sub(r'^difficulty (3|h)',r'difficulty hard',command)

		#Teleport to tp (Sorry if this will be confusing)
		command = re.sub(r'^teleport',r'tp', command)

		command = re.sub(r'^xp ([\-0-9]+)L (@[a-z][A-Za-z0-9=\.,_\-\!\[\]]*|[a-zA-Z0-9_\-\#]+)', r'xp add \2 \1 levels',command)
		command = re.sub(r'^xp ([\-0-9]+)L', r'xp add @s \1 levels',command)
		command = re.sub(r'^xp ([\-0-9]+) (@[a-z][A-Za-z0-9=\.,_\-\!\[\]]*|[a-zA-Z0-9_\-\#]+)', r'xp add \2 \1 points',command)
		command = re.sub(r'^xp ([\-0-9]+)', r'xp add @s \1 points',command)
		


		#Give, clear and replaceitem
		if command.startswith("give"):
			#Fill replace
			tmp = re.findall(r'^give (@[a-z][A-Za-z0-9=\.,_\-\!\[\]]*|[a-zA-Z0-9_\-\#]+) (?:minecraft\:)?([A-Za-z_]+)(?: )?([0-9]+)?(?: )?([0-9]+)?(?: )?({.*})?', command)
			command = re.sub(r'^give (@[a-z][A-Za-z0-9=\.,_\-\!\[\]]*|[a-zA-Z0-9_\-\#]+) (?:minecraft\:)?([A-Za-z_]+)(?: )?([0-9]+)?(?: )?([0-9]+)?(?: )?({.*})?', r'give \1 minecraft:pl@ceh0ld3r \3', command)
			if tmp:
				command = re.sub(r'pl@ceh0ld3r', change_item(tmp[0][1], tmp[0][3], tmp[0][4]), command)

		if command.startswith("clear"):
			#Fill replace
			tmp = re.findall(r'^clear (@[a-z][A-Za-z0-9=\.,_\-\!\[\]]*|[a-zA-Z0-9_\-\#]+) (?:minecraft\:)?([A-Za-z_]+)(?: )?([0-9]+)?(?: )?([0-9]+)?(?: )?({.*})?', command)
			command = re.sub(r'^clear (@[a-z][A-Za-z0-9=\.,_\-\!\[\]]*|[a-zA-Z0-9_\-\#]+) (?:minecraft\:)?([A-Za-z_]+)(?: )?([0-9]+)?(?: )?([0-9]+)?(?: )?({.*})?', r'clear \1 minecraft:pl@ceh0ld3r \4', command)
			if tmp:
				command = re.sub(r'pl@ceh0ld3r', change_item(tmp[0][1], tmp[0][2], tmp[0][4]), command)


		if command.startswith("replaceitem"):
			#Fill replace
			tmp = re.findall(r'^replaceitem entity (@[a-z][A-Za-z0-9=\.,_\-\!\[\]]*|[a-zA-Z0-9_\-\#]+) ([a-z0-9\.]+) (?:minecraft\:)?([A-Za-z_]+)(?: )?([0-9]+)?(?: )?([0-9]+)?(?: )?({.*})?', command)
			command = re.sub(r'^replaceitem entity (@[a-z][A-Za-z0-9=\.,_\-\!\[\]]*|[a-zA-Z0-9_\-\#]+) ([a-z0-9\.]+) (?:minecraft\:)?([A-Za-z_]+)(?: )?([0-9]+)?(?: )?([0-9]+)?(?: )?({.*})?', r'replaceitem entity \1 \2 minecraft:pl@ceh0ld3r \4', command)
			if tmp:
				command = re.sub(r'pl@ceh0ld3r', change_item(tmp[0][2], tmp[0][4], tmp[0][5]), command)
			else:
				tmp = re.findall(r'^replaceitem block ([~\-0-9\.]+ [~\-0-9\.]+ [~\-0-9\.]+) ([a-z0-9\.]+) (?:minecraft\:)?([A-Za-z_]+)(?: )?([0-9]+)?(?: )?([0-9]+)?(?: )?({.*})?', command)
				command = re.sub(r'^replaceitem block ([~\-0-9\.]+ [~\-0-9\.]+ [~\-0-9\.]+) ([a-z0-9\.]+) (?:minecraft\:)?([A-Za-z_]+)(?: )?([0-9]+)?(?: )?([0-9]+)?(?: )?({.*})?', r'replaceitem block \1 \2 minecraft:pl@ceh0ld3r \4', command)
				if tmp:
					command = re.sub(r'pl@ceh0ld3r', change_item(tmp[0][2], tmp[0][4], tmp[0][5]), command)



		#Effect command
		if command.startswith("effect"):

			#Effect ID's
			tmp = re.findall(r'^effect (@[a-z][A-Za-z0-9=\.,_\-\!\[\]]*|[a-zA-Z0-9_\-\#]+) (?:minecraft\:)?(speed|slowness|haste|mining_fatigue|strength|instant_health|instant_damage|jump_boost|nausea|regeneration|resistance|fire_resistance|water_breathing|invisibility|blindness|night_vision|hunger|weakness|poison|wither|health_boost|absorption|saturation|glowing|levitation|luck|unluck)', command)
			command = re.sub(r'^effect (@[a-z][A-Za-z0-9=\.,_\-\!\[\]]*|[a-zA-Z0-9_\-\#]+) (?:minecraft\:)?(speed|slowness|haste|mining_fatigue|strength|instant_health|instant_damage|jump_boost|nausea|regeneration|resistance|fire_resistance|water_breathing|invisibility|blindness|night_vision|hunger|weakness|poison|wither|health_boost|absorption|saturation|glowing|levitation|luck|unluck)', r'effect \1 pl@ceh0ld3r', command)
			if tmp:
				command = re.sub(r'pl@ceh0ld3r', str(effect_id.index(tmp[0][1]) + 1), command)


			#Effect clear
			command = re.sub(r'^effect (@[a-z][A-Za-z0-9=\.,_\-\!\[\]]*|[a-zA-Z0-9_\-\#]+) clear', r'effect clear \1', command)
			command = re.sub(r'^effect (@[a-z][A-Za-z0-9=\.,_\-\!\[\]]*|[a-zA-Z0-9_\-\#]+) ([0-9]+) 0(.*)', r'effect clear \1 \2', command)
			#Effect give
			command = re.sub(r'^effect (@[a-z][A-Za-z0-9=\.,_\-\!\[\]]*|[a-zA-Z0-9_\-\#]+) ([0-9]+) ([1-9][0-9]*)', r'effect give \1 \2 \3', command)
			command = re.sub(r'^effect (@[a-z][A-Za-z0-9=\.,_\-\!\[\]]*|[a-zA-Z0-9_\-\#]+) ([0-9]+)$', r'effect give \1 \2 30 0', command)

			#Effect ID's
			tmp = re.findall(r'^effect (give|clear) (@[a-z][A-Za-z0-9=\.,_\-\!\[\]]*|[a-zA-Z0-9_\-\#]+) ([0-9]+)', command)
			command = re.sub(r'^effect (give|clear) (@[a-z][A-Za-z0-9=\.,_\-\!\[\]]*|[a-zA-Z0-9_\-\#]+) ([0-9]+)', r'effect \1 \2 pl@ceh0ld3r', command)
			if tmp:
				command = re.sub(r'pl@ceh0ld3r', 'minecraft:' + effect_id[int(tmp[0][2]) - 1], command)



		#Function, advancement and loot table file locations
		command = re.sub(r'^function ([A-Za-z_]+):([A-Za-z_/]+)', r'function {}:functions/\1/\2'.format(datapack), command)
		command = re.sub(r'structure_block(.+)name:(?:")?([A-Za-z_/]+)(?:")?', r'structure_block\1name:"{}:structures/\2"'.format(datapack), command)

		if re.findall(r'^advancement (.*) minecraft:([A-Za-z_/]+)', command):
			command = re.sub(r'^advancement (.*) minecraft:([A-Za-z_/]+)', r'advancement \1 minecraft:advancements/\2', command)
		else:
			command = re.sub(r'^advancement (.*) ([A-Za-z_]+):([A-Za-z_/]+)', r'advancement \1 {}:advancements/\2/\3'.format(datapack), command)

		if re.findall(r'LootTable:"minecraft:([A-Za-z_/]+)"', command):
			command = re.sub(r'LootTable:"minecraft:([A-Za-z_/]+)"', r'LootTable:"minecraft:loot_tables/\1"', command)
		else:
			command = re.sub(r'LootTable:"([A-Za-z_]+):([A-Za-z_/]+)"', r'LootTable:"{}:loot_tables/\1/\2"'.format(datapack), command)




		#Block states instead of data values. It will just copy states over if they were already used
		if command.startswith("setblock"):
			tmp = re.findall(r'^setblock ([~\-0-9\.]+ [~\-0-9\.]+ [~\-0-9\.]+) (?:minecraft\:)?([A-Za-z_]+)(?: )?([\S]+)?(?: )?(destroy|keep|replace)?(?: )?(.+)?', command)
			command = re.sub(r'^setblock ([~\-0-9\.]+ [~\-0-9\.]+ [~\-0-9\.]+) (?:minecraft\:)?([A-Za-z_]+)(?: )?([\S]+)?(?: )?(destroy|keep|replace)?(?: )?(.+)?', r'setblock \1 minecraft:pl@ceh0ld3r \4', command)
			if tmp:
				command = re.sub(r'pl@ceh0ld3r', change_block(tmp[0][1], tmp[0][2], tmp[0][4]), command)

		if command.startswith("testforblock "):
			tmp = re.findall(r'^testforblock ([~\-0-9\.]+ [~\-0-9\.]+ [~\-0-9\.]+) (?:minecraft\:)?([A-Za-z_]+)(?: )?([\S]+)?(?: )?({.*})?', command)
			command = re.sub(r'^testforblock ([~\-0-9\.]+ [~\-0-9\.]+ [~\-0-9\.]+) (?:minecraft\:)?([A-Za-z_]+)(?: )?([\S]+)?(?: )?({.*})?', r'if block \1 minecraft:pl@ceh0ld3r', command)
			if tmp:
				data = tmp[0][2]
				if data == "":
					data = "*"


				command = re.sub(r'pl@ceh0ld3r', change_block(tmp[0][1], data, tmp[0][3]), command)

		if command.startswith("fill"):
			#Fill replace
			tmp = re.findall(r'^fill ([~\-0-9\.]+ [~\-0-9\.]+ [~\-0-9\.]+ [~\-0-9\.]+ [~\-0-9\.]+ [~\-0-9\.]+) (?:minecraft\:)?([A-Za-z_]+) ([\S]+) replace (?:minecraft\:)?([A-Za-z_]+)(?: )?([\S]+)?', command)
			command = re.sub(r'^fill ([~\-0-9\.]+ [~\-0-9\.]+ [~\-0-9\.]+ [~\-0-9\.]+ [~\-0-9\.]+ [~\-0-9\.]+) (?:minecraft\:)?([A-Za-z_]+) ([\S]+) replace (?:minecraft\:)?([A-Za-z_]+)(?: )?([\S]+)?', r'fill \1 minecraft:pl@ceh0ld3r replace minecraft:pl@ceh0ld2r', command)
			if tmp:
				command = re.sub(r'pl@ceh0ld3r', change_block(tmp[0][1], tmp[0][2], ""), command)
				command = re.sub(r'pl@ceh0ld2r', change_block(tmp[0][3], tmp[0][4], ""), command)
			else:
				#Fill normal
				tmp = re.findall(r'^fill ([~\-0-9\.]+ [~\-0-9\.]+ [~\-0-9\.]+ [~\-0-9\.]+ [~\-0-9\.]+ [~\-0-9\.]+) (?:minecraft\:)?([A-Za-z_]+) ([\S]+)(?: )?(destroy|hollow|keep|outline|replace)?(?: )?({.+})?', command)
				command = re.sub(r'^fill ([~\-0-9\.]+ [~\-0-9\.]+ [~\-0-9\.]+ [~\-0-9\.]+ [~\-0-9\.]+ [~\-0-9\.]+) (?:minecraft\:)?([A-Za-z_]+) ([\S]+)(?: )?(destroy|hollow|keep|outline|replace)?(?: )?({.+})?', r'fill \1 minecraft:pl@ceh0ld3r \4', command)
				if tmp:
					command = re.sub(r'pl@ceh0ld3r', change_block(tmp[0][1], tmp[0][2], tmp[0][4]), command)

		#Filtered clone
		tmp = re.findall(r'^clone ([~\-0-9\.]+ [~\-0-9\.]+ [~\-0-9\.]+ [~\-0-9\.]+ [~\-0-9\.]+ [~\-0-9\.]+ [~\-0-9\.]+ [~\-0-9\.]+ [~\-0-9\.]+) (filtered|replace|masked) (force|move|normal) (?:minecraft\:)?([A-Za-z_]+)(?: )?([\S]+)?', command)
		command = re.sub(r'^clone ([~\-0-9\.]+ [~\-0-9\.]+ [~\-0-9\.]+ [~\-0-9\.]+ [~\-0-9\.]+ [~\-0-9\.]+ [~\-0-9\.]+ [~\-0-9\.]+ [~\-0-9\.]+) (filtered|replace|masked) (force|move|normal) (?:minecraft\:)?([A-Za-z_]+)(?: )?([\S]+)?', r'clone \1 filtered \3 minecraft:pl@ceh0ld3r', command)
		if tmp:
			command = re.sub(r'pl@ceh0ld3r', change_block(tmp[0][3], tmp[0][4], ""), command)

		#Entity NBT
		tmp = re.findall(r'summon (minecraft\:)?([A-Za-z_]+) ([~\-0-9\.]+ [~\-0-9\.]+ [~\-0-9\.]+) ({.*})', command)
		command = re.sub(r'summon (minecraft\:)?([A-Za-z_]+) ([~\-0-9\.]+ [~\-0-9\.]+ [~\-0-9\.]+) ({.*})', r'summon \1\2 \3 pl@ceh0ld3r', command)
		if tmp:
			command = re.sub(r'pl@ceh0ld3r', new_nbt(tmp[0][3]), command)

		tmp = re.findall(r'entitydata (@[a-z][A-Za-z0-9=\.,_\-\!\[\]]*|[a-zA-Z0-9_\-\#]+) ({.*})', command)
		command = re.sub(r'entitydata (@[a-z][A-Za-z0-9=\.,_\-\!\[\]]*|[a-zA-Z0-9_\-\#]+) ({.*})', r'entitydata \1 pl@ceh0ld3r', command)
		if tmp:
			command = re.sub(r'pl@ceh0ld3r', new_nbt(tmp[0][1]), command)



		#Testforblocks
		command = re.sub(r'^testforblocks ([~\-0-9\.]+ [~\-0-9\.]+ [~\-0-9\.]+ [~\-0-9\.]+ [~\-0-9\.]+ [~\-0-9\.]+ [~\-0-9\.]+ [~\-0-9\.]+ [~\-0-9\.]+) (all|masked)', r'if blocks \1 \2', command)

		#Testfor
		command = re.sub(r'^testfor (@[a-z][A-Za-z0-9=\.,_\-\!\[\]]*|[a-zA-Z0-9_\-\#]+)( {.*})?', r'if entity \1\2', command)




	#except:
	#	print("[Error] Unknown error in {}".format(filename))
	#	return gets


	return command

def convert(command, filename):
	global executelist
	global tp_new_pos

	if command.startswith("/"):
		command = command[1:]


	if re.findall(r'^([a-z])',command):
		executelist = []
		get_executes(command)

		if tp_new_pos == False:
			new_pos = False
		else:
			new_pos = True

		tp_self = True #Used for detecting a tp command

		for i in range(len(executelist) - 1):
			if executelist[i].startswith("execute"):
				execute = re.findall(r'^execute (@[a-z][A-Za-z0-9=\.,_\-\!\[\]]*|[a-zA-Z0-9_\-\#]+) ([~\-0-9\.]+ [~\-0-9\.]+ [~\-0-9\.]+)',executelist[i])[0]

				if not execute[0].startswith("@s"):
					new_pos = True
					tp_self = False


				if execute[0] == "@s":
					useas = False
				else:
					useas = True

				if re.findall(r'^[~0]+ [~0]+ [~0]+$', execute[1]):
					offset = False
					useat = False
				else:
					offset = True
					useat = True


				if executelist[i + 1].startswith("execute"):
					next_execute = re.findall(r'^execute (@[a-z][A-Za-z0-9=\.,_\-\!\[\]]*|[a-zA-Z0-9_\-\#]+) ([~\-0-9\.]+ [~\-0-9\.]+ [~\-0-9\.]+)',executelist[i + 1])[0]

					if re.findall(r'(dx=|dy=|dz=|c=|r=|rm=)', next_execute[0]) or next_execute[0].startswith("@p"):
						useat = True



				elif executelist[i + 1].startswith("detect"):
					next_execute = re.findall(r'^detect ([~\-0-9\.]+ [~\-0-9\.]+ [~\-0-9\.]+) (?:minecraft\:)?([a-zA-Z_]+) ([\S]+)',executelist[i + 1])[0]
					useas = False
					useat = True


				elif re.findall(r'(~|dx=|dy=|dz=|c=|r=|rm=|@p)', executelist[i + 1]):
					useat = True
				elif executelist[i + 1].startswith("function"):
					useat = True








				if new_pos == False:
					useat = False
				elif useat == True:
					new_pos = False

				#Set it
				if useas == False and useat == False:
					if offset == False:
						executelist[i] = "" #Remove execute if it was only used for detecting a block for example
					else:
						executelist[i] = "offset {0}".format(execute[1])

				elif useas == True and useat == False:
					if offset == False:
						executelist[i] = "as {0}".format(execute[0]) #No at if relative coordinates weren't used
					else:
						executelist[i] = "as {0} offset {1}".format(execute[0], execute[1]) #Same just with offset

				elif useas == False and useat == True:

					if offset == False:
						executelist[i] = "at {0}".format(execute[0], execute[1]) #No at if relative coordinates weren't used
					else:
						executelist[i] = "at {0} offset {1}".format(execute[0], execute[1]) #Same just with offset

				elif useas == True and useat == True:

					if offset == False:
						executelist[i] = "as {0} at @s".format(execute[0]) #Use everything. Not always needed but makes sure that it works for function commands for example.
					else:
						executelist[i] = "as {0} at @s offset {1}".format(execute[0], execute[1]) #Same just with offset





			elif executelist[i].startswith("detect"):

				tmp = re.findall(r'^detect ([~\-0-9\.]+ [~\-0-9\.]+ [~\-0-9\.]+) (?:minecraft\:)?([A-Za-z_]+) ([\S]+)', executelist[i])
				executelist[i] = re.sub(r'^detect ([~\-0-9\.]+ [~\-0-9\.]+ [~\-0-9\.]+) (?:minecraft\:)?([A-Za-z_]+) ([\S]+)', r'if block \1 minecraft:pl@ceh0ld3r', executelist[i])
				if tmp:
					executelist[i] = re.sub(r'pl@ceh0ld3r', change_block(tmp[0][1], tmp[0][2], ""), executelist[i])

		executelist = [i for i in executelist if i != ""]

		if tp_self == True and re.findall(r'^tp @s', executelist[-1]):
			tp_new_pos = True

		executelist[-1] = convert_command(executelist[-1], filename)

		tmp = re.findall(r'^function (\S+) (if|unless) (@[a-z][A-Za-z0-9=\.,_\-\!\[\]]*|[a-zA-Z0-9_\-\#]+)', executelist[-1])
		if tmp:
			executelist[-1] = "{0} entity {1}".format(tmp[0][1], tmp[0][2])
			executelist += ["function {0}".format(tmp[0][0])]



		if executelist[-1].startswith("if "):
			command = "execute "+" ".join(executelist)
		elif len(executelist) > 1:
			command = "execute "+" ".join(executelist[:-1])+" then "+executelist[-1]
		else:
			command = executelist[-1]






		#Selectors
		tmp = re.findall(r'@([a-z])\[([A-Za-z0-9=\.,_\-\!]*)\]', command)
		command = re.sub(r'@([a-z])\[([A-Za-z0-9=\.,_\-\!]*)\]', r'@\1[pl@ceh0ld3r]', command)
		for match in tmp:
			selector = match[1].split(",")

			''' Turned off now because of a change where dx, dy and dz aren't doubles anymore. Will wait and see first though
			#dx dy dz
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

			else:'''
			if True:
				#Int coordinates to floats if needed
				for i in range(len(selector)):
					arg = selector[i].split("=")
					if arg[0] in ["x","y","z"]:
						selector[i] = "{}={}".format(arg[0],float(arg[1]) + 0.5)

			selector_lm = ""
			selector_l = ""

			selector_rm = ""
			selector_r = ""

			selector_rxm = ""
			selector_rx = ""

			selector_rym = ""
			selector_ry = ""

			selector_scoremin = ""
			selector_score = ""

			limit_used = False #For sort=arbitrary

			#Others
			n = len(selector)
			for i in range(n):
				arg = selector[i].split("=")

				#Gamemode
				if arg[0] == "m":
					if arg[1] in ["0","s"]:
						arg[1] = "survival"
					elif arg[1] in ["1","c"]:
						arg[1] = "creative"
					elif arg[1] in ["2","a"]:
						arg[1] = "adventure"
					elif arg[1] in ["3","sp"]:
						arg[1] = "spectator"

					selector[i] = "{}={}".format("gamemode", arg[1])

				#Limit
				if arg[0] == "c":
					if int(arg[1]) < 0:
						arg[1] = abs(int(arg[1]))
						selector += ["sort=furthest"]

					limit_used = True
					selector[i] = "{}={}".format("limit", arg[1])


				#Level
				if arg[0] == "lm":
					selector_lm = int(arg[1])
					selector[i] = "UNUSED" #Uses UNUSED to prevent changing the list size while iterating
				if arg[0] == "l":
					selector_l = int(arg[1])
					selector[i] = "UNUSED"

				#Distance
				if arg[0] == "rm":
					selector_rm = int(arg[1])
					selector[i] = "UNUSED"
				if arg[0] == "r":
					selector_r = int(arg[1])
					selector[i] = "UNUSED"

				#X rotation
				if arg[0] == "rxm":
					selector_rxm = int(arg[1])
					selector[i] = "UNUSED"
				if arg[0] == "rx":
					selector_rx = int(arg[1])
					selector[i] = "UNUSED"

				#Y rotation
				if arg[0] == "rym":
					selector_rym = int(arg[1])
					selector[i] = "UNUSED"
				if arg[0] == "ry":
					selector_ry = int(arg[1])
					selector[i] = "UNUSED"

				#Scores
				tmp = re.findall(r'score_([A-Za-z0-9]+)(_min)?', arg[0])
				if tmp:

					a = ""
					for j in range(i+1, n):
						arg2 = selector[j].split("=")

						if arg2[0] == "score_{}{}".format(tmp[0][0], "_min"*(len(tmp[0][1]) == 0) ):
							a = int(arg2[1])
							selector[j] = "UNUSED"
							break

					if str(a) == str(arg[1]):
						selector += ["score_{}={}".format(tmp[0][0], a)]
					elif len(tmp[0][1]) == 0: #If no _min
						selector += ["score_{}={}..{}".format(tmp[0][0], a, arg[1])]
					else:
						selector += ["score_{}={}..{}".format(tmp[0][0], arg[1], a)]

					selector[i] = "UNUSED"



			#Range selectors
			if selector_lm != "" or selector_l != "":
				if selector_lm == selector_l:
					selector += ["level={}".format(selector_lm)]
				else:
					selector += ["level={}..{}".format(selector_lm, selector_l)]

			if selector_rm != "" or selector_r != "":
				if selector_rm == selector_r:
					selector += ["distance={}".format(selector_rm)]
				else:
					selector += ["distance={}..{}".format(selector_rm, selector_r)]

			if selector_rxm != "" or selector_rx != "":
				if selector_rxm == selector_rx:
					selector += ["x_rotation={}".format(selector_rxm)]
				else:
					selector += ["x_rotation={}..{}".format(selector_rxm, selector_rx)]

			if selector_rym != "" or selector_ry != "":
				if selector_rym == selector_ry:
					selector += ["y_rotation={}".format(selector_rym)]
				else:
					selector += ["y_rotation={}..{}".format(selector_rym, selector_ry)]

			if not limit_used and match[0] in ["a","e"]:
				selector += ["sort=arbitrary"]

			selector = [i for i in selector if i != "UNUSED"]
			command = re.sub(r'pl@ceh0ld3r', ",".join(selector), command, count=1)

		command = re.sub(r'@(a|e)($|\s)', r'@\1[sort=arbitrary]\2', command)

		#Scoreboard NBT selector
		if "scoreboard" in command:


			#scoreboard players tag
			tmp = re.findall(r'scoreboard players tag @([a-z])([A-Za-z0-9=\.,_\-\!\[\]]*) (add|remove) ([\S]+) ({.*})', command)
			command = re.sub(r'scoreboard players tag @([a-z])([A-Za-z0-9=\.,_\-\!\[\]]*) (add|remove) ([\S]+) ({.*})', r'scoreboard players tag @\1pl@ceh0ld3r \3 \4', command)
			if tmp:
				if len(tmp[0][1]) > 0:
					command = re.sub(r'pl@ceh0ld3r', "[{0},nbt={1}]".format(tmp[0][1][1:-1], new_nbt(tmp[0][4])), command)
				else:
					command = re.sub(r'pl@ceh0ld3r', "[nbt={0}]".format(new_nbt(tmp[0][4])), command)

			#scoreboard players set/add/remove
			tmp = re.findall(r'scoreboard players (set|add|remove) @([a-z])([A-Za-z0-9=\.,_\-\!\[\]]*) ([\S]+) ([0-9]+) ({.*})', command)
			command = re.sub(r'scoreboard players (set|add|remove) @([a-z])([A-Za-z0-9=\.,_\-\!\[\]]*) ([\S]+) ([0-9]+) ({.*})', r'scoreboard players \1 @\2pl@ceh0ld3r \4 \5', command)
			if tmp:
				if len(tmp[0][2]) > 0:
					command = re.sub(r'pl@ceh0ld3r', "[{0},nbt={1}]".format(tmp[0][2][1:-1], new_nbt(tmp[0][5])), command)
				else:
					command = re.sub(r'pl@ceh0ld3r', "[nbt={0}]".format(new_nbt(tmp[0][5])), command)

		#testfor NBT selector and execute command
		if "if entity" in command:

			tmp = re.findall(r'if entity @([a-z])([A-Za-z0-9=\.,_\-\!\[\]]*) ({.*})', command)
			command = re.sub(r'if entity @([a-z])([A-Za-z0-9=\.,_\-\!\[\]]*) ({.*})', r'if entity @\1pl@ceh0ld3r', command)
			if tmp:
				if len(tmp[0][1]) > 0:
					command = re.sub(r'pl@ceh0ld3r', "[{0},nbt={1}]".format(tmp[0][1][1:-1], new_nbt(tmp[0][2])), command)
				else:
					command = re.sub(r'pl@ceh0ld3r', "[nbt={0}]".format(new_nbt(tmp[0][2])), command)

	return command+"\n"








def convert_advancement(adv):
	adv = json.loads(adv)

	try:
		if re.findall(r'minecraft:([A-Za-z_/]+)', adv['parent']):
			adv['parent'] = re.sub(r'minecraft:([A-Za-z_/]+)', r'minecraft:advancements/\1', adv['parent'])
		else:
			adv['parent'] = re.sub(r'([A-Za-z_]+):([A-Za-z_/]+)', r'{}:advancements/\1/\2'.format(datapack), adv['parent'])
	except:
		pass


	try:
		adv['rewards']['function'] = re.sub(r'([A-Za-z_]+):([A-Za-z_/]+)', r'{}:functions/\1/\2'.format(datapack), adv['rewards']['function'])
	except:
		pass


	try:
		newloot = []
		for loot in adv['rewards']['loot']:

			if re.findall(r'minecraft:([A-Za-z_/]+)', loot):
				newloot += [re.sub(r'minecraft:([A-Za-z_/]+)', r'minecraft:loot_tables/\1', loot)]
			else:
				newloot += [re.sub(r'([A-Za-z_]+):([A-Za-z_/]+)', r'{}:loot_tables/\1/\2'.format(datapack), loot)]

		adv['rewards']['loot'] = newloot
	except:
		pass


	try:
		item = adv['display']['icon']['item']

		try:
			data = adv['display']['icon']['data']
		except:
			data = 0

		adv['display']['icon']['item'] = change_item(item, data, "")
		del adv['display']['icon']['data']
	except:
		pass


	return json.dumps(adv, indent=4)



worldpath = input("Path to world folder: ")
datapack = input("Datapack name (a-z and underscore): ").rstrip()

while not re.findall(r'^[a-z_]+$', datapack):
	datapack = input("Datapack name (a-z and underscore): ")


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


#Make pack.mcmeta file
with open(os.path.join(worldpath, "data", datapack, "pack.mcmeta"), 'w+') as f:
	f.write( json.dumps( {"pack": {"pack_format": 3, "description": datapack}} , indent=4) )


#Convert functions
print("Converting functions")

for path, dirs, files in os.walk( os.path.join(worldpath, "data", datapack, "functions") ):
	for file in files:
		if file.endswith(".mcfunction"):
			fullpath = os.path.join(path, file)

			memory = ""

			with open(fullpath, 'r') as f:
				tp_new_pos = False
				linenumber = 0
				for line in f:
					linenumber += 1
					memory += convert(line.rstrip(), "{} line {}".format(fullpath[len(worldpath+"data")+2:-len(".mcfunction")], linenumber))

			with open(fullpath, 'w') as f:
				f.write(memory)


#Convert advancements
print("Converting advancements")

for path, dirs, files in os.walk( os.path.join(worldpath, "data", datapack, "advancements") ):
	for file in files:
		if file.endswith(".json"):
			fullpath = os.path.join(path, file)

			memory = ""

			with open(fullpath, 'r') as f:
				memory += convert_advancement(f.read())

			with open(fullpath, 'w') as f:
				f.write(memory)


print("Done")
input()
