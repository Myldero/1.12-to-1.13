import os
import shutil
from . import commands

path = input("Path to world folder: ")
datapack = input("Datapack name (Alphanumeric): ")

while not datapack.isalnum():
    datapack = input("Datapack name (Alphanumeric): ")


print("Moving directories")

try:
    shutil.move(os.path.join(path, "data", "functions"), os.path.join(path, "data", datapack, "functions"))
except:
    pass

try:
    shutil.move(os.path.join(path, "data", "advancements"), os.path.join(path, "data", datapack, "advancements"))
except:
    pass

try:
    shutil.move(os.path.join(path, "data", "loot_tables"), os.path.join(path, "data", datapack, "loot_tables"))
except:
    pass

try:
    shutil.move(os.path.join(path, "structures"), os.path.join(path, "data", datapack, "structures"))
except:
    pass


#Convert functions
print("Converting functions")

for path, dirs, files in os.walk( os.path.join(path, "data", datapack, "functions") ):
    for file in files:
        if file.endswith(".mcfunction"):
            fullpath = os.path.join(path, file)

            memory = ""

            with open(fullpath, 'r') as f:
                for line in f:
                    memory += commands.convert(line)

            with open(fullpath, 'w') as f:
                f.write(memory)
