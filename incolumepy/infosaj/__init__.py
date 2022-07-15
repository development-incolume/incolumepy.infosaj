"""
Principal Module.

Update metadata from version by semver
"""
from pathlib import Path
try:
    import tomllib
except ModuleNotFoundError:
    import tomli as tomllib

configfile = Path(__file__).parents[2].joinpath("pyproject.toml")
versionfile = Path(__file__).parent.joinpath("version.txt")
versionfile.write_text(
    f"{tomllib.loads(configfile.read_text())['tool']['poetry']['version']}\n"
)
__version__ = versionfile.read_text().strip()
