import os

home = os.path.expanduser("~")
settings_path = os.path.join(home, ".qiskit", "settings.conf")

# The file is optional and not created by Qiskit; create it if missing.
if not os.path.exists(settings_path):
    os.makedirs(os.path.dirname(settings_path), exist_ok=True)
    with open(settings_path, "w") as f:
        f.write("[default]\ncircuit_drawer = mpl\n")

with open(settings_path, "r") as f:
    contents = f.read()

print(contents)
