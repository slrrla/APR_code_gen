# The import statement itself does not change: the ImportError
# ("dlopen: cannot load any more object with static TLS") is caused by
# an OS-level limitation -- glibc on Ubuntu 14.04 has a small static TLS
# slot limit that is exhausted when scikit-learn (pulled in by
# qiskit.aqua) loads its compiled extensions.
#
# The fix is not a code change: upgrading the OS (e.g. Ubuntu 14.04 ->
# 16.04 or newer, which ships a newer glibc with a higher/absent static
# TLS slot limit) resolves the failure. The Python import remains the
# same.
from qiskit.aqua.operators import PrimitiveOp
