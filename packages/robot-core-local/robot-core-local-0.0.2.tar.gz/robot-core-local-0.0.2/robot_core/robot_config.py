import json

import pip
from pymongo import MongoClient


def start_config(code):
    """
    Load a configuration of robot and install dependencies
    """
    print ("Robot Config")

    with open("robot-config.json") as json_file:
        config = json.load(json_file)
        name = config["name"]
        name = name.lower().replace(" ", "_")

        client = MongoClient("mongodb://localhost:27017")
        db = client[name]

        config_db = db.confg.find_one({"code": name})
        if not config_db:
            db.config.insert(config)

            for pack in config['packages']:
                pip.main(['install', pack["pip"]])





