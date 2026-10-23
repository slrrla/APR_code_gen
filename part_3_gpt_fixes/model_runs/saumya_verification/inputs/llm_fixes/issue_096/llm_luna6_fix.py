import os

home = os.path.expanduser("~")
settings_path = os.path.join(home, ".qiskit", "settings.conf")

# FIX: the configuration directory and file may not exist -> create them before reading, because opening a missing path in read mode fails
os.makedirs(os.path.dirname(settings_path), exist_ok=True)
open(settings_path, "a").close()

with open(settings_path, "r") as f:
    contents = f.read()

print(contents)
