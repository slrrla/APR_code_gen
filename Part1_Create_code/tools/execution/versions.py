"""Canonical Qiskit version list and per-version interpreter/dependency policy.

Historical Qiskit packaging changed shape three times, and the environment
recipe has to follow it rather than assume one layout:

* **<= 0.43** ``qiskit`` is a *metapackage*. Installing it pulls qiskit-terra,
  qiskit-aer, qiskit-ignis, qiskit-aqua and qiskit-ibmq-provider together.
  Adding ``qiskit-aer`` explicitly fights the pin, so we never do.
* **0.44 - 0.46** ``qiskit`` becomes the former terra core on its own. Aer and
  the algorithms package are separate installs.
* **>= 1.0** core only, with a hard break in the 1.0 API surface.

Python support windows are taken from each release's own metadata rather than
guessed: the interpreter chosen per release is the newest one that release
actually supports, which keeps wheel availability good on Windows.
"""
from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class VersionSpec:
    qiskit: str
    python: str
    #: Extra pip requirements beyond ``qiskit==<version>``.
    extras: tuple[str, ...] = ()
    #: Packaging era, used by the classifier to read failures correctly.
    era: str = "core"
    note: str = ""

    @property
    def env_name(self) -> str:
        return "qiskit_" + self.qiskit.replace(".", "_")

    @property
    def requirements(self) -> list[str]:
        return [f"qiskit=={self.qiskit}", *self.extras]


#: Common scientific stack the reconstructed programs draw on. Deliberately
#: unpinned: pip resolves each against the Qiskit pin for that environment, so
#: an old release gets an old numpy rather than a 2.x that breaks it.
_BASE_EXTRAS = ("numpy", "scipy", "sympy", "matplotlib")

#: 0.44+ split Aer out of the metapackage. Left unpinned on purpose so the
#: resolver backtracks to an Aer that matches the Qiskit pin instead of
#: dragging in a build that demands a newer core.
_AER = ("qiskit-aer",)
_ALGOS = ("qiskit-algorithms",)

VERSIONS: tuple[VersionSpec, ...] = (
    # -- metapackage era -------------------------------------------------
    # qiskit 0.25.x == terra 0.17.x, April 2021. Metadata allows 3.6-3.9;
    # 3.9 is the newest supported and the only one with usable Windows wheels.
    VersionSpec("0.25.0", "3.9", _BASE_EXTRAS, "metapackage",
                "metapackage: bundles terra/aer/ignis/aqua/ibmq-provider"),
    VersionSpec("0.25.1", "3.9", _BASE_EXTRAS, "metapackage",
                "metapackage: bundles terra/aer/ignis/aqua/ibmq-provider"),
    VersionSpec("0.25.2", "3.9", _BASE_EXTRAS, "metapackage",
                "metapackage: bundles terra/aer/ignis/aqua/ibmq-provider"),
    VersionSpec("0.25.3", "3.9", _BASE_EXTRAS, "metapackage",
                "metapackage: bundles terra/aer/ignis/aqua/ibmq-provider"),

    # -- split era, pre-1.0 ----------------------------------------------
    # 0.45/0.46 support 3.8-3.12; 3.11 is the newest with complete wheels for
    # the matching Aer builds.
    VersionSpec("0.45.0", "3.11", _BASE_EXTRAS + _AER + _ALGOS, "split"),
    VersionSpec("0.45.1", "3.11", _BASE_EXTRAS + _AER + _ALGOS, "split"),
    VersionSpec("0.45.2", "3.11", _BASE_EXTRAS + _AER + _ALGOS, "split"),
    VersionSpec("0.45.3", "3.11", _BASE_EXTRAS + _AER + _ALGOS, "split"),
    VersionSpec("0.46.0", "3.11", _BASE_EXTRAS + _AER + _ALGOS, "split"),
    VersionSpec("0.46.1", "3.11", _BASE_EXTRAS + _AER + _ALGOS, "split"),
    VersionSpec("0.46.2", "3.11", _BASE_EXTRAS + _AER + _ALGOS, "split"),
    VersionSpec("0.46.3", "3.11", _BASE_EXTRAS + _AER + _ALGOS, "split"),

    # -- 1.x --------------------------------------------------------------
    VersionSpec("1.0.0", "3.11", _BASE_EXTRAS + _AER + _ALGOS, "v1"),
    VersionSpec("1.0.1", "3.11", _BASE_EXTRAS + _AER + _ALGOS, "v1"),
    VersionSpec("1.0.2", "3.11", _BASE_EXTRAS + _AER + _ALGOS, "v1"),
    VersionSpec("1.1.0", "3.11", _BASE_EXTRAS + _AER + _ALGOS, "v1"),
    VersionSpec("1.1.1", "3.11", _BASE_EXTRAS + _AER + _ALGOS, "v1"),
    VersionSpec("1.1.2", "3.11", _BASE_EXTRAS + _AER + _ALGOS, "v1"),
    VersionSpec("1.2.0", "3.11", _BASE_EXTRAS + _AER + _ALGOS, "v1"),
    VersionSpec("1.2.1", "3.11", _BASE_EXTRAS + _AER + _ALGOS, "v1"),
    VersionSpec("1.2.2", "3.11", _BASE_EXTRAS + _AER + _ALGOS, "v1"),
    VersionSpec("1.2.3", "3.11", _BASE_EXTRAS + _AER + _ALGOS, "v1"),
    VersionSpec("1.2.4", "3.11", _BASE_EXTRAS + _AER + _ALGOS, "v1"),

    # -- 2.x --------------------------------------------------------------
    VersionSpec("2.0.0", "3.12", _BASE_EXTRAS + _AER + _ALGOS, "v2"),
    VersionSpec("2.2.0", "3.12", _BASE_EXTRAS + _AER + _ALGOS, "v2"),
    VersionSpec("2.3.0", "3.12", _BASE_EXTRAS + _AER + _ALGOS, "v2"),
    VersionSpec("2.4.0", "3.12", _BASE_EXTRAS + _AER + _ALGOS, "v2"),
    VersionSpec("2.5.0", "3.12", _BASE_EXTRAS + _AER + _ALGOS, "v2"),
)

BY_VERSION = {v.qiskit: v for v in VERSIONS}

#: Representative subset for the pilot: one per packaging era plus the
#: boundaries where the API broke.
PILOT_VERSIONS = ("0.25.0", "0.46.3", "1.0.0", "1.2.4", "2.0.0", "2.5.0")


def get(version: str) -> VersionSpec:
    if version not in BY_VERSION:
        raise KeyError(f"unknown qiskit version {version!r}; "
                       f"known: {', '.join(BY_VERSION)}")
    return BY_VERSION[version]


def all_versions() -> list[str]:
    return [v.qiskit for v in VERSIONS]


def python_versions_needed() -> dict[str, list[str]]:
    out: dict[str, list[str]] = {}
    for v in VERSIONS:
        out.setdefault(v.python, []).append(v.qiskit)
    return out
