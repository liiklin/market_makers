   
#!/usr/bin/python
import argparse
import hashlib
import time
import datetime
import calendar
from sqlalchemy import create_engine, exc
from sqlalchemy import Column, Date, ForeignKey, Integer, Numeric, PrimaryKeyConstraint, String, Table, UniqueConstraint, Boolean, DateTime, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy_utils import database_exists


Base = declarative_base()

class DimDateTime(Base):
    """
    Date spans
    """
    def __init__(self, timestamp=None, year=None, month=None, day=1, hour=0, minute=0):
        if timestamp:
            dt = datetime.datetime.fromtimestamp(timestamp)
            self.year = dt.year
            self.month = dt.month
            self.day = dt.day
            self.hour = dt.hour
            self.minute = dt.minute
            self.timestamp = timestamp
                
        elif year and month:
            self.year = year
            self.month = month
            self.day = day
            self.hour = hour
            self.minute = minute
            #self.qtr = (month % 3 + 3) * 3
            exact_dt = datetime.date(self.year, self.month, self.day, \
                hour=self.hour, minute=self.minute)
            self.date = exact_dt
            #self.weekday = weekday
            #self.week_number = week_number
            self.timestamp = time.mktime(exact_dt.timetuple())
        else:
            return None
        self.hash_value = hash("{0}-{1}-{2}-{3}-{4}".format(self.year, self.month, \
                self.day, self.hour, self.minute))

    __tablename__ = "dim_date"
    __table_args__ = (UniqueConstraint("year", "month", "day", "hour", \
        "minute", name='uc_dim_date_ymdhm_constraint'),\
        UniqueConstraint("hash_value",name="uc_dim_date_hash_value_constraint"))
    def __str__(self):
        return self.date.strftime("%Y-%m-%d")
    timestamp = Column(Integer, nullable=False, index=True, primary_key=True)
    hash_value = Column(String(20), nullable=False, index=True)
    year = Column(Integer, nullable=False, index=True)
    month = Column(Integer, nullable=False, index=True)
    day = Column(Integer, nullable=False, index=True)
    hour = Column(Integer, nullable=False, index=True)
    minute = Column(Integer, nullable=False, index=True)
    

class CurrencyPair(Base):
    def __init__(self, name, baseCurrency, quoteCurrency, quantityIncrement=0, \
        tickSize=0.1, takeLiquidityRate=0.0, provideLiquidityRate=0.0, \
        feeCurrency="USD", exchange="None"):
        self.baseCurrency = baseCurrency
        self.quoteCurrency   = quoteCurrency
        self.quantityIncrement = quantityIncrement
        self.tickSize = tickSize
        self.takeLiquidityRate = takeLiquidityRate
        self.provideLiquidityRate = provideLiquidityRate
        self.feeCurrency  = feeCurrency
        self.name = name
        self.exchange = exchange
    __tablename__ = "dim_currency_pair"
    __table_args__ = (UniqueConstraint("name", "baseCurrency", "quoteCurrency", name="uc_dim_currency_pair_nbq_constraint"),)
    def __str__(self):
        return "%s_%s_%s" % (self.name, self.baseCurrency, self.quoteCurrency)
    def as_dict(self):
        return self.__dict__
    name = Column(String(20), nullable=False, index=True, primary_key=True)
    baseCurrency = Column(String(20), nullable=False, index=True, primary_key=False)
    quoteCurrency = Column(String(20), nullable=False, index=True, primary_key=False)
    quantityIncrement = Column(Numeric(), nullable=True)
    tickSize = Column(Numeric(), nullable=True)
    takeLiquidityRate = Column(Numeric(), nullable=True)
    provideLiquidityRate = Column(Numeric(), nullable=True)
    feeCurrency = Column(String(20), nullable=True)
    exchange = Column(String(20), nullable=False, index=True, primary_key=False)

class Symbol(Base):
    """
    Basic symbol definition.
    """
    def __init__(self, name, exchangeName, crypto=True):
        self.name = name
        self.isCrypto = crypto
        self.exchangeName = exchangeName
    __tablename__ = "dim_symbol"
    __table_args__ = (UniqueConstraint("name", name="uc_dim_symbol_key"),)
    def __str__(self):
        return "%s" % (self.name)
    name = Column(String(20), nullable=False, index=True, primary_key=True)
    exchangeName = Column(String(20), nullable=False, index=True)
    isCrypto = Column(Boolean())

class Exchange(Base):
    """
    A coin Exchange
    """
    def __init__(self, name, public_url_base, currency_pair_lookup):
        self.name = name
        self.public_url_base = public_url_base
        self.currency_pair_lookup = currency_pair_lookup
    __tablename__ = "dim_exchange"
    __table_args__ = (UniqueConstraint("name", name="uc_dim_exchange_key"),)

    def __str__(self):
        return "%s %s" % (self.name, self.public_url_base)
    name = Column(String(20), nullable=False, index=True, primary_key=True)
    public_url_base = Column(String(150), nullable=True)
    currency_pair_lookup = Column(String(150), nullable=True)

class Trade(Base):
    __tablename__ = "fact_trade"
    #__table_args__ = (UniqueConstraint("name", name="uc_dim_exchange_key"),)
    exchange = Column(String(20), nullable=False, index=True, primary_key=True)
    currency_pair = Column(String(20), nullable=False, index=True, primary_key=True)
    date_time = Column(Date(), primary_key=True)
    price = Column(Numeric)
    quantity = Column(Numeric)
    side = Column(String(20), index=True)
    date_time_hash = Column(String(20))
    def __init__(self, exchange, currency_pair, date_time, price, quantity, side, date_time_hash):
        self.exchange = exchange
        self.currency_pair = currency_pair
        self.date_time = date_time
        self.price = price
        self.quantity = quantity
        self.side = side
        self.date_time_hash = date_time_hash
    def as_dict(self):
        return self.__dict__
class Price(Base):
    __tablename__ = "fact_price"
    exchange = Column(String(20), nullable=False, index=True, primary_key=True)
    currency_pair = Column(String(20), nullable=False, index=True, primary_key=True)
    timestamp = Column(Integer, nullable=False, index=True, primary_key=True)
    datetime_hash = (Column(String(20)))
    open = Column(Float)
    close = Column(Float)
    low = Column(Float)
    high = Column(Float)
    average = Column(Float)
    vol = Column(Float)
    vol_zero = Column(Numeric)
    std_price = Column(Float)
    def __init__(self, exchange, currency_pair, timestamp, \
        open=0, close=0, low=0, high=0, average=0, vol=0, std_price=0):
        self.exchange = exchange
        self.currency_pair = currency_pair
        self.open = open
        self.close = close
        self.low = low
        self.high = high
        self.average = average
        self.vol = vol
        self.vol_zero = 1 if self.vol == 0 else 0
        self.std_price = std_price
        self.timestamp = timestamp
    def as_dict(self):
        return self.__dict__

def create_db(connection):
    STATEMENT = "create database IF NOT EXISTS market_data;"
    init_conn = connection.replace("/market_data", "")
    print "%s using connection %s" % (STATEMENT, connection)
    engine = create_engine(connection)
    c = engine.connect()
    c.execute(STATEMENT)
    c.close()
    #print STATEMENT  
    
def create_schema(connection):
    print "Creating schema ..."
    engine = create_engine(connection)
    Base.metadata.create_all(engine)

def drop_recreate_db(connection):
    create_db(connection)
    print "Dropping schema ..."
    engine = create_engine(connection)
    Base.metadata.drop_all(engine)
    print "Recreate schema ..."
    Base.metadata.create_all(engine)

