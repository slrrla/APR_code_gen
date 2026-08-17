# To find where a pip-installed package lives, use `pip show <package>`
# instead of guessing from the imported module's __file__ attribute.
# This can be run as a shell command, or invoked from Python via subprocess.

import subprocess

result = subprocess.run(
    ["pip", "show", "qiskit-textbook"],
    capture_output=True,
    text=True
)

print(result.stdout)

# Example output:
# Name: qiskit-textbook
# Version: 0.1.0
# Summary: A collection of widgets, tools and games for using along
#   the Qiskit Textbook. See the textbook and a list of contributors at qiskit.org/textbook
# Home-page: UNKNOWN
# Author: Qiskit Team
# Author-email: hello@qiskit.org
# License: UNKNOWN
# Location: /usr/local/anaconda3/lib/python3.7/site-packages
# Requires: ipython, matplotlib, numpy, qiskit, ipywidgets
# Required-by:
