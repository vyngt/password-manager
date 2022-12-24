from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_DIR = BASE_DIR / "data"
DATA_LOCATION = DATA_DIR / "vault.vpm"

PROFILE = DATA_DIR / "profile.vpm"

STATIC_ROOT = BASE_DIR / "assets"
