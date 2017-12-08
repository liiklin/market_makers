import os
import json
class ConfigProvider(object):
    """
    Load and validate configuration data
    """
    config_path = "./app_config.json"
    required_settings = []
    data = {}
    nodes = []
    def __init__(self, required_settings=None, nodes=None, config_path=None):
        if nodes:
            self.nodes = nodes
        if required_settings:
            self.required_settings = required_settings
        if config_path and os.path.exists(config_path) and os.path.isfile(config_path):
            self.config_path = config_path
        self.load_config()
    def lower_keys(self, x):
        """
        Convert all dictionary keys to lower for consistentcy
        """
        if isinstance(x, list):
            return [self.lower_keys(v) for v in x]
        elif isinstance(x, dict):
            return dict((k.lower(), self.lower_keys(v)) for k, v in x.iteritems())
        else:
            return x
    def load_config(self):
        """
        Load the connection configuration data.
        """
        if os.path.exists(self.config_path):
            if os.path.isfile(self.config_path):
                with open(self.config_path, 'r') as file_object:
                    self.data = self.lower_keys(json.load(file_object))
                    self.validate_config()
                    # extend nodes list with the configuration data
                    if "nodes" in self.data.keys() and len(self.data["nodes"]) > 0:
                        self.nodes[:] = []
                        self.nodes.extend(self.data["nodes"])
                    if "version" in self.data.keys():
                        #print "app_version : %s" % (self.data["version"])
                        pass
                    #print "Config file %s loaded %s." % (self.config_path, self.data)
                    return
        else:
            print "Config file %s not found." % (self.config_path)
        if self.nodes is None:
            raise IOError("Missing or invalid config_path (%s) on ConnectionProvider" % \
                (self.config_path))
        else:
            print "No config file found will use provided nodes instead %s" % (",".join(self.nodes))

    def validate_config(self):
        """
        Verify the fields required exist in the config file.
        """
        fx_inconfig = lambda x: x in self.data.keys()
        missing_settings = [x for x in self.required_settings if not fx_inconfig(x)]
        if len(missing_settings) > 0:
            raise KeyError("Missing required settings %s" % (",".join(missing_settings)))
