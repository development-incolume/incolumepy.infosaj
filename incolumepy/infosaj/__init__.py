"""
Principal Module.

Update metadata from version by semver
"""
from pathlib import Path

import toml

configfile = Path(__file__).parents[2].joinpath("pyproject.toml")
versionfile = Path(__file__).parent.joinpath("version.txt")
versionfile.write_text(
    f"{toml.load(configfile)['tool']['poetry']['version']}\n"
)
__version__ = versionfile.read_text().strip()
