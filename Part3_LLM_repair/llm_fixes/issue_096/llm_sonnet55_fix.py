import os

home = os.path.expanduser("~")
settings_path = os.path.join(home, ".qiskit", "settings.conf")

# FIX: the config directory and file were assumed to exist -> create the directory and an empty file if missing, because Qiskit does not create ~/.qiskit/settings.conf by default and opening it for reading raised FileNotFoundError
os.makedirs(os.path.dirname(settings_path), exist_ok=True)
if not os.path.exists(settings_path):
    open(settings_path, "a").close()

with open(settings_path, "r") as f:
    contents = f.read()

print(contents)
