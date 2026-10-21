import os

home = os.path.expanduser("~")
settings_path = os.path.join(home, ".qiskit", "settings.conf")

# FIX: opening a missing settings file in "r" mode raised FileNotFoundError -> create the parent directory and open in "a+" mode, because this creates the file if it is missing and still allows reading
os.makedirs(os.path.dirname(settings_path), exist_ok=True)
with open(settings_path, "a+") as f:
    # FIX: "a+" positions the cursor at the end of the file -> seek to the start before reading, because otherwise read() returns an empty string
    f.seek(0)
    contents = f.read()

print(contents)
