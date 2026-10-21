import os

home = os.path.expanduser("~")
settings_path = os.path.join(home, ".qiskit", "settings.conf")

# FIX: the settings file was opened for reading without checking it exists -> create the directory and an empty file if missing, because ~/.qiskit/settings.conf is not created by default and reading it raised FileNotFoundError
os.makedirs(os.path.dirname(settings_path), exist_ok=True)
if not os.path.exists(settings_path):
    open(settings_path, "a").close()

with open(settings_path, "r") as f:
    contents = f.read()

print(contents)
