import logging
import sys

class LoggingBase(object):
    logger = None
    config_provider = None
    def flush(self):
        pass
    def __init__(self, config_provider=None):
        self.config_provider = config_provider
        if config_provider is not None:
            if "logger" in config_provider.data and config_provider.data["logger"]:
                self.logger = config_provider.data["logger"]
                #self.logger.debug("ConfigProvider is object %s in %s" % (isinstance(config_provider, object), __name__))
                #self.logger = config_provider.data["logger"]
                self.logger.debug("Using provided logger.")
                return
        self.logger = logging.getLogger()
        logging.basicConfig()
        if not self.config_provider is None and "log_level" in self.config_provider.data:
            self.logger.setLevel(self.config_provider.data["log_level"])
        else:
            self.logger.setLevel(logging.INFO)
        self.logger.debug("Logging base created for %s" % (self.__class__.__name__))