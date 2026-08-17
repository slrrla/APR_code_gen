# Fix: create the missing configuration directory/file(s) ourselves
# instead of assuming they already exist.

import os

home = os.path.expanduser("~")
qiskit_dir = os.path.join(home, ".qiskit")
settings_path = os.path.join(qiskit_dir, "settings.conf")

# Ensure the directory exists
os.makedirs(qiskit_dir, exist_ok=True)

# Create the settings file if it doesn't exist yet
if not os.path.exists(settings_path):
    with open(settings_path, "w") as f:
        f.write("[default]\n")

with open(settings_path, "r") as f:
    contents = f.read()

print(contents)

# Also ensure the IPython kernel config exists by generating a profile
# (equivalent to running `ipython profile create` from the shell)
ipython_dir = os.path.join(home, ".ipython", "profile_default")
if not os.path.isdir(ipython_dir):
    os.system("ipython profile create")
