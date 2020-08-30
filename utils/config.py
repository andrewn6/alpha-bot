from ast import literal_eval
import json
from os import path

class Config():


    def __init__(self):
        self.conf_file = 'config.json'
        if not path.isfile(self.conf_file):
            raise FileNotFoundError


    def load(self):
        with open(self.conf_file) as conf:
            return json.load(conf)


    def save(self, config):
        with open(self.conf_file, 'w') as conf:
            json.dump(conf, config)


    def set(self, key: str, val):
        """
        Updates a single entry in the config file
        """
        # read config from disk
        config = self.load()
        # check item exists
        if config.get(key):
            # if true, log previous value
            print(f"Config value for '{key}' changed "\
                "from '{config.get(key)}' to '{val}'")
        else:
            # if false, log a new key val pair
            print(f"Config value for '{key}' set to '{val}'")
        config[key] = literal_eval(val)
        # write config back to disk
        self.save(config)
