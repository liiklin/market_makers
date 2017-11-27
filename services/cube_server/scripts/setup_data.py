from mpipe import OrderedWorker, Stage, Pipeline
import sys
import os
import json
from repo.model import create_db, create_schema
from providers.config_provider import ConfigProvider

def load_config():
    if os.path.exists("./app_config.json"):
        print "Loading app_config.json..."
        with open("./app_config.json", 'r') as fp:
            config = json.load(fp)
            return config
    else:
        print "./config.json not found"
    return None
class SetupDatabase(OrderedWorker):
    def doTask(self, is_go):
        if is_go:
            print "go time, load config..."
            config = load_config()
            print "create db..."
            init_conn = config["CONNECTION"].replace("/market_maker", "")
            create_db(init_conn)
            create_schema(config["CONNECTION"])
            return "setup done."
            


def main():
     stage_setup = Stage(SetupDatabase,1)
     pipe = Pipeline(stage_setup)
     pipe.put(True)
     pipe.put(None)
     for result in pipe.results():
         print 'pipe result %s' % (result)




if __name__ == "__main__":
    main()

