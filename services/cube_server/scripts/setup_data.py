from mpipe import OrderedWorker, Stage, Pipeline
import sys
import os
import json
import requests
import time
import math
from datetime import timedelta 
from datetime import datetime
from sqlalchemy_utils import database_exists, create_database, drop_database
from repo.model import create_db, create_schema
from providers.config_provider import ConfigProvider
from repo.exchange_repo import ExchangeRepository
from repo.symbol_repo import SymbolRepository
from repo.currency_pair_repo import CurrencyPairRepository
from repo.date_repo import DateRepo
from repo.price_repo import PriceRepo
from providers.logging_base import LoggingBase
from repo.model import Symbol, CurrencyPair, Price

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
def load_file(path):
    if os.path.exists(path):
        #print "Loading %s" % (path)
        with open(path, 'r') as fp:
            values = fp.readlines()
            return values
    else:
        print "%s file not found" % (path)
    return None
def is_valid_data_dict(data, required_fields):
        if not data or not isinstance(data, dict):
            repo.logger.warn("Called with invalid data, must be a dict and have the keys %s", required_keys)
            return False
        missing = [x for x in required_fields if x not in data.keys()]
        if missing:
            repo = CurrencyPairRepository(config_provider=get_config_provider())
            repo.logger.warn("Called with invalid data, must be a dict and have the keys %s but %s is missing", required_keys, missing)
            return False
        return True



class SetupDatabase(OrderedWorker):
    """
    Configure and populate the database
    """
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
            self.putResult({"baseCurrency":x["baseCurrency"], \
                "id": x["id"], 
                "quoteCurrency":x["quoteCurrency"],
                "exchange": exchange_item[0]})

class SaveCurrencyPair(OrderedWorker):
    def doTask(self, data):
        """
        given data with the keys :
            id, baseCurrency, quoteCurrency, exchange
        add a new CurrencyPair to the database
        and return it as a dictrionary having the keys:
            baseCurrency, quoteCurrency, quantityIncrement, tickSize, takeLiquidityRate, 
            provideLiquidityRage, feeCurrency, name, exchange
        """
        repo = CurrencyPairRepository(config_provider=get_config_provider())
        required_keys = ["id", "baseCurrency", "quoteCurrency", "exchange"]
        if is_valid_data_dict(data, required_keys):
            id = data["id"]
            base_currency = data["baseCurrency"]
            quote_currency = data["quoteCurrency"]
            exchange = data["exchange"]
            cp_item = repo.add_get(CurrencyPair(name=id, baseCurrency=base_currency,\
                quoteCurrency=quote_currency, exchange=exchange))
            self.putResult(cp_item.as_dict())
            #repo.logger.info("Saved CurrencyPair %s", id)
        else:
            repo.logger.warn("failed to find one or more required keys: %s in %s", required_keys, data.keys())
            return None
            

class GetTradeRanges(OrderedWorker):
    def doTask(self, data):
        """
        creates a list of date/hour start/end values from the starttime to endtime
        for each of the currency_pairs in the download_list from app.config
        """
        dr_repo = DateRepo(config_provider=get_config_provider())
        start_date = None
        end_date = None
        if "start_date" in dr_repo.config_provider.data:
            start_date = datetime.strptime(dr_repo.config_provider.data["start_date"], \
            "%Y-%m-%dT%H:%M:%S")
        if "end_date" in dr_repo.config_provider.data:
            end_date = datetime.strptime(dr_repo.config_provider.data["end_date"], 
            "%Y-%m-%dT%H:%M:%S")
        if not start_date or not end_date:
            dr_repo.logger.warn("Invalid start or end_date, check config: %s %s", start_date, end_date)
        current_date = start_date
        #dr_repo.logger.info("config: %s", dr_repo.config_provider.data)
        if "download_list" in dr_repo.config_provider.data:
            pairs = load_file(dr_repo.config_provider.data["download_list"])
            if "name" in data and data["name"] in pairs:
                dr_repo.logger.info("Generating dates for %s from %s to %s", data["name"], start_date , end_date)
                while current_date < end_date:
                    data["start_date"] = current_date
                    data["end_date"] = current_date + timedelta(hours=1)
                    current_date = current_date + timedelta(hours=1)
                    dr_repo.logger.info("tradedate: %s", data)
                    self.putResult(data)
            else:
                dr_repo.logger.info("Skipping %s because it's not in the download list", data["name"])
        else:
            dr_repo.logger.info("No download list found.")
class GetRangeData(OrderedWorker):
    """
    Given a Pair name, exchange, start_date, end_data, exchange
    download the data and aggregate it into a price entry.
    Insert the price into the fact_price table.
    """
    def doTask(self, data):
        price_repo = PriceRepo(config_provider=get_config_provider())

        required_keys =  ["start_date", "end_date", "exchange", "name"]
        data["start_ts"] = time.mktime(data["start_date"].timetuple())
        data["end_ts"] = time.mktime(data["end_date"].timetuple())
        api_call = "https://api.hitbtc.com/api/2/public/trades/{name}?sort=DESC&by=timestamp&from={start_ts}&till={end_ts}&limit=10000".format(**data)
        r = requests.get(api_call)
        max_price = 0
        min_price = 9999999
        open_price = -1
        close_price = 0
        vol = 0
        avg_price = 0
        if r.status_code == 200:
            for trade in r.json():
                if "price" in trade:
                    if open_price = -1:
                        open_price = trade["price"]
                    min_price = math.min(min_price, trade["price"])
                    max_price = math.max(max_price, trade["price"])
                if "quantity" in trade:
                    vol += trade["quantity"]
            close_price = trade["price"]
            p = Price(exchange=data["exchange"], 
                currency_pair=data["name"], 
                timestamp=data["start_ts"],
                open = open_price,
                close = close_price, 
                low = min_price,
                high = max_price, 
                average = avg_price )
        else:
            price_repo.logger.info("Invalid status code %s for %s", r.status_code, api_call)



class SaveSymbol(OrderedWorker):
    def doTask(self, data):
        if len(data) >= 4:
            name1 = data[1]
            exchange_name = data[3]
            name = data[0]
            repo = SymbolRepository(config_provider=get_config_provider())
            repo.add_get(Symbol(name, exchange_name))
            repo.add_get(Symbol(name1, exchange_name))
            #repo.logger.info("Saved Symbol %s", data)
        
class CloseSymbolRepoSession(OrderedWorker):
    def doTask(self, data):
        if SymbolRepository.active_session:
            SymbolRepository.active_session.close_all()
            SymbolRepository.db_engine = None
            SymbolRepository.session = None
            lb = LoggingBase(config_provider=get_config_provider())
            lb.logger.info("Closed Symbol Repo Sessions")

class CloseCurrencyPairRepoSession(OrderedWorker):
    def doTask(self, data):
        if CurrencyPairRepository.active_session:
            CurrencyPairRepository.active_session.close_all()
            CurrencyPairRepository.db_engine = None
            CurrencyPairRepository.session = None
            lb = LoggingBase(config_provider=get_config_provider())
            lb.logger.info("Closed Currency Pair Sessions")

class CloseDateRepoSession(OrderedWorker):
    def doTask(self, data):
        if DateRepo.active_session:
            DateRepo.active_session.close_all()
            DateRepo.db_engine = None
            DateRepo.session = None
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
    trade_dates = Stage(GetTradeRanges)
    # link stages
    stage_setup.link(stage_load_ex)
    stage_load_ex.link(save_exchange)
    save_exchange.link(get_symbols)
    #get_symbols.link(save_symbols)
    get_symbols.link(save_curency_pair)
    save_curency_pair.link(trade_dates)
    # setup pipeline
    pipe = Pipeline(stage_setup)
    pipe.put(True)
    pipe.put(None)
    for result in pipe.results():
        print 'pipe result %s' % (result)
    close1 = CloseSymbolRepoSession()
    close1.doTask("")
    close2 = CloseCurrencyPairRepoSession()
    close2.doTask("")
    close3 = CloseDateRepoSession()
    close3.doTask("")

if __name__ == "__main__":
    main()

