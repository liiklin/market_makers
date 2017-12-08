from mpipe import OrderedWorker, Stage, Pipeline
import sys
import os
import json
import requests
from sqlalchemy_utils import database_exists, create_database, drop_database
from repo.model import create_db, create_schema
from providers.config_provider import ConfigProvider
from repo.exchange_repo import ExchangeRepository
from repo.symbol_repo import SymbolRepository
from repo.currency_pair_repo import CurrencyPairRepository
from providers.logging_base import LoggingBase
from repo.model import Symbol, CurrencyPair

def load_config():
    if os.path.exists("./app_config.json"):
        print "Loading app_config.json..."
        with open("./app_config.json", 'r') as fp:
            config = json.load(fp)
            return config
    else:
        print "./config.json not found"
    return None
def get_config_provider():
    cp = ConfigProvider()
    cp.load_config()
    return cp

class SetupDatabase(OrderedWorker):
    def doTask(self, force):
        if force:
            print "force db create..."
            config = load_config()
            
            print "drop database..."
            if database_exists(config["CONNECTION"]):
                drop_database(config["CONNECTION"])
            print "create db..."
            init_conn = config["CONNECTION"].replace("/market_data", "")
            create_db(init_conn)
            create_schema(config["CONNECTION"])
            return "db create done."
        else:
            print "create db if if not exists..."
            config = load_config()
            if not database_exists(config["CONNECTION"]):
                print "create db..."
                init_conn = config["CONNECTION"].replace("/market_data", "")
                create_db(init_conn)
                create_schema(config["CONNECTION"])
            return "setup done."

class LoadExchange(OrderedWorker):
    def doTask(self, load):
        if load:
            config = get_config_provider()
            repo = ExchangeRepository(config_provider=config)
            if os.path.exists(config.data["exchange_list"]):
                repo.logger.info("found exchange list on path %s", config.data["exchange_list"])
                with open(config.data["exchange_list"]) as fp:
                    for line in fp:
                        self.putResult(line.split(","))
            else:
                repo.logger.warn("Could not find file %s", config.data["exchange_list"])

class SaveGetExchange(OrderedWorker):
    def doTask(self, data):
        config = get_config_provider()
        repo = ExchangeRepository(config_provider=config)
        item = repo.add_get({"name":data[0], "public_url_base":data[1], "currency_pair_lookup":data[2]})
        repo.logger.info("Loaded exchange %s", data)
        return (item.name, item.public_url_base, item.currency_pair_lookup)

class GetSymbols(OrderedWorker):
    def doTask(self, exchange_item):
        config = get_config_provider()
        repo = ExchangeRepository(config_provider=config)
        repo.logger.info("Load symbols for exchange %s", exchange_item[0])
        r = requests.get("%s%s" % (exchange_item[1], exchange_item[2]))
        repo.logger.info("Got %s symbols" % (len(r.json())))
        for x in r.json():
            self.putResult(( x["baseCurrency"], \
                x["id"], x["quoteCurrency"], exchange_item[0]))

class SaveCurrencyPair(OrderedWorker):
    def doTask(selv, data):
        if len(data) >= 4:
            id = data[1]
            base_currency = data[0]
            quote_currency = data[2]
            exchange = data[3]
            repo = CurrencyPairRepository(config_provider=get_config_provider())
            repo.add_get(CurrencyPair(name=id, baseCurrency=base_currency,\
                quoteCurrency=quote_currency, exchange=exchange))
            repo.loggger.info("Saved CurrencyPair %s", id)

class SaveSymbol(OrderedWorker):
    def doTask(self, data):
        if len(data) >= 4:
            name1 = data[1]
            exchange_name = data[3]
            name = data[0]
            repo = SymbolRepository(config_provider=get_config_provider())
            repo.add_get(Symbol(name, exchange_name))
            repo.add_get(Symbol(name1, exchange_name))
            repo.logger.info("Saved Symbol %s", data)
        
class CloseSymbolReopSession(OrderedWorker):
    def doTask(self, data):
        if SymbolRepository.active_session:
            SymbolRepository.active_session.close_all()
            SymbolRepository.db_engine = None
            SymbolRepository.session = None
            lb = LoggingBase(config_provider=get_config_provider())
            lb.logger.info("Closed Symbol Repo Sessions")

class CloseSymbolReopSession(OrderedWorker):
    def doTask(self, data):
        if CurrencyPairRepository.active_session:
            CurrencyPairRepository.active_session.close_all()
            CurrencyPairRepository.db_engine = None
            CurrencyPairRepository.session = None
            lb = LoggingBase(config_provider=get_config_provider())
            lb.logger.info("Closed Currency Pair Sessions")
def main():
    # create stages
    stage_setup = Stage(SetupDatabase,1)
    stage_load_ex = Stage(LoadExchange,1)
    save_exchange = Stage(SaveGetExchange)
    get_symbols = Stage(GetSymbols)
    save_symbols = Stage(SaveSymbol, 1)
    save_curency_pair = Stage(SaveCurrencyPair)
    # link stages
    stage_setup.link(stage_load_ex)
    stage_load_ex.link(save_exchange)
    save_exchange.link(get_symbols)
    get_symbols.link(save_symbols)
    get_symbols.link(save_curency_pair)
    # setup pipeline
    pipe = Pipeline(stage_setup)
    pipe.put(True)
    pipe.put(None)
    for result in pipe.results():
        print 'pipe result %s' % (result)
    close1 = CloseSymbolRepoSession()
    close1.doTask("")
    close2 = CloseCurRepoSessionRepoSession()
    close2.doTask("")

if __name__ == "__main__":
    main()

