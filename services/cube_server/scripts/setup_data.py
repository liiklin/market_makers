from mpipe import OrderedWorker, Stage, Pipeline
import sys
import os
import json
from repo.model import create_db
from providers.config_provider import ConfigProvider

def load_config():
    if os.path.exists("./config.json"):
        print "Loading config.json..."
        with open("./config.json", 'r') as fp:
            config = json.load(fp)
            return config
    else:
        print "./config.json not found"
    return None
class SetupDatabase(OrderedWorker):
    def doTask():
        config = load_config()
        create_db(config["CONNECTION"])

def main():
     stage_lookup = Stage(SetupDatabase,1)

if __name__ == "__main__":
    main()

