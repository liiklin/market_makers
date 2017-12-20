from model import Price
from sqlalchemy import asc, create_engine, desc
from sqlalchemy.orm import sessionmaker
from providers.logging_base import LoggingBase

class PriceRepository(LoggingBase):
    active_session = None
    db_engine = None
    session = None
    def __init__(self, config_provider=None):
        super(PriceRepository, self).__init__(config_provider=config_provider)
        if not PriceRepository.db_engine:
            self.connection = config_provider.data["connection"]
            PriceRepository.db_engine = create_engine(self.connection)
            PriceRepository.session = sessionmaker(bind=self.db_engine)
            PriceRepository.active_session = PriceRepository.session()

    def get_count(self):
        return self.active_session.query(Price).count()

    def add_get(self, price, error_if_exists=False):
        """
        Add the provided Price info to the database if it DNE
        expects dict of Price values {"name":"", ...}
        """
        value_or_empty = lambda e, f: e[f] if f in e else ""
        query = PriceRepository.active_session.query(price).filter_by(\
            exchange=price.exchange, 
            currency_pair=price.currency_pair,
            timestamp=price.timestamp)
        if query.count() > 0:
            if error_if_exists:
                raise Exception("Item with %s %s %s already exists" % (price.currency, price.currency_pair, price.timestamp ))
            return query.first()
        else:
            PriceRepository.active_session.add(price)
            PriceRepository.active_session.commit()
            self.logger.info("Inserted new Price %s %s %s", price.exchange, price.currency_pair, price.timestamp)
            return price
        return None

    def truncate(self):
        self.db_engine.execute("DELETE FROM fact_Price")

    