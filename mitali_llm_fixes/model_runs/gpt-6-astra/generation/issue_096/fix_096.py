import os

home = os.path.expanduser("~")
settings_path = os.path.join(home, ".qiskit", "settings.conf")

# FIX: The configuration directory may not exist -> create it if missing, because opening a file cannot create its parent directory.
os.makedirs(os.path.dirname(settings_path), exist_ok=True)
# FIX: Reading a missing file fails -> open in a+ mode and rewind, because this creates the file if needed and reads existing contents without truncating them.
with open(settings_path, "a+") as f:
    f.seek(0)
    contents = f.read()

print(contents)
