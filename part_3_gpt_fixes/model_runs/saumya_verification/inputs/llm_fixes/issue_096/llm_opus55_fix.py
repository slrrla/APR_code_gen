import os

home = os.path.expanduser("~")
settings_path = os.path.join(home, ".qiskit", "settings.conf")

# FIX: opening a non-existent ~/.qiskit/settings.conf in "r" mode crashed -> create the directory and open with "a+" then seek to start, because the config file is not created on install and must be made by the user
os.makedirs(os.path.dirname(settings_path), exist_ok=True)
with open(settings_path, "a+") as f:
    f.seek(0)
    contents = f.read()

print(contents)

