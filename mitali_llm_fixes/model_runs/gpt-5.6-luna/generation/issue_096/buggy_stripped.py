
import os

home = os.path.expanduser("~")
settings_path = os.path.join(home, ".qiskit", "settings.conf")

with open(settings_path, "r") as f:
    contents = f.read()

print(contents)
