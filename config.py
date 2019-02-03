import json
from urllib import parse
import hashlib

_config = None


def readConfigFile(path=None):
    if not path:
        path = "config.json"
    with open(path, 'r') as f:
        _config = json.load(f)

    _config["username_urlencode"] =parse.quote(_config["username"])
    _config["password_md5"] = hashlib.md5(_config["password"].encode('utf-8')).hexdigest()

    print(_config)
    return _config


class Config:
    @staticmethod
    def getConfig():
        global _config
        if not _config:
            _config = readConfigFile()
        return _config


if __name__ == "__main__":
    print(Config.getConfig())