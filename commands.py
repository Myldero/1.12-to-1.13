import os, json, errno, re

#Set values
effect_id = ('speed', 'slowness', 'haste', 'mining_fatigue', 'strength', 'instant_health', 'instant_damage', 'jump_boost', 'nausea', 'regeneration', 'resistance', 'fire_resistance', 'water_breathing', 'invisibility', 'blindness', 'night_vision', 'hunger', 'weakness', 'poison', 'wither', 'health_boost', 'absorption', 'saturation', 'glowing', 'levitation', 'luck', 'unluck')
particles = {'angryVillager': 'angry_villager', 'blockcrack': 'block', 'blockdust': 'dust', 'damageIndicator': 'damage_indicator', 'dragonbreath': 'dragon_breath', 'dripLava': 'drip_lava', 'dripWater': 'drip_water', 'droplet': 'rain', 'enchantmenttable': 'enchant', 'endRod': 'end_rod', 'explode': 'poof', 'fallingdust': 'falling_dust', 'fireworksSpark': 'firework', 'happyVillager': 'happy_villager', 'hugeexplosion': 'explosion_emitter', 'iconcrack': 'item', 'instantSpell': 'instant_effect', 'largeexplode': 'explosion', 'largesmoke': 'large_smoke', 'magicCrit': 'enchanted_hit', 'mobSpell': 'entity_effect', 'mobSpellAmbient': 'ambient_entity_effect', 'mobappearance': 'elder_guardian', 'reddust': 'dust 255 0 0 1', 'slime': 'item_slime', 'snowballpoof': 'item_snowball', 'spell': 'effect', 'suspended': 'underwater', 'sweepAttack': 'sweep_attack', 'totem': 'totem_of_undying', 'townaura': 'mycelium', 'wake': 'fishing', 'witchMagic': 'witch'}
objective_names = {'drop': 'drop', 'swimOneCm': 'swim_one_cm', 'walkOneCm': 'walk_one_cm', 'recordPlayed': 'play_record', 'noteblockPlayed': 'play_noteblock', 'deaths': 'deaths', 'leaveGame': 'leave_game', 'damageDealt': 'damage_dealt', 'fishCaught': 'fish_caught', 'trappedChestTriggered': 'trigger_trapped_chest', 'tradedWithVillager': 'traded_with_villager', 'playerKills': 'player_kills', 'damageTaken': 'damage_taken', 'sneakTime': 'sneak_time', 'flowerPotted': 'pot_flower', 'playOneMinute': 'play_one_minute', 'enderchestOpened': 'open_enderchest', 'armorCleaned': 'clean_armor', 'aviateOneCm': 'aviate_one_cm', 'beaconInteraction': 'interact_with_beacon', 'pigOneCm': 'pig_one_cm', 'craftingTableInteraction': 'interact_with_crafting_table', 'sleepInBed': 'sleep_in_bed', 'talkedToVillager': 'talked_to_villager', 'brewingstandInteraction': 'interact_with_brewingstand', 'cakeSlicesEaten': 'eat_cake_slice', 'flyOneCm': 'fly_one_cm', 'chestOpened': 'open_chest', 'furnaceInteraction': 'interact_with_furnace', 'hopperInspected': 'inspect_hopper', 'horseOneCm': 'horse_one_cm', 'animalsBred': 'animals_bred', 'shulkerBoxOpened': 'open_shulker_box', 'jump': 'jump', 'dropperInspected': 'inspect_dropper', 'climbOneCm': 'climb_one_cm', 'timeSinceDeath': 'time_since_death', 'bannerCleared': 'clean_banner', 'mobKills': 'mob_kills', 'cauldronFilled': 'fill_cauldron', 'itemEnchanted': 'enchant_item', 'crouchOneCm': 'crouch_one_cm', 'sprintOneCm': 'sprint_one_cm', 'fallOneCm': 'fall_one_cm', 'cauldronUsed': 'use_cauldron', 'noteblockTuned': 'tune_noteblock', 'minecartOneCm': 'minecart_one_cm', 'boatOneCm': 'boat_one_cm', 'diveOneCm': 'dive_one_cm'}
entity_names = {'Item': 'item', 'XPOrb': 'xp_orb', 'LeashKnot': 'leash_knot', 'Enderman': 'enderman', 'Endermite': 'endermite', 'Horse': 'horse', 'LavaSlime': 'magma_cube', 'WitherSkeleton': 'wither_skeleton', 'EyeOfEnderSignal': 'eye_of_ender_signal', 'FallingSand': 'falling_block', 'MinecartRideable': 'minecart', 'Spider': 'spider', 'MinecartSpawner': 'spawner_minecart', 'MushroomCow': 'mooshroom', 'Guardian': 'guardian', 'Skeleton': 'skeleton', 'ThrownExpBottle': 'xp_bottle', 'EnderDragon': 'ender_dragon', 'Witch': 'witch', 'Arrow': 'arrow', 'Snowball': 'snowball', 'EnderCrystal': 'ender_crystal', 'Zombie': 'zombie', 'Giant': 'giant', 'ArmorStand': 'armor_stand', 'ThrownEnderpearl': 'ender_pearl', 'CaveSpider': 'cave_spider', 'Silverfish': 'silverfish', 'WitherBoss': 'wither', 'Bat': 'bat', 'ElderGuardian': 'elder_guardian', 'Donkey': 'donkey', 'ItemFrame': 'item_frame', 'Cow': 'cow', 'SmallFireball': 'small_fireball', 'ThrownEgg': 'egg', 'Shulker': 'shulker', 'MinecartFurnace': 'furnace_minecart', 'WitherSkull': 'wither_skull', 'Creeper': 'creeper', 'Villager': 'villager', 'ZombieHorse': 'zombie_horse', 'Fireball': 'fireball', 'SpectralArrow': 'spectral_arrow', 'MinecartHopper': 'hopper_minecart', 'Painting': 'painting', 'Blaze': 'blaze', 'Chicken': 'chicken', 'DragonFireball': 'dragon_fireball', 'Squid': 'squid', 'PrimedTnt': 'tnt', 'SnowMan': 'snowman', 'ThrownPotion': 'potion', 'ZombieVillager': 'zombie_villager', 'Slime': 'slime', 'Mule': 'mule', 'MinecartChest': 'chest_minecart', 'VillagerGolem': 'villager_golem', 'PolarBear': 'polar_bear', 'PigZombie': 'zombie_pigman', 'SkeletonHorse': 'skeleton_horse', 'Ghast': 'ghast', 'Husk': 'husk', 'MinecartTNT': 'tnt_minecart', 'Boat': 'boat', 'Rabbit': 'rabbit', 'FireworksRocketEntity': 'fireworks_rocket', 'AreaEffectCloud': 'area_effect_cloud', 'MinecartCommandBlock': 'commandblock_minecart', 'Ozelot': 'ocelot', 'Stray': 'stray', 'Wolf': 'wolf', 'ShulkerBullet': 'shulker_bullet', 'Pig': 'pig', 'Sheep': 'sheep'}
enchanting = {0: 'minecraft:protection', 1: 'minecraft:fire_protection', 2: 'minecraft:feather_falling', 3: 'minecraft:blast_protection', 4: 'minecraft:projectile_protection', 5: 'minecraft:respiration', 6: 'minecraft:aqua_affinity', 7: 'minecraft:thorns', 8: 'minecraft:depth_strider', 9: 'minecraft:frost_walker', 10: 'minecraft:binding_curse', 66: 'minecraft:impaling', 16: 'minecraft:sharpness', 17: 'minecraft:smite', 18: 'minecraft:bane_of_arthropods', 19: 'minecraft:knockback', 20: 'minecraft:fire_aspect', 21: 'minecraft:looting', 22: 'minecraft:sweeping', 68: 'minecraft:channeling', 71: 'minecraft:vanishing_curse', 32: 'minecraft:efficiency', 33: 'minecraft:silk_touch', 34: 'minecraft:unbreaking', 35: 'minecraft:fortune', 70: 'minecraft:mending', 65: 'minecraft:loyalty', 67: 'minecraft:riptide', 48: 'minecraft:power', 49: 'minecraft:punch', 50: 'minecraft:flame', 51: 'minecraft:infinity', 61: 'minecraft:luck_of_the_sea', 62: 'minecraft:lure'}

blockstates = dict(line.rstrip().split(":", 1) for line in open(os.path.join(".", "blockstates.txt"), 'r') if line.count(":") > 0)
blockstates_other = dict(line.rstrip().split(" ", 1) for line in open(os.path.join(".", "blockstates_other.txt"), 'r') if line.count(" ") > 0)
itemvalues = dict(line.rstrip().split(":", 1) for line in open(os.path.join(".", "itemvalues.txt"), 'r') if line.count(":") > 0)

colors = ['white', 'orange', 'magenta', 'light_blue', 'yellow', 'lime', 'pink', 'gray', 'light_gray', 'cyan', 'purple', 'blue', 'brown', 'green', 'red', 'black']
skulls = ['skeleton_skull', 'wither_skeleton_skull', 'zombie_head', 'player_head', 'creeper_head', 'dragon_head']
wall_skulls = ['skeleton_wall_skull', 'wither_skeleton_wall_skull', 'zombie_wall_head', 'player_wall_head', 'creeper_wall_head', 'dragon_wall_head']
flowers = {'red_flower 0': 'poppy', 'yellow_flower 0': 'dandelion', 'sapling 0': 'oak_sapling', 'sapling 1': 'spruce_sapling', 'sapling 2': 'birch_sapling', 'sapling 3': 'jungle_sapling', 'red_mushroom 0': 'red_mushroom', 'brown_mushroom 0': 'brown_mushroom', 'cactus 0': 'cactus', 'deadbush 0': 'dead_bush', 'tallgrass 2': 'fern', 'sapling 4': 'acacia_sapling', 'sapling 5': 'dark_oak_sapling', 'red_flower 1': 'blue_orchid', 'red_flower 2': 'allium', 'red_flower 3': 'azure_bluet', 'red_flower 4': 'red_tulip', 'red_flower 5': 'orange_tulip', 'red_flower 6': 'white_tulip', 'red_flower 7': 'pink_tulip', 'red_flower 8': 'oxeye_daisy'}
mobs = ['bat', 'blaze', 'cave_spider', 'chicken', 'cow', 'creeper', 'donkey', 'elder_guardian', 'enderman', 'endermite', 'evocation_illager', 'ghast', 'guardian', 'horse', 'husk', 'llama', 'magma_cube', 'mooshroom', 'mule', 'ocelot', 'parrot', 'pig', 'polar_bear', 'rabbit', 'sheep', 'shulker', 'silverfish', 'skeleton', 'skeleton_horse', 'slime', 'spider', 'squid', 'stray', 'vex', 'villager', 'vindication_illager', 'witch', 'wither_skeleton', 'wolf', 'zombie', 'zombie_horse', 'zombie_pigman', 'zombie_villager']

def change_block(block, data="", nbt="", use_tags=True):
	block = block.lower()

	if data.isdigit():
		data = int(data)
	elif len(data) == 0:
		data = 0

	elif data not in ['-1','*']: #Just to take everything where there's already been used something like "color=red"
		tmp = data
		data = 0

		if block in blockstates_other:

			default, *states = blockstates_other[block].split()

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


	#Block State
	if data in ['-1','*'] and (block in blockstates or block == "flower_pot"):
		
		if block == "skull":
			all_blocks = ["minecraft:" + i for i in skulls + wall_skulls]
		
		elif block == "banner":
			all_blocks = ["minecraft:" + i + "_banner" for i in colors]
			all_blocks = ["minecraft:" + i + "_wall_banner" for i in colors]
		
		elif block == "bed":
			all_blocks = ["minecraft:" + i + "_bed" for i in colors]
		
		elif block == "flower_pot":
			all_blocks = ["minecraft:potted_" + flowers[i] for i in flowers]

		else:
			all_blocks = list(set(["minecraft:" + re.findall(r'^[a-z_]+', i)[0] for i in blockstates[block].split() if re.findall(r'^[a-z_]', i)]))

		if len(all_blocks) > 1:

			if use_tags == False:
				return "#"


			if block == "wool":
				block = "#minecraft:wool"
			
			elif 'worldpath' in globals(): #This var is only created in run.py

				filepath = os.path.join(worldpath, "datapacks", datapack, "data", datapack, "tags", "blocks", block+".json")

				try:
				    open(filepath, 'r')
				except IOError:
				    
					with open(filepath, 'w+') as f:
						f.write( json.dumps( {"values": all_blocks} , indent=4) )

				block = "#{}:{}".format(datapack, block)

			else:
				block = "#{}:{}".format(datapack, block)
		else:
			block = re.sub(r'^minecraft:', r'', all_blocks[0])


		
	elif isinstance(data, int):
		
		if block in blockstates:
			states = blockstates[block].split() #Gets list of block states

			if states[data % len(states)].isdigit():
				block = states[ int(states[data % len(states)]) ]
			else:
				block = states[data % len(states)] #This picks the correct block state

		#Special cases (love those)
		if block.startswith("skull"):
			
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
			
			color = 0

			tmp = re.findall(r'Base:([0-9]+)', nbt)
			if tmp:
				color = 15 - int(tmp[0][0])

				nbt = re.sub(r'(,)?Base:([0-9])(b)?(,)?', r',', nbt)
				nbt = re.sub(r'^{,', r'{', nbt)
				nbt = re.sub(r',}$', r'}', nbt)


			block = colors[color] + "_" + block

		elif block.startswith("bed"):
			
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

			flower_id = "air"
			flower_data = 0

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
		block += new_nbt(nbt)

	return block

def change_item(item, data, nbt, use_tags=True):
	item = item.lower()

	if re.findall(r'^[0-9\-]+$', data):
		data = int(data)
	elif data == '*':
		data = -1
	elif len(data) == 0:
		data = 0

	if len(nbt) > 2:
		nbt = new_nbt(nbt)

	if any(item.endswith(i) for i in ("filled_map","shield","sword","shovel","pickaxe","hoe","axe","flint_and_steel","helmet","chestplate","leggings","boots","bow","fishing_rod","shears")):
		if data != -1:
			item += "{Damage:"+str(data)+"s"

			if len(nbt) > 0:
				item += ","+nbt[1:]
			else:
				item += "}"

			return item
	
	elif data == -1 and (item in itemvalues or item == "spawn_egg"):

		if item == "spawn_egg":
			all_items = ["minecraft:" + i + "_spawn_egg" for i in mobs]
		else:
			all_items = list(set(["minecraft:" + re.findall(r'^[a-z_]+', i)[0] for i in itemvalues[item].split()]))

		if len(all_items) > 1:

			if use_tags == False:
				return "#"


			if item == "wool":
				return "#minecraft:wool" + nbt
			
			elif 'worldpath' in globals(): #This var is only created in run.py

				filepath = os.path.join(worldpath, "datapacks", datapack, "data", datapack, "tags", "items", item+".json")

				try:
				    open(filepath, 'r')
				except IOError:
				    
					with open(filepath, 'w+') as f:
						f.write( json.dumps( {"values": all_items} , indent=4) )

				return "#{}:{}".format(datapack, item) + nbt

			else:
				return "#{}:{}".format(datapack, item) + nbt
		else:
			return re.sub(r'^minecraft:', r'', all_items[0]) + nbt


	elif item == "spawn_egg":

		tmp = re.findall(r'entitytag:{id:(?:\")?(?:minecraft:)?([a-z_]+)', nbt.lower())
		if tmp:
			return tmp[0] + "_" + item

	else:
		if item in itemvalues:
			values = itemvalues[item].split()

			return values[data % len(values)] + nbt #Returns the correct item and nbt concatenated


	return item + nbt #Returns the item and nbt concatenated

def change_objective(criteria):
	
	if criteria.startswith("stat."):
		criteria = criteria.split(".")

		if len(criteria) == 2:
			return "minecraft.custom:minecraft.{}".format(objective_names[criteria[1]])
		else:
			*c_type, c = criteria
			c_type = ".".join(c_type)

			if c_type == "stat.craftItem.minecraft":
				return "minecraft.crafted:minecraft.{}".format(change_item(c, "*", "", use_tags=False))

			elif c_type == "stat.useItem.minecraft":
				return "minecraft.used:minecraft.{}".format(change_item(c, "*", "", use_tags=False))

			elif c_type == "stat.breakItem.minecraft":
				return "minecraft.broken:minecraft.{}".format(change_item(c, "*", "", use_tags=False))

			elif c_type == "stat.mineBlock.minecraft":
				return "minecraft.mined:minecraft.{}".format(change_block(c, "*", "", use_tags=False))

			elif c_type == "stat.killEntity":
				return "minecraft.killed:minecraft.{}".format(entity_names[c])

			elif c_type == "stat.pickup.minecraft":
				return "minecraft.picked_up:minecraft.{}".format(change_item(c, "*", "", use_tags=False))

			elif c_type == "stat.drop.minecraft":
				return "minecraft.dropped:minecraft.{}".format(change_item(c, "*", "", use_tags=False))

			elif c_type == "stat.entityKilledBy":
				return "minecraft.killed_by:minecraft.{}".format(entity_names[c])

	else:
		return criteria




def get_item_nbt(nbt, nbt_type):

	'''
	Gets the values of an item inputted in NBT, so it can convert it.
	'''

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



			item, start_nbt, end_nbt = change_item(item_nbt["id"], item_nbt["Damage"], item_nbt["tag"], use_tags=False), match_index+len(nbt_type)+1, end_index

			if item.startswith("#"):
				item = item_nbt["id"]
				print("[Info] NBT in {} contains a block/item name that cannot be translated".format(filename))

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

	'''
	Finds a list in NBT in which to update 
	'''

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

				block = re.findall(r'(?:minecraft:)?([a-z_]+)|$',nbt_list[i])[0]
				
				if block in blockstates:
					states = ["minecraft:"+i for i in set(re.findall(r'(?:^| )([a-z_]+)', blockstates[block]))] #Gets list of unique block names

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

		elif nbt_type == "ench:":

			for i in range(len(nbt_list)):

				enchid = re.findall(r'id:([0-9]+)|$',nbt_list[i])[0]
				enchlvl = re.findall(r'lvl:([0-9]+)|$',nbt_list[i])[0]

				if enchid != '' and enchlvl != '':
					nbt_list[i] = "{id:\""+ enchanting[int(enchid)] + "\",lvl:"+enchlvl+"}"




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

	nbt = get_nbt_list(nbt, "ench:")

	nbt = nbt.replace("ench:[","Enchantments:[")

	return nbt




def get_executes(command):
	global executelist
	global precommand

	if command.startswith("/"):
		command = command[1:]

	if command.startswith("execute"):
		tmp = re.findall(r'^execute (@[a-z][A-Za-z0-9=\.,_\-\!\[\]]*|[a-zA-Z0-9_\-\#]+) ([~\-0-9\.]+ [~\-0-9\.]+ [~\-0-9\.]+) (.+)', command)
		if tmp:
			executelist += [re.findall(r'^execute (?:@[a-z][A-Za-z0-9=\.,_\-\!\[\]]*|[a-zA-Z0-9_\-\#]+) [~\-0-9\.]+ [~\-0-9\.]+ [~\-0-9\.]+',command)[0]]
			get_executes(tmp[0][2])

	elif command.startswith("detect"):

		tmp = re.findall(r'^detect ([~\-0-9\.]+ [~\-0-9\.]+ [~\-0-9\.]+) (?:minecraft\:)?([a-zA-Z_]+) ([\S]+) (.+)', command)
		if tmp:
			executelist += [re.findall(r'^detect [~\-0-9\.]+ [~\-0-9\.]+ [~\-0-9\.]+ (?:minecraft\:)?[a-zA-Z_]+ [\S]+', command)[0]]
			get_executes(tmp[0][3])


		#The following commands need execute so they need to be converted here already
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
	elif command.startswith("scoreboard players test"):

		#Scoreboard test
		

		tmp = re.findall(r'^scoreboard players test (@[a-z][A-Za-z0-9=\.,_\-\!\[\]]*) (\S+) ([0-9\*\-]+)(?: )?([0-9\*\-]+)?', command)
		if tmp:
			selector = tmp[0][0]
			tmp1 = []

			if "*" not in tmp[0][2] and len(tmp[0][2]) > 0:
				tmp1 += ["score_{}_min={}".format(tmp[0][1], tmp[0][2])]

			if "*" not in tmp[0][3] and len(tmp[0][3]) > 0:
				tmp1 += ["score_{}={}".format(tmp[0][1], tmp[0][3])]



			if tmp1:
				if re.findall(r'^@[a-z]$', selector):
					selector += "[{}]".format(",".join(tmp1))
				elif re.findall(r'^@[a-z]\[\]$', selector):
					selector = selector[:-1] + "{}]".format(",".join(tmp1))
				elif re.findall(r'^@[a-z]\[\S+\]$', selector):
					selector = selector[:-1] + ",{}]".format(",".join(tmp1))

			executelist += ["if entity {0}".format(selector)]
		else:
			tmp = re.findall(r'^scoreboard players test ([a-zA-Z0-9_\-\#]+) (\S+) ([0-9\*\-]+)(?: )?([0-9\*\-]+)?', command)
			if tmp:

				if tmp[0][2] == tmp[0][3] and tmp[0][2] != "*" and len(tmp[0][2]) > 0:
					executelist += ["if score {0} {1} matches {2}".format(tmp[0][0], tmp[0][1], tmp[0][2])]

				elif tmp[0][2] != "*" and len(tmp[0][2]) > 0 and (len(tmp[0][3]) == 0 or tmp[0][3] == "*"):
					executelist += ["if score {0} {1} matches {2}..".format(tmp[0][0], tmp[0][1], tmp[0][2])]

				elif tmp[0][3] != "*" and len(tmp[0][3]) > 0 and (len(tmp[0][2]) == 0 or tmp[0][2] == "*"):
					executelist += ["if score {0} {1} matches ..{2}".format(tmp[0][0], tmp[0][1], tmp[0][3])]

				elif tmp[0][2] != "*" and len(tmp[0][2]) > 0 and tmp[0][3] != "*" and len(tmp[0][3]) > 0:
					executelist += ["if score {0} {1} matches {2}..{3}".format(tmp[0][0], tmp[0][1], tmp[0][2],tmp[0][3])]

	else:
		executelist += [command]

def convert_command(gets):
	command = gets
	try:

		if command.startswith("toggledownfall"):
			#Toggledownfall to weather clear
			command = re.sub(r'^toggledownfall', r'weather clear', command)
		
		elif command.startswith("gamemode"):
			#Gamemode
			command = re.sub(r'^gamemode (0|s)',r'gamemode survival',command)
			command = re.sub(r'^gamemode (1|c)',r'gamemode creative',command)
			command = re.sub(r'^gamemode (2|a)',r'gamemode adventure',command)
			command = re.sub(r'^gamemode (3|sp)',r'gamemode spectator',command)
		
		elif command.startswith("difficulty"):

			#Difficulty
			command = re.sub(r'^difficulty (0|p)',r'difficulty peaceful',command)
			command = re.sub(r'^difficulty (1|e)',r'difficulty easy',command)
			command = re.sub(r'^difficulty (2|n)',r'difficulty normal',command)
			command = re.sub(r'^difficulty (3|h)',r'difficulty hard',command)
		
		elif command.startswith("teleport"):
			#Teleport to tp (Sorry if this will be confusing)
			command = re.sub(r'^teleport',r'tp', command)

		elif command.startswith("xp"):

			command = re.sub(r'^xp ([\-0-9]+)L (@[a-z][A-Za-z0-9=\.,_\-\!\[\]]*|[a-zA-Z0-9_\-\#]+)', r'xp add \2 \1 levels',command)
			command = re.sub(r'^xp ([\-0-9]+)L', r'xp add @s \1 levels',command)
			command = re.sub(r'^xp ([\-0-9]+) (@[a-z][A-Za-z0-9=\.,_\-\!\[\]]*|[a-zA-Z0-9_\-\#]+)', r'xp add \2 \1 points',command)
			command = re.sub(r'^xp ([\-0-9]+)', r'xp add @s \1 points',command)
		
		elif command.startswith("scoreboard teams"):
			#Teams now
			command = re.sub(r'^scoreboard teams', r'team', command)

		elif command.startswith("scoreboard objectives"):
			tmp = re.findall(r'^scoreboard objectives add (\S+) ([A-Za-z0-9\.\-_]+)', command)
			if tmp:
				criteria = change_objective(tmp[0][1])

				if "#" not in criteria:
					command = re.sub(r'^scoreboard objectives add (\S+) ([A-Za-z0-9\.\-_]+)', r'scoreboard objectives add \1 '+ criteria, command)
				else:
					print("[Info] Objective in {} contains a block/item name that cannot be translated".format(filename))


		elif command.startswith("particle"):

			#Particles
			tmp = re.findall(r'^particle (?:minecraft\:)?([a-zA-Z0-9_]+)', command)
			if tmp:
				command = re.sub(r'^particle (?:minecraft\:)?([a-zA-Z0-9_]+)', r'particle minecraft:pl@ceh0ld3r', command)
				if tmp[0] in particles:
					command = re.sub(r'pl@ceh0ld3r', particles[tmp[0]], command)
				else:
					command = re.sub(r'pl@ceh0ld3r', tmp[0], command)
		


		#Give, clear and replaceitem
		elif command.startswith("give"):

			tmp = re.findall(r'^give (@[a-z][A-Za-z0-9=\.,_\-\!\[\]]*|[a-zA-Z0-9_\-\#]+) (?:minecraft\:)?([A-Za-z_]+)(?: )?([0-9]+)?(?: )?([0-9]+)?(?: )?({.*})?', command)
			if tmp:
				command = re.sub(r'^give (@[a-z][A-Za-z0-9=\.,_\-\!\[\]]*|[a-zA-Z0-9_\-\#]+) (?:minecraft\:)?([A-Za-z_]+)(?: )?([0-9]+)?(?: )?([0-9]+)?(?: )?({.*})?', r'give \1 pl@ceh0ld3r \3', command)
				command = re.sub(r'pl@ceh0ld3r', change_item(tmp[0][1], tmp[0][3], tmp[0][4]), command)

		elif command.startswith("clear"):

			tmp = re.findall(r'^clear (@[a-z][A-Za-z0-9=\.,_\-\!\[\]]*|[a-zA-Z0-9_\-\#]+) (?:minecraft\:)?([A-Za-z_]+)(?: )?([0-9\-\*]+)?(?: )?([0-9\-\*]+)?(?: )?({.*})?', command)
			if tmp:
				command = re.sub(r'^clear (@[a-z][A-Za-z0-9=\.,_\-\!\[\]]*|[a-zA-Z0-9_\-\#]+) (?:minecraft\:)?([A-Za-z_]+)(?: )?([0-9\-\*]+)?(?: )?([0-9\-\*]+)?(?: )?({.*})?', r'clear \1 pl@ceh0ld3r pl@ceh0ld2r', command)
				command = re.sub(r'pl@ceh0ld3r', change_item(tmp[0][1], tmp[0][2] if tmp[0][2] else "*", tmp[0][4]), command)
				command = re.sub(r'pl@ceh0ld2r', tmp[0][3] if tmp[0][3].isdigit() else "", command)


		elif command.startswith("replaceitem"):

			tmp = re.findall(r'^replaceitem entity (@[a-z][A-Za-z0-9=\.,_\-\!\[\]]*|[a-zA-Z0-9_\-\#]+) slot\.([a-z0-9\.]+) (?:minecraft\:)?([A-Za-z_]+)(?: )?([0-9]+)?(?: )?([0-9]+)?(?: )?({.*})?', command)
			if tmp:
				command = re.sub(r'^replaceitem entity (@[a-z][A-Za-z0-9=\.,_\-\!\[\]]*|[a-zA-Z0-9_\-\#]+) slot\.([a-z0-9\.]+) (?:minecraft\:)?([A-Za-z_]+)(?: )?([0-9]+)?(?: )?([0-9]+)?(?: )?({.*})?', r'replaceitem entity \1 \2 pl@ceh0ld3r \4', command)
				command = re.sub(r'pl@ceh0ld3r', change_item(tmp[0][2], tmp[0][4], tmp[0][5]), command)
			else:
				tmp = re.findall(r'^replaceitem block ([~\-0-9\.]+ [~\-0-9\.]+ [~\-0-9\.]+) slot\.([a-z0-9\.]+) (?:minecraft\:)?([A-Za-z_]+)(?: )?([0-9]+)?(?: )?([0-9]+)?(?: )?({.*})?', command)
				if tmp:
					command = re.sub(r'^replaceitem block ([~\-0-9\.]+ [~\-0-9\.]+ [~\-0-9\.]+) slot\.([a-z0-9\.]+) (?:minecraft\:)?([A-Za-z_]+)(?: )?([0-9]+)?(?: )?([0-9]+)?(?: )?({.*})?', r'replaceitem block \1 \2 pl@ceh0ld3r \4', command)
					command = re.sub(r'pl@ceh0ld3r', change_item(tmp[0][2], tmp[0][4], tmp[0][5]), command)



		#Effect command
		elif command.startswith("effect"):

			#Effect ID's
			tmp = re.findall(r'^effect (@[a-z][A-Za-z0-9=\.,_\-\!\[\]]*|[a-zA-Z0-9_\-\#]+) (?:minecraft\:)?(speed|slowness|haste|mining_fatigue|strength|instant_health|instant_damage|jump_boost|nausea|regeneration|resistance|fire_resistance|water_breathing|invisibility|blindness|night_vision|hunger|weakness|poison|wither|health_boost|absorption|saturation|glowing|levitation|luck|unluck)', command)
			if tmp:
				command = re.sub(r'^effect (@[a-z][A-Za-z0-9=\.,_\-\!\[\]]*|[a-zA-Z0-9_\-\#]+) (?:minecraft\:)?(speed|slowness|haste|mining_fatigue|strength|instant_health|instant_damage|jump_boost|nausea|regeneration|resistance|fire_resistance|water_breathing|invisibility|blindness|night_vision|hunger|weakness|poison|wither|health_boost|absorption|saturation|glowing|levitation|luck|unluck)', r'effect \1 pl@ceh0ld3r', command)
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


		#Block states instead of data values. It will just copy states over if they were already used
		elif command.startswith("setblock"):
			tmp = re.findall(r'^setblock ([~\-0-9\.]+ [~\-0-9\.]+ [~\-0-9\.]+) (?:minecraft\:)?([A-Za-z_]+)(?: )?([\S]+)?(?: )?(destroy|keep|replace)?(?: )?({.+})?', command)
			command = re.sub(r'^setblock ([~\-0-9\.]+ [~\-0-9\.]+ [~\-0-9\.]+) (?:minecraft\:)?([A-Za-z_]+)(?: )?([\S]+)?(?: )?(destroy|keep|replace)?(?: )?({.+})?', r'setblock \1 pl@ceh0ld3r \4', command)
			if tmp:
				command = re.sub(r'pl@ceh0ld3r', change_block(tmp[0][1], tmp[0][2] if tmp[0][2] else "default", tmp[0][4]), command)

		elif command.startswith("testforblock "):
			tmp = re.findall(r'^testforblock ([~\-0-9\.]+ [~\-0-9\.]+ [~\-0-9\.]+) (?:minecraft\:)?([A-Za-z_]+)(?: )?([\S]+)?(?: )?({.*})?', command)
			command = re.sub(r'^testforblock ([~\-0-9\.]+ [~\-0-9\.]+ [~\-0-9\.]+) (?:minecraft\:)?([A-Za-z_]+)(?: )?([\S]+)?(?: )?({.*})?', r'if block \1 pl@ceh0ld3r', command)
			if tmp:
				data = tmp[0][2]
				if data == "":
					data = "*"


				command = re.sub(r'pl@ceh0ld3r', change_block(tmp[0][1], data, tmp[0][3]), command)

		elif command.startswith("fill"):
			#Fill replace
			tmp = re.findall(r'^fill ([~\-0-9\.]+ [~\-0-9\.]+ [~\-0-9\.]+ [~\-0-9\.]+ [~\-0-9\.]+ [~\-0-9\.]+) (?:minecraft\:)?([A-Za-z_]+) ([\S]+) replace (?:minecraft\:)?([A-Za-z_]+)(?: )?([\S]+)?', command)
			command = re.sub(r'^fill ([~\-0-9\.]+ [~\-0-9\.]+ [~\-0-9\.]+ [~\-0-9\.]+ [~\-0-9\.]+ [~\-0-9\.]+) (?:minecraft\:)?([A-Za-z_]+) ([\S]+) replace (?:minecraft\:)?([A-Za-z_]+)(?: )?([\S]+)?', r'fill \1 pl@ceh0ld3r replace pl@ceh0ld2r', command)
			if tmp:
				command = re.sub(r'pl@ceh0ld3r', change_block(tmp[0][1], tmp[0][2] if tmp[0][2] else "default", ""), command)
				command = re.sub(r'pl@ceh0ld2r', change_block(tmp[0][3], tmp[0][4] if tmp[0][4] else "default", ""), command)
			else:
				#Fill normal
				tmp = re.findall(r'^fill ([~\-0-9\.]+ [~\-0-9\.]+ [~\-0-9\.]+ [~\-0-9\.]+ [~\-0-9\.]+ [~\-0-9\.]+) (?:minecraft\:)?([A-Za-z_]+) ([\S]+)(?: )?(destroy|hollow|keep|outline|replace)?(?: )?({.+})?', command)
				command = re.sub(r'^fill ([~\-0-9\.]+ [~\-0-9\.]+ [~\-0-9\.]+ [~\-0-9\.]+ [~\-0-9\.]+ [~\-0-9\.]+) (?:minecraft\:)?([A-Za-z_]+) ([\S]+)(?: )?(destroy|hollow|keep|outline|replace)?(?: )?({.+})?', r'fill \1 pl@ceh0ld3r \4', command)
				if tmp:
					command = re.sub(r'pl@ceh0ld3r', change_block(tmp[0][1], tmp[0][2], tmp[0][4]), command)
				else:
					tmp = re.findall(r'^fill ([~\-0-9\.]+ [~\-0-9\.]+ [~\-0-9\.]+ [~\-0-9\.]+ [~\-0-9\.]+ [~\-0-9\.]+) (?:minecraft\:)?([A-Za-z_]+)', command)
					command = re.sub(r'^fill ([~\-0-9\.]+ [~\-0-9\.]+ [~\-0-9\.]+ [~\-0-9\.]+ [~\-0-9\.]+ [~\-0-9\.]+) (?:minecraft\:)?([A-Za-z_]+)', r'fill \1 pl@ceh0ld3r', command)
					if tmp:
						command = re.sub(r'pl@ceh0ld3r', change_block(tmp[0][1], "default", ""), command)



		elif command.startswith("clone"):
			#Filtered clone
			tmp = re.findall(r'^clone ([~\-0-9\.]+ [~\-0-9\.]+ [~\-0-9\.]+ [~\-0-9\.]+ [~\-0-9\.]+ [~\-0-9\.]+ [~\-0-9\.]+ [~\-0-9\.]+ [~\-0-9\.]+) (filtered|replace|masked) (force|move|normal) (?:minecraft\:)?([A-Za-z_]+)(?: )?([\S]+)?', command)
			command = re.sub(r'^clone ([~\-0-9\.]+ [~\-0-9\.]+ [~\-0-9\.]+ [~\-0-9\.]+ [~\-0-9\.]+ [~\-0-9\.]+ [~\-0-9\.]+ [~\-0-9\.]+ [~\-0-9\.]+) (filtered|replace|masked) (force|move|normal) (?:minecraft\:)?([A-Za-z_]+)(?: )?([\S]+)?', r'clone \1 filtered \3 pl@ceh0ld3r', command)
			if tmp:
				command = re.sub(r'pl@ceh0ld3r', change_block(tmp[0][3], tmp[0][4], ""), command)

		elif command.startswith("summon"):
			#Entity NBT
			tmp = re.findall(r'^summon (minecraft\:)?([A-Za-z_]+)', command)
			command = re.sub(r'^summon (minecraft\:)?([A-Za-z_]+)', r'summon \1pl@ceh0ld3r', command)
			if tmp:
				command = re.sub(r'pl@ceh0ld3r', tmp[0][1].lower(), command)


			command = re.sub(r'^summon (minecraft\:)?([A-Za-z_]+) ({.*})', r'summon \1\2 ~ ~ ~ \3', command)

			tmp = re.findall(r'^summon (minecraft\:)?([A-Za-z_]+) ([~\-0-9\.]+ [~\-0-9\.]+ [~\-0-9\.]+) ({.*})', command)
			command = re.sub(r'^summon (minecraft\:)?([A-Za-z_]+) ([~\-0-9\.]+ [~\-0-9\.]+ [~\-0-9\.]+) ({.*})', r'summon \1\2 \3 pl@ceh0ld3r', command)
			if tmp:
				command = re.sub(r'pl@ceh0ld3r', new_nbt(tmp[0][3]), command)

		elif command.startswith("entitydata"):
			#Entitydata
			tmp = re.findall(r'^entitydata (@[a-z][A-Za-z0-9=\.,_\-\!\[\]]*|[a-zA-Z0-9_\-\#]+) ({.+})', command)
			command = re.sub(r'^entitydata (@[a-z][A-Za-z0-9=\.,_\-\!\[\]]*|[a-zA-Z0-9_\-\#]+) ({.+})', r'data merge entity \1 pl@ceh0ld3r', command)
			if tmp:
				command = re.sub(r'pl@ceh0ld3r', new_nbt(tmp[0][1]), command)

			command = re.sub(r'entitydata (@[a-z][A-Za-z0-9=\.,_\-\!\[\]]*|[a-zA-Z0-9_\-\#]+) {}',r'data get entity \1', command)

		elif command.startswith("blockdata"):
			#Blockdata
			tmp = re.findall(r'^blockdata ([~\-0-9\.]+ [~\-0-9\.]+ [~\-0-9\.]+) ({.+})', command)
			command = re.sub(r'^blockdata ([~\-0-9\.]+ [~\-0-9\.]+ [~\-0-9\.]+) ({.+})', r'data merge block \1 pl@ceh0ld3r', command)
			if tmp:
				command = re.sub(r'pl@ceh0ld3r', new_nbt(tmp[0][1]), command)

			command = re.sub(r'blockdata (@[a-z][A-Za-z0-9=\.,_\-\!\[\]]*|[a-zA-Z0-9_\-\#]+) {}',r'data get block \1', command)

		elif command.startswith("testforblocks"):

			#Testforblocks
			command = re.sub(r'^testforblocks ([~\-0-9\.]+ [~\-0-9\.]+ [~\-0-9\.]+ [~\-0-9\.]+ [~\-0-9\.]+ [~\-0-9\.]+ [~\-0-9\.]+ [~\-0-9\.]+ [~\-0-9\.]+) (all|masked)', r'if blocks \1 \2', command)

		elif command.startswith("testfor "):
			#Testfor
			command = re.sub(r'^testfor (@[a-z][A-Za-z0-9=\.,_\-\!\[\]]*|[a-zA-Z0-9_\-\#]+)( {.*})?', r'if entity \1\2', command)

		elif command.startswith("advancement"):
			#Update advancement path
			tmp = re.findall(r'^advancement (.*) minecraft:([A-Za-z0-9_\-/]+)', command)
			if tmp:
				command = re.sub(r'^advancement (.*) minecraft:([A-Za-z0-9_\-/]+)', r'advancement \1 minecraft:{}'.format(tmp[0][1].lower()), command)
			else:
				tmp = re.findall(r'^advancement (.*) ([A-Za-z0-9_\-]+):([A-Za-z0-9_\-/]+)', command)
				if tmp:
					command = re.sub(r'^advancement (.*) ([A-Za-z0-9_\-]+):([A-Za-z0-9_\-/]+)', r'advancement \1 {}:{}/{}'.format(datapack, tmp[0][1].lower(), tmp[0][2].lower()), command)

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

				if len(selector) > 4:
					command += selector[:-1] + "," + tmp1 + "]"

				elif len(selector) == 4:

					command += selector[:-1] + tmp1 + "]"

				else:

					command += selector + "[" + tmp1 + "]"

		elif command.startswith("function"):


			#Rename function paths
			tmp = re.findall(r'^function ([A-Za-z0-9_\-]+):([A-Za-z0-9_\-/]+)', command)
			if tmp:
				command = re.sub(r'^function ([A-Za-z0-9_\-]+):([A-Za-z0-9_\-/]+)', r'function {}:{}/{}'.format(datapack, tmp[0][0].lower(), tmp[0][1].lower()), command)


		
		#These do

		#Rename structure paths
		tmp = re.findall(r'structure_block(.+)name:(?:")?([A-Za-z0-9_\-/]+)(?:")?', command)
		if tmp:
			command = re.sub(r'structure_block(.+)name:(?:")?([A-Za-z0-9_\-/]+)(?:")?', r'structure_block\1name:"{}:{}"'.format(datapack, tmp[0][1]), command)

		#Rename loot table paths
		tmp = re.findall(r'LootTable:"minecraft:([A-Za-z0-9_\-/]+)"', command)
		if tmp:
			command = re.sub(r'LootTable:"minecraft:([A-Za-z0-9_\-/]+)"', r'LootTable:"minecraft:{}"'.format(tmp[0][0].lower()), command)
		else:
			tmp = re.findall(r'LootTable:"([A-Za-z0-9_\-]+):([A-Za-z0-9_\-/]+)"', command)
			if tmp:
				command = re.sub(r'LootTable:"([A-Za-z0-9_\-]+):([A-Za-z0-9_\-/]+)"', r'LootTable:"{}:{}/{}"'.format(datapack, tmp[0][0].lower(), tmp[0][1].lower()), command)



	except Exception as inst:
		print("[Error] Unknown error in {}".format(filename))
		print(inst)

		return gets


	return command

def convert(command):
	global executelist
	global tp_new_pos
	global precommand

	precommand = ""

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
				executelist[i] = re.sub(r'^detect ([~\-0-9\.]+ [~\-0-9\.]+ [~\-0-9\.]+) (?:minecraft\:)?([A-Za-z_]+) ([\S]+)', r'if block \1 pl@ceh0ld3r', executelist[i])
				if tmp:
					executelist[i] = re.sub(r'pl@ceh0ld3r', change_block(tmp[0][1], tmp[0][2], ""), executelist[i])

		executelist = [i for i in executelist if i != ""]

		if tp_self == True and re.findall(r'^tp @s', executelist[-1]):
			tp_new_pos = True

		executelist[-1] = convert_command(executelist[-1])

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
		tmp = re.findall(r'@([a-z])\[([A-Za-z0-9=\.,_\-\!\{\}]*)\]', command)
		command = re.sub(r'@([a-z])\[([A-Za-z0-9=\.,_\-\!\{\}]*)\]', r'@\1[pl@ceh0ld3r]', command)
		for match in tmp:
			selector = match[1].split(",")

			#Int coordinates to floats if needed
			for i in range(len(selector)):
				arg = selector[i].split("=")
				if arg[0] in ["x","z"]:
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
					if match[0] != "r":
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

	return precommand + command+"\n"



datapack = input("Datapack namespace [a-z0-9_-]: ").rstrip()

while not re.findall(r'^[a-z0-9_\-]+$', datapack):
	datapack = input("Datapack namespace [a-z0-9_-]: ")

tp_new_pos = False
while True:
	filename = "console"
	print(convert(input("> ").rstrip()), end="")
