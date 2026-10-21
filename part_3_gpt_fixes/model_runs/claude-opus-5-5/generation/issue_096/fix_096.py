import os

home = os.path.expanduser("~")
settings_path = os.path.join(home, ".qiskit", "settings.conf")

# FIX: file/folder may not exist (Qiskit doesn't create them) -> create ~/.qiskit and a default settings.conf if missing, because opening a nonexistent file for reading raises FileNotFoundError
os.makedirs(os.path.dirname(settings_path), exist_ok=True)
if not os.path.exists(settings_path):
    with open(settings_path, "w") as f:
        f.write("[default]\ncircuit_drawer = mpl\n")

with open(settings_path, "r") as f:
    contents = f.read()

print(contents)
