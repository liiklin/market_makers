from mpipe import OrderedWorker, Stage, Pipeline
import sys
import os
import json
import requests
import time
import math
from datetime import timedelta 
from datetime import datetime
import numpy as np
from sqlalchemy_utils import database_exists, create_database, drop_database
from repo.model import create_db, create_schema
from providers.config_provider import ConfigProvider
from repo.exchange_repo import ExchangeRepository
from repo.symbol_repo import SymbolRepository
from repo.currency_pair_repo import CurrencyPairRepository
from repo.date_repo import DateRepo
from repo.price_repo import PriceRepository
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
        if not force:
            return "Skipping database creation."
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
        if not load:
            return None
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
        if not data:
            return None
        config = get_config_provider()
        repo = ExchangeRepository(config_provider=config)
        item = repo.add_get({"name":data[0], "public_url_base":data[1], "currency_pair_lookup":data[2]})
        repo.logger.info("Loaded exchange %s", data)
        return (item.name, item.public_url_base, item.currency_pair_lookup)

class GetSymbols(OrderedWorker):
    def doTask(self, exchange_item):
        if not exchange_item:
            return None
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
        if not data:
            return data
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
            repo.logger.debug("Passing CurrencyPair %s downstream", id)
        else:
            repo.logger.warn("failed to find one or more required keys: %s in %s", required_keys, data.keys())
            return None

class GetTradeRanges(OrderedWorker):
    def doTask(self, data):
        """
        creates a list of date/hour start/end values from the starttime to endtime
        for each of the currency_pairs in the download_list from app.config
        """
        if not data:
            return data
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
            pairs = [x.strip('\n').strip(" ") for x in  load_file(dr_repo.config_provider.data["download_list"])]
            if "name" in data and data["name"] in pairs:
                dr_repo.logger.info("Generating dates for %s from %s to %s", data["name"], start_date , end_date)
                while current_date < end_date:
                    data["start_date"] = current_date
                    data["end_date"] = current_date + timedelta(hours=1)
                    current_date = current_date + timedelta(hours=1)
                    #dr_repo.logger.info("tradedate: %s", data)
                    data["start_ts"] = time.mktime(data["start_date"].timetuple())
                    data["end_ts"] = time.mktime(data["end_date"].timetuple())
                    dr_repo.add_get(timestamp=data["start_ts"])
                    self.putResult(data)
                self.putResult(None)
            else:
                #dr_repo.logger.info("Skipping %s because it's not in %s", data["name"], pairs)
                pass
        else:
            dr_repo.logger.info("No download list found.")
class AddPriceData(OrderedWorker):
    """
    Given a Pair name, exchange, start_date, end_data, exchange
    download the data and aggregate it into a price entry.
    Insert the price into the fact_price table.
    """
    def doTask(self, data):
        if not data:
            return data
        price_repo = PriceRepository(config_provider=get_config_provider())
        required_keys =  ["start_date", "end_date", "exchange", "name"]
        if is_valid_data_dict(data, required_keys):
            
            existing = price_repo.exists(Price(exchange=data["exchange"], \
                currency_pair=data["name"], timestamp=data["start_ts"]))
            if not existing:
                api_call = "https://api.hitbtc.com/api/2/public/trades/{name}?sort=DESC&by=timestamp&from={start_ts}&till={end_ts}".format(**data)
                #time.sleep(1)
                r = requests.get(api_call)
                open_price = -1
                close_price = 0
                vol = 0
                avg_price = 0
                plist = []
                vlist = []
                current_price = 0
                max_price = 0
                min_price = 9999999
                price_repo.logger.info("Called %s status %s", api_call, r.status_code)
                if r.status_code == 200:
                    for trade in r.json():
                        if "quantity" in trade and trade["quantity"] > 0:
                            if "price" in trade:
                                current_price = float(trade["price"])
                                if open_price == -1:
                                    open_price = float(trade["price"])
                                min_price = float(min(min_price, float(trade["price"])))
                                max_price = float(max(max_price, float(trade["price"])))
                                plist.append(float(trade["price"]))
                            if "quantity" in trade:
                                vol += float(trade["quantity"])
                                vlist.append(float(trade["quantity"]))
                            avg_price = float(np.average(plist, weights=vlist) if not sum(vlist) == 0 else 0)
                            close_price = current_price
                        else:
                            current_price = -1
                            open_price = -1
                            min_price = -1
                            max_price = -1
                            vol = -1
                            avg_price = -1
                            close_price = -1

                    p = Price(exchange=data["exchange"], 
                        currency_pair=data["name"], 
                        timestamp=int(data["start_ts"]),
                        open = open_price,
                        close = close_price, 
                        low = min_price,
                        high = max_price, 
                        average = avg_price, 
                        vol= float(sum(vlist)), 
                        std_price=float(np.std(plist) if plist and \
                            not math.isnan(np.std(plist)) else 0))
                    price_repo.add_get(p)
                    return 1
                else:
                    price_repo.logger.info("Invalid status code %s for %s", r.status_code, api_call)
                return None
            else:
                price_repo.logger.info("Price exists, not inserting %s", data)
                return None
        else:
            price_repo.logger.info("No valid insert data %s", data)
            return None

class SaveSymbol(OrderedWorker):
    def doTask(self, data):
        if not data:
            return data
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
class ClosePriceRepoSession(OrderedWorker):
    def doTask(self, data):
        if PriceRepository.active_session:
            PriceRepository.active_session.close_all()
            PriceRepository.db_engine = None
            PriceRepository.session = None
            lb = LoggingBase(config_provider=get_config_provider())
            lb.logger.info("Closed PriceRepository Sessions")

def main():
    config = load_config()
    clean_data = True if "True" in config["CLEAN_DATA"] else False

    # create stages
    stage_setup = Stage(SetupDatabase,1)
    stage_load_ex = Stage(LoadExchange,1)
    save_exchange = Stage(SaveGetExchange)
    get_symbols = Stage(GetSymbols)
    save_symbols = Stage(SaveSymbol, 1)
    save_curency_pair = Stage(SaveCurrencyPair)
    trade_dates = Stage(GetTradeRanges,1)
    add_price = Stage(AddPriceData, 1)
    # link stages
    stage_setup.link(stage_load_ex)
    stage_load_ex.link(save_exchange)
    save_exchange.link(get_symbols)
    #get_symbols.link(save_symbols)
    get_symbols.link(save_curency_pair)
    save_curency_pair.link(trade_dates)
    trade_dates.link(add_price)
    # setup pipeline
    pipe = Pipeline(stage_setup)
    pipe.put(clean_data)
    pipe.put(None)
    insert_count = []
    for result in pipe.results():
        print 'pipe result %s' % (result)
        insert_count.append(result)
    print "inserted %s records" % (sum(insert_count))
    close1 = CloseSymbolRepoSession()
    close1.doTask("")
    close2 = CloseCurrencyPairRepoSession()
    close2.doTask("")
    close3 = CloseDateRepoSession()
    close3.doTask("")
    close4 = ClosePriceRepoSession()
    close4.doTask("")

if __name__ == "__main__":
    main()

