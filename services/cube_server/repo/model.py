   
#!/usr/bin/python
import argparse
import hashlib
import time
import datetime
import calendar
from sqlalchemy import create_engine, exc
from sqlalchemy import Column, Date, ForeignKey, Integer, Numeric, PrimaryKeyConstraint, String, Table, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship


Base = declarative_base()

class DimDateTime(Base):
    """
    Date spans
    """
    def __init__(self, year, month, day=1, hour=0, minute=0):
        self.year = year
        self.month = month
        self.day = day
        self.hour = hour
        self.minute = minute
        #self.qtr = (month % 3 + 3) * 3
        exact_dt = datetime.date(self.year, self.month, self.day, hour=self.hour, minute=self.minute)
        self.date = exact_dt
        #self.weekday = weekday
        #self.week_number = week_number
        self.timestamp = time.mktime(exact_dt.timetuple())
        self.hash_value = hash("{0}-{1}-{2}-{3}-{4}".format(self.year, self.month, self.day, self.hour, self.minute))

    __tablename__ = "dim_date"
    __table_args__ = (UniqueConstraint("year", "month", "day", name='uc_dim_date_ymd_constraint'),)
    def __str__(self):
        return self.date.strftime("%Y-%m-%d")
    hash_value = Column(String(20), nullable=False, index=True, primary_key=True)
    year = Column(Integer, nullable=False, index=True)
    month = Column(Integer, nullable=False, index=True)
    day = Column(Integer, nullable=False, index=True)
    hour = Column(Integer, nullable=False, index=True)
    minute = Column(Integer, nullable=False, index=True)
    timestamp = Column(Integer, nullable=False, indext=True)

class CurrencyPair(Base):
    def __init__(self, name, baseCurrency, quoteCurrency, quantityIncrement=0, tickSize=0.1, takeLiquidityRate=0.0, provideLiquidityRate=0.0, feeCurrency="USD"):
        self.baseCurrency = baseCurrency
        self.quoteCurrency   = quoteCurrency
        self.quantityIncrement = quantityIncrement
        self.tickSize = tickSize
        self.takeLiquidityRate = takeLiquidityRate
        self.provideLiquidityRate = provideLiquidityRate
        self.feeCurrency  = feeCurrency
        self.name = name
    __tablename__ = "dim_currency_pair"
    __table_args__ = (UniqueConstraint("name", "baseCurrency", "quoteCurrency", name="uc_dim_currency_pair_nbq_constraint"),)
    def __str__(self):
        return "%s_%s_%s" % (self.name, self.baseCurrency, self.quoteCurrency)
    name = Column(String(20), nullable=False, index=True, primary_key=True)
    baseCurrency = Column(String(20), nullable=False, index=True, primary_key=False)
    quoteCurrency = Column(String(20), nullable=False, index=True, primary_key=False)
    quantityIncrement = Column(Numeric(), nullable=True)
    tickSize = Column(Numeric(), nullable=True)
    takeLiquidityRate = Column(Numeric(), nullable=True)
    provideLiquidityRate = Column(Numeric(), nullable=True)
    feeCurrency = Column(String(20), nullable=True)

class Symbol(Base):
    """
    Basic symbol definition.
    """
    def __init__(self, name, fullName, crypto=True):
        self.name = name
        self.fullName = fullName
        self.isCrypto = crypto
    __tablename__ = "dim_symbol"
    __table_args__ = (UniqueConstraint("name", name="uc_dim_symbol_key"))
    def __str__(self):
        return "%s" % (self.name)
    name = Column(String(20), nullable=False, index=True, primary_key=True)
    fullName = Column(String(150), nullalbe=True)
    isCrypto = Column(Boolean())

