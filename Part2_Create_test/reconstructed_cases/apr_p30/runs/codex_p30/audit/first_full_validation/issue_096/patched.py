# Create missing user configuration files without replacing existing ones.

import os

home = os.path.expanduser("~")
settings_path = os.path.join(home, ".qiskit", "settings.conf")

ipython_dir = os.environ.get("IPYTHONDIR", os.path.join(home, ".ipython"))
ipython_config_path = os.path.join(
    ipython_dir, "profile_default", "ipython_kernel_config.py")
config_defaults = {
    settings_path: "[default]\ncircuit_drawer = mpl\n",
    ipython_config_path: "# IPython kernel configuration\nc = get_config()\n",
}
for config_path, default_contents in config_defaults.items():
    os.makedirs(os.path.dirname(config_path), exist_ok=True)
    if not os.path.exists(config_path):
        with open(config_path, "x", encoding="utf-8") as f:
            f.write(default_contents)

with open(settings_path, "r", encoding="utf-8") as f:
    contents = f.read()

print(contents)
