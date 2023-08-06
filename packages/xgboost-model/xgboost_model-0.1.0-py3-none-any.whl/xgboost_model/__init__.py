from xgboost_model.config import config

VERSION_PATH = config.PACKAGE_ROOT / 'VERSION'

print("here")
print(VERSION_PATH)

with open(VERSION_PATH, 'r') as version_file:
    __version__ = version_file.read().strip()
