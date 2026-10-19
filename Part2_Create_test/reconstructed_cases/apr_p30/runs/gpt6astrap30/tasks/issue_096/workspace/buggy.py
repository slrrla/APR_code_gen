# Read the optional Qiskit configuration, creating it if needed.

import os

home = os.path.expanduser("~")
settings_path = os.path.join(home, ".qiskit", "settings.conf")

# Qiskit does not create this optional configuration file automatically.
os.makedirs(os.path.dirname(settings_path), exist_ok=True)
if not os.path.exists(settings_path):
    with open(settings_path, "w") as f:
        f.write("[default]\n")

with open(settings_path, "r") as f:
    contents = f.read()

print(contents)
