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

		if block.startswith("skull"):
			skulls = ['skeleton_skull', 'wither_skeleton_skull', 'zombie_head', 'player_head', 'creeper_head', 'dragon_head']

			rotation = 0
			skull_type = 0

			#Set rotation
			tmp = re.findall(r'Rot:([0-9]+)', nbt)
			if tmp:
				rotation = int(tmp[0][0])

				nbt = re.sub(r'(,)?Rot:([0-9]+)(b)?(,)?', r',', nbt)
				nbt = re.sub(r'^{,', r'{', nbt)
				nbt = re.sub(r',}$', r'}', nbt)


			if block.startswith("skull["):
				block = block[:-1] + ",rotation="+str(rotation)+"]"
			else:
				block = block + "[rotation="+str(rotation)+"]"


			#Set Skull Type
			tmp = re.findall(r'SkullType:([0-9])', nbt)
			if tmp:
				skull_type = int(tmp[0][0])

				nbt = re.sub(r'(,)?SkullType:([0-9])(b)?(,)?', r',', nbt)
				nbt = re.sub(r'^{,', r'{', nbt)
				nbt = re.sub(r',}$', r'}', nbt)


			block = re.sub(r'^skull', skulls[skull_type], block)


		elif block.startswith("wall_skull"):
			wall_skulls = ['skeleton_wall_skull', 'wither_skeleton_wall_skull', 'zombie_wall_head', 'player_wall_head', 'creeper_wall_head', 'dragon_wall_head']

			skull_type = 0

			tmp = re.findall(r'SkullType:([0-9])', nbt)
			if tmp:
				skull_type = int(tmp[0][0])

				nbt = re.sub(r'(,)?SkullType:([0-9])(b)?(,)?', r',', nbt)
				nbt = re.sub(r'^{,', r'{', nbt)
				nbt = re.sub(r',}$', r'}', nbt)


			block = re.sub(r'^wall_skull', wall_skulls[skull_type], block)
			nbt = ""

		elif block.startswith("wall_banner") or block.startswith("banner"):
			colors = ['black', 'red', 'green', 'brown', 'blue', 'purple', 'cyan', 'light_gray', 'gray', 'pink', 'lime', 'yellow', 'light_blue', 'magenta', 'orange', 'white']
			color = 0


			tmp = re.findall(r'Base:([0-9]+)', nbt)
			if tmp:
				color = int(tmp[0][0])

				nbt = re.sub(r'(,)?Base:([0-9])(b)?(,)?', r',', nbt)
				nbt = re.sub(r'^{,', r'{', nbt)
				nbt = re.sub(r',}$', r'}', nbt)


			block = colors[color] + "_" + block

		elif block.startswith("bed"):
			colors = ['white', 'orange', 'magenta', 'light_blue', 'yellow', 'lime', 'pink', 'gray', 'light_gray', 'cyan', 'purple', 'blue', 'brown', 'green', 'red', 'black']
			color = 0
			tmp = re.findall(r'color:([0-9]+)', nbt, flags=re.IGNORECASE)
			if tmp:
				color = int(tmp[0][0])

			block = colors[color] + "_" + block
			nbt = ""

		elif block.startswith("note_block"):
			note = 0
			tmp = re.findall(r'note:([0-9]+)', nbt, flags=re.IGNORECASE)
			if tmp:
				note = int(tmp[0][0])

			block = block + "[note="+str(note)+"]"
			nbt = ""

		elif block.startswith("flower_pot"):

			flowers = {'red_flower 0': 'poppy', 'yellow_flower 0': 'dandelion', 'sapling 0': 'oak_sapling', 'sapling 1': 'spruce_sapling', 'sapling 2': 'birch_sapling', 'sapling 3': 'jungle_sapling', 'red_mushroom 0': 'red_mushroom', 'brown_mushroom 0': 'brown_mushroom', 'cactus 0': 'cactus', 'deadbush 0': 'dead_bush', 'tallgrass 2': 'fern', 'sapling 4': 'acacia_sapling', 'sapling 5': 'dark_oak_sapling', 'red_flower 1': 'blue_orchid', 'red_flower 2': 'allium', 'red_flower 3': 'azure_bluet', 'red_flower 4': 'red_tulip', 'red_flower 5': 'orange_tulip', 'red_flower 6': 'white_tulip', 'red_flower 7': 'pink_tulip', 'red_flower 8': 'oxeye_daisy'}
			flower_id = "air"
			flower_data = 0
			#{Item:"minecraft:red_flower",Data:0}
			tmp = re.findall(r'Item:(?:\")?(?:minecraft:)?([a-z_]+)', nbt, flags=re.IGNORECASE)
			if tmp:
				flower_id = tmp[0]

			tmp = re.findall(r'Data:([0-9]+)', nbt, flags=re.IGNORECASE)
			if tmp:
				flower_data = int(tmp[0][0])

				tmp = flower_id+" "+str(flower_data)
				if tmp in flowers:
					block = "potted_" + flowers[tmp]

			nbt = ""










	#NBT data
	if len(nbt) > 2:
		block += nbt

	return block

def change_item(item, data, nbt):
	if data.isdigit():
		data = int(data)
	elif data == '*':
		data = -1
	elif len(data) == 0:
		data = 0

	if len(nbt) > 0:
		nbt = new_nbt(nbt)


	if data != -1 and any(item.endswith(i) for i in ("filled_map","sword","shovel","pickaxe","hoe","axe","flint_and_steel","helmet","chestplate","leggings","boots","bow","fishing_rod","shears")):
		item += "{Damage:"+str(data)

		if len(nbt) > 0:
			item += ","+nbt[1:]
		else:
			item += "}"

		return item
	if item == "spawn_egg":

		tmp = re.findall(r'entitytag:{id:(?:\")?(?:minecraft:)?([a-z_]+)', nbt.lower())
		if tmp:
			return tmp[0] + "_" + item



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
		item_nbt = {'id': '', 'Damage': '*', 'tag': ''}
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

		if len(item_nbt["id"]) > 0:

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

		elif nbt_type in ("CanDestroy:","CanPlaceOn:"):

			for i in range(len(nbt_list)):

				block = re.findall(r'(?:minecraft:)?([a-z_]+)',nbt_list[i])[0]
				with open(os.path.join(".", "blockstates.txt"), 'r') as f:
					for line in f:
						if re.findall(r'^{}:'.format(block), line): #Find block in blockstates.txt
							states = ["minecraft:"+i for i in set(re.findall(r'(?:\:| )([a-z_]+)', line))]
							print(states)
							if states[0] == "minecraft:skull":
								states = ['minecraft:skeleton_skull', 'minecraft:wither_skeleton_skull', 'minecraft:zombie_head', 'minecraft:player_head', 'minecraft:creeper_head', 'minecraft:dragon_head', 'minecraft:skeleton_wall_skull', 'minecraft:wither_skeleton_wall_skull', 'minecraft:zombie_wall_head', 'minecraft:player_wall_head', 'minecraft:creeper_wall_head', 'minecraft:dragon_wall_head']
							elif states[0] == "minecraft:banner":
								states = ['minecraft:black_banner', 'minecraft:red_banner', 'minecraft:green_banner', 'minecraft:brown_banner', 'minecraft:blue_banner', 'minecraft:purple_banner', 'minecraft:cyan_banner', 'minecraft:light_gray_banner', 'minecraft:gray_banner', 'minecraft:pink_banner', 'minecraft:lime_banner', 'minecraft:yellow_banner', 'minecraft:light_blue_banner', 'minecraft:magenta_banner', 'minecraft:orange_banner', 'minecraft:white_banner']
							elif states[0] == "minecraft:wall_banner":
								states = ['minecraft:black_wall_banner', 'minecraft:red_wall_banner', 'minecraft:green_wall_banner', 'minecraft:brown_wall_banner', 'minecraft:blue_wall_banner', 'minecraft:purple_wall_banner', 'minecraft:cyan_wall_banner', 'minecraft:light_gray_wall_banner', 'minecraft:gray_wall_banner', 'minecraft:pink_wall_banner', 'minecraft:lime_wall_banner', 'minecraft:yellow_wall_banner', 'minecraft:light_blue_wall_banner', 'minecraft:magenta_wall_banner', 'minecraft:orange_wall_banner', 'minecraft:white_wall_banner']
							elif states[0] == "minecraft:bed":
								states = ['minecraft:white_bed', 'minecraft:orange_bed', 'minecraft:magenta_bed', 'minecraft:light_blue_bed', 'minecraft:yellow_bed', 'minecraft:lime_bed', 'minecraft:pink_bed', 'minecraft:gray_bed', 'minecraft:light_gray_bed', 'minecraft:cyan_bed', 'minecraft:purple_bed', 'minecraft:blue_bed', 'minecraft:brown_bed', 'minecraft:green_bed', 'minecraft:red_bed', 'minecraft:black_bed']
							elif states[0] == "minecraft:flower_pot":
								states = ['minecraft:flower_pot', 'minecraft:potted_poppy', 'minecraft:potted_dandelion', 'minecraft:potted_oak_sapling', 'minecraft:potted_spruce_sapling', 'minecraft:potted_birch_sapling', 'minecraft:potted_jungle_sapling', 'minecraft:potted_red_mushroom', 'minecraft:potted_brown_mushroom', 'minecraft:potted_cactus', 'minecraft:potted_dead_bush', 'minecraft:potted_fern', 'minecraft:potted_acacia_sapling', 'minecraft:potted_dark_oak_sapling', 'minecraft:potted_blue_orchid', 'minecraft:potted_allium', 'minecraft:potted_azure_bluet', 'minecraft:potted_red_tulip', 'minecraft:potted_orange_tulip', 'minecraft:potted_white_tulip', 'minecraft:potted_pink_tulip', 'minecraft:potted_oxeye_daisy']

							nbt_list[i] = "\"" + "\",\"".join(states) + "\""




							



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

	for i in ["CanPlaceOn:","CanDestroy:"]:
		nbt = get_nbt_list(nbt, i)
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
		if tmp[0] != "@s":
			executelist += ["execute {0} ~ ~ ~".format(tmp[0])]
		executelist += ["tp @s {0}".format(tmp[1])]

	elif command.startswith("entitydata"):
		tmp = re.findall(r'entitydata (@[a-z][A-Za-z0-9=\.,_\-\!\[\]]*|[a-zA-Z0-9_\-\#]+)(.*)', command)[0]
		if not tmp[0].startswith("@s") and not tmp[0].startswith("@p") and not 'c=1' in tmp[0]:
			executelist += ["execute {0} ~ ~ ~".format(tmp[0])]
			executelist += ["entitydata @s{0}".format(tmp[1])]
		else:
			executelist += ["entitydata {0}{1}".format(tmp[0], tmp[1])]
	else:
		executelist += [command]

def convert_command(gets, filename):
	command = gets
	try:

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

		#Teams now
		command = re.sub(r'^scoreboard teams', r'team', command)
		


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
			tmp = re.findall(r'^replaceitem entity (@[a-z][A-Za-z0-9=\.,_\-\!\[\]]*|[a-zA-Z0-9_\-\#]+) slot\.([a-z0-9\.]+) (?:minecraft\:)?([A-Za-z_]+)(?: )?([0-9]+)?(?: )?([0-9]+)?(?: )?({.*})?', command)
			command = re.sub(r'^replaceitem entity (@[a-z][A-Za-z0-9=\.,_\-\!\[\]]*|[a-zA-Z0-9_\-\#]+) slot\.([a-z0-9\.]+) (?:minecraft\:)?([A-Za-z_]+)(?: )?([0-9]+)?(?: )?([0-9]+)?(?: )?({.*})?', r'replaceitem entity \1 \2 minecraft:pl@ceh0ld3r \4', command)
			if tmp:
				command = re.sub(r'pl@ceh0ld3r', change_item(tmp[0][2], tmp[0][4], tmp[0][5]), command)
			else:
				tmp = re.findall(r'^replaceitem block ([~\-0-9\.]+ [~\-0-9\.]+ [~\-0-9\.]+) slot\.([a-z0-9\.]+) (?:minecraft\:)?([A-Za-z_]+)(?: )?([0-9]+)?(?: )?([0-9]+)?(?: )?({.*})?', command)
				command = re.sub(r'^replaceitem block ([~\-0-9\.]+ [~\-0-9\.]+ [~\-0-9\.]+) slot\.([a-z0-9\.]+) (?:minecraft\:)?([A-Za-z_]+)(?: )?([0-9]+)?(?: )?([0-9]+)?(?: )?({.*})?', r'replaceitem block \1 \2 minecraft:pl@ceh0ld3r \4', command)
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
		command = re.sub(r'^function ([A-Za-z_]+):([A-Za-z_/]+)', r'function {}:\1/\2'.format(datapack), command)
		command = re.sub(r'structure_block(.+)name:(?:")?([A-Za-z_/]+)(?:")?', r'structure_block\1name:"{}:\2"'.format(datapack), command)

		if re.findall(r'^advancement (.*) minecraft:([A-Za-z_/]+)', command):
			command = re.sub(r'^advancement (.*) minecraft:([A-Za-z_/]+)', r'advancement \1 minecraft:\2', command)
		else:
			command = re.sub(r'^advancement (.*) ([A-Za-z_]+):([A-Za-z_/]+)', r'advancement \1 {}:\2/\3'.format(datapack), command)

		if re.findall(r'LootTable:"minecraft:([A-Za-z_/]+)"', command):
			command = re.sub(r'LootTable:"minecraft:([A-Za-z_/]+)"', r'LootTable:"minecraft:\1"', command)
		else:
			command = re.sub(r'LootTable:"([A-Za-z_]+):([A-Za-z_/]+)"', r'LootTable:"{}:\1/\2"'.format(datapack), command)




		#Block states instead of data values. It will just copy states over if they were already used
		if command.startswith("setblock"):
			tmp = re.findall(r'^setblock ([~\-0-9\.]+ [~\-0-9\.]+ [~\-0-9\.]+) (?:minecraft\:)?([A-Za-z_]+)(?: )?([\S]+)?(?: )?(destroy|keep|replace)?(?: )?({.+})?', command)
			command = re.sub(r'^setblock ([~\-0-9\.]+ [~\-0-9\.]+ [~\-0-9\.]+) (?:minecraft\:)?([A-Za-z_]+)(?: )?([\S]+)?(?: )?(destroy|keep|replace)?(?: )?({.+})?', r'setblock \1 minecraft:pl@ceh0ld3r \4', command)
			if tmp:
				command = re.sub(r'pl@ceh0ld3r', change_block(tmp[0][1], tmp[0][2], new_nbt(tmp[0][4])), command)

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
		tmp = re.findall(r'^summon (minecraft\:)?([A-Za-z_]+)', command)
		command = re.sub(r'^summon (minecraft\:)?([A-Za-z_]+)', r'summon \1pl@ceh0ld3r', command)
		if tmp:
			command = re.sub(r'pl@ceh0ld3r', tmp[0][1].lower(), command)


		tmp = re.findall(r'^summon (minecraft\:)?([A-Za-z_]+) ([~\-0-9\.]+ [~\-0-9\.]+ [~\-0-9\.]+) ({.*})', command)
		command = re.sub(r'^summon (minecraft\:)?([A-Za-z_]+) ([~\-0-9\.]+ [~\-0-9\.]+ [~\-0-9\.]+) ({.*})', r'summon \1\2 \3 pl@ceh0ld3r', command)
		if tmp:
			command = re.sub(r'pl@ceh0ld3r', new_nbt(tmp[0][3]), command)


		#Entitydata
		tmp = re.findall(r'^entitydata (@[a-z][A-Za-z0-9=\.,_\-\!\[\]]*|[a-zA-Z0-9_\-\#]+) ({.+})', command)
		command = re.sub(r'^entitydata (@[a-z][A-Za-z0-9=\.,_\-\!\[\]]*|[a-zA-Z0-9_\-\#]+) ({.+})', r'data merge entity \1 pl@ceh0ld3r', command)
		if tmp:
			command = re.sub(r'pl@ceh0ld3r', new_nbt(tmp[0][1]), command)

		command = re.sub(r'entitydata (@[a-z][A-Za-z0-9=\.,_\-\!\[\]]*|[a-zA-Z0-9_\-\#]+) {}',r'data get entity \1', command)


		#Blockdata
		tmp = re.findall(r'^blockdata ([~\-0-9\.]+ [~\-0-9\.]+ [~\-0-9\.]+) ({.+})', command)
		command = re.sub(r'^blockdata ([~\-0-9\.]+ [~\-0-9\.]+ [~\-0-9\.]+) ({.+})', r'data merge block \1 pl@ceh0ld3r', command)
		if tmp:
			command = re.sub(r'pl@ceh0ld3r', new_nbt(tmp[0][1]), command)

		command = re.sub(r'blockdata (@[a-z][A-Za-z0-9=\.,_\-\!\[\]]*|[a-zA-Z0-9_\-\#]+) {}',r'data get block \1', command)


		#Testforblocks
		command = re.sub(r'^testforblocks ([~\-0-9\.]+ [~\-0-9\.]+ [~\-0-9\.]+ [~\-0-9\.]+ [~\-0-9\.]+ [~\-0-9\.]+ [~\-0-9\.]+ [~\-0-9\.]+ [~\-0-9\.]+) (all|masked)', r'if blocks \1 \2', command)

		#Testfor
		command = re.sub(r'^testfor (@[a-z][A-Za-z0-9=\.,_\-\!\[\]]*|[a-zA-Z0-9_\-\#]+)( {.*})?', r'if entity \1\2', command)

		#Scoreboard test
		tmp = re.findall(r'^scoreboard players test (@[a-z][A-Za-z0-9=\.,_\-\!\[\]]*|[a-zA-Z0-9_\-\#]+) (\S+) ([0-9\*\-]+)(?: )?([0-9\*\-]+)?', command)
		if tmp:
			command = "if score {0} {1} {2} {3}".format(tmp[0][0], tmp[0][1], tmp[0][2], tmp[0][3] if tmp[0][3] else "*")

		#Advancement test
		tmp = re.findall(r'^advancement test (@[a-z][A-Za-z0-9=\.,_\-\!\[\]]*|[a-zA-Z0-9_\-\#]+) ([a-z0-9_/:]+)(?: )?([a-z0-9_/:]+)?', command)
		if tmp:
			selector = tmp[0][0]
			command = "if entity "
			tmp1 = ""
			if len(tmp[0][2]) == 0:
				tmp1 = "advancements={" + tmp[0][1] + "=true}"
			else:
				tmp1 = "advancements={" + tmp[0][1] + "={" + tmp[0][2] +"=true}}"




			if len(selector) > 2:

				command += selector[:-1] + "," + tmp1 + "]"

			else:

				command += selector + "[" + tmp1 + "]"







	except Exception as inst:
		print("[Error] Unknown error in {}".format(filename))
		print(inst)

		return gets


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
			command = "execute "+" ".join(executelist[:-1])+" run "+executelist[-1]
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

			selector_scores = {}


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

				elif arg[0] == "type":
					selector[i] = selector[i].lower()

					#Limit
				elif arg[0] == "c":
					if int(arg[1]) < 0:
						arg[1] = abs(int(arg[1]))
						selector += ["sort=furthest"]
					else:
						selector += ["sort=nearest"]

					selector[i] = "{}={}".format("limit", arg[1])


					#Level
				elif arg[0] == "lm":
					selector_lm = int(arg[1])
					selector[i] = "UNUSED" #Uses UNUSED to prevent changing the list size while iterating
				elif arg[0] == "l":
					selector_l = int(arg[1])
					selector[i] = "UNUSED"

					#Distance
				elif arg[0] == "rm":
					selector_rm = int(arg[1])
					selector[i] = "UNUSED"
				elif arg[0] == "r":
					selector_r = int(arg[1])
					selector[i] = "UNUSED"

					#X rotation
				elif arg[0] == "rxm":
					selector_rxm = int(arg[1])
					selector[i] = "UNUSED"
				elif arg[0] == "rx":
					selector_rx = int(arg[1])
					selector[i] = "UNUSED"

					#Y rotation
				elif arg[0] == "rym":
					selector_rym = int(arg[1])
					selector[i] = "UNUSED"
				elif arg[0] == "ry":
					selector_ry = int(arg[1])
					selector[i] = "UNUSED"

				#Scores
				tmp = re.findall(r'^score_([A-Za-z0-9]+)(_min)?', arg[0])
				if tmp:


					if len(tmp[0][1]) == 0:

						if tmp[0][0] in selector_scores and re.findall(r'^([0-9\-]+)..$', selector_scores[tmp[0][0]]):
							
							if arg[1] + ".." == selector_scores[tmp[0][0]]:
								selector_scores[tmp[0][0]] = arg[1]
							else:
								selector_scores[tmp[0][0]] = selector_scores[tmp[0][0]] + arg[1]

						else:
							selector_scores[tmp[0][0]] = ".." + arg[1]
					
					else:
						if tmp[0][0] in selector_scores and re.findall(r'^..([0-9\-]+)$', selector_scores[tmp[0][0]]):
							
							if ".." + arg[1] == selector_scores[tmp[0][0]]:
								selector_scores[tmp[0][0]] = arg[1]
							else:
								selector_scores[tmp[0][0]] = arg[1] + selector_scores[tmp[0][0]]

						else:
							selector_scores[tmp[0][0]] = arg[1] + ".."

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

			if not selector_scores == {}:

				selector += ["scores={" + ",".join([i+"="+selector_scores[i] for i in selector_scores]) + "}"]



			selector = [i for i in selector if i != "UNUSED"]
			command = re.sub(r'pl@ceh0ld3r', ",".join(selector), command, count=1)

		#Scoreboard NBT selector
		if "scoreboard" in command:


			#scoreboard players tag
			tmp = re.findall(r'scoreboard players tag @([a-z])(\[.*\])? (add|remove) ([\S]+) ({.*})', command)
			command = re.sub(r'scoreboard players tag @([a-z])(\[.*\])? (add|remove) ([\S]+) ({.*})', r'tag @\1pl@ceh0ld3r \3 \4', command)
			if tmp:
				if len(tmp[0][1]) > 0:
					command = re.sub(r'pl@ceh0ld3r', "[{0},nbt={1}]".format(tmp[0][1][1:-1], new_nbt(tmp[0][4])), command)
				else:
					command = re.sub(r'pl@ceh0ld3r', "[nbt={0}]".format(new_nbt(tmp[0][4])), command)
			else:
				command = re.sub(r'scoreboard players tag', r'tag', command)

			#scoreboard players set/add/remove
			tmp = re.findall(r'scoreboard players (set|add|remove) @([a-z])(\[.*\])? ([\S]+) ([0-9]+) ({.*})', command)
			command = re.sub(r'scoreboard players (set|add|remove) @([a-z])(\[.*\])? ([\S]+) ([0-9]+) ({.*})', r'scoreboard players \1 @\2pl@ceh0ld3r \4 \5', command)
			if tmp:
				if len(tmp[0][2]) > 0:
					command = re.sub(r'pl@ceh0ld3r', "[{0},nbt={1}]".format(tmp[0][2][1:-1], new_nbt(tmp[0][5])), command)
				else:
					command = re.sub(r'pl@ceh0ld3r', "[nbt={0}]".format(new_nbt(tmp[0][5])), command)

		#testfor NBT selector and execute command
		if "if entity" in command:

			tmp = re.findall(r'if entity @([a-z])(\[.*\])? ({.*})', command)
			command = re.sub(r'if entity @([a-z])(\[.*\])? ({.*})', r'if entity @\1pl@ceh0ld3r', command)
			if tmp:
				if len(tmp[0][1]) > 0:
					command = re.sub(r'pl@ceh0ld3r', "[{0},nbt={1}]".format(tmp[0][1][1:-1], new_nbt(tmp[0][2])), command)
				else:
					command = re.sub(r'pl@ceh0ld3r', "[nbt={0}]".format(new_nbt(tmp[0][2])), command)

	return command+"\n"


datapack = input("Datapack namespace: ")
tp_new_pos = False
while True:
	print(convert(input().rstrip(), "console"), end="")
