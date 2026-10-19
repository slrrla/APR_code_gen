import os

home = os.path.expanduser("~")
settings_path = os.path.join(home, ".qiskit", "settings.conf")

# FIX: the .qiskit directory may not exist -> create it, because the file cannot be created without its parent directory
os.makedirs(os.path.dirname(settings_path), exist_ok=True)

# FIX: opening in read mode fails when the settings file is absent -> create it if needed and rewind, because the contents can then be read
with open(settings_path, "a+") as f:
    f.seek(0)
    contents = f.read()

print(contents)
