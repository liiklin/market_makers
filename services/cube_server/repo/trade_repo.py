from model import Trade
from sqlalchemy import asc, create_engine, desc
from sqlalchemy.orm import sessionmaker
from providers.logging_base import LoggingBase

class TradeRepository(LoggingBase):
    active_session = None
    db_engine = None
    session = None
    def __init__(self, config_provider=None):
        super(TradeRepository, self).__init__(config_provider=config_provider)
        if not TradeRepository.db_engine:
            self.connection = config_provider.data["connection"]
            TradeRepository.db_engine = create_engine(self.connection)
            TradeRepository.session = sessionmaker(bind=self.db_engine)
            TradeRepository.active_session = TradeRepository.session()

    def get_count(self):
        return self.active_session.query(Trade).count()

    def add_get(self, trade, error_if_exists=False):
        """
        Add the provided Trade info to the database if it DNE
        expects dict of Trade values {"name":"", ...}
        """
        value_or_empty = lambda e, f: e[f] if f in e else ""
        query = TradeRepository.active_session.query(Trade).filter_by(\
            exchange=trade.exchange, 
            currency_pair=trade.currency_pair, 
            date_time=trade.date_time )
        if query.count() > 0:
            if error_if_exists:
                raise Exception("Item with %s %s %s already exists" % (trade.currency, trade.currency_pair, trade.date_time ))
            return query.first()
        
        else:
            insert_Trade = trade
            TradeRepository.active_session.add(insert_Trade)
            TradeRepository.active_session.commit()
            self.logger.info("Inserted new Trade %s %s %s", trade.exchange, trade.currency_pair, trade.date_time)
            return insert_Trade
        return None

    def truncate(self):
        self.db_engine.execute("DELETE FROM dim_Trade")

    