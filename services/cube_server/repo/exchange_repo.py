from model import Exchange
from sqlalchemy import asc, create_engine, desc
from sqlalchemy.orm import sessionmaker
from providers.logging_base import LoggingBase

class ExchangeRepository(LoggingBase):
    active_session = None
    def __init__(self, config_provider=None):
        super(ExchangeRepository, self).__init__(config_provider=config_provider)
        self.connection = config_provider.data["connection"]
        self.db_engine = create_engine(self.connection)
        self.session = sessionmaker(bind=self.db_engine)
        self.active_session = self.session()
    def get_count(self):
        return self.active_session.query(Exchange).count()
    def get_exchanges(self):
        items = self.active_session.query(Exchange).all()
        return items
    def add_get(self, exchange):
        """
        Add the provided exchange info to the database if it DNE
        expects dict of exchange values {"name":"", ...}
        """
        value_or_empty = lambda e, f: e[f] if f in e else ""
        if "name" in exchange:
            query = self.active_session.query(Exchange).filter_by(\
                name=exchange["name"])
        else:
            self.logger.warn("Name not provided so cannot get/add exchange.")
        if query.count() > 0:
            return query.first()
        else:
            insert_exchange = Exchange(name=exchange["name"], \
                public_url_base=value_or_empty(exchange, "public_url_base"), \
                currency_pair_lookup=value_or_empty(exchange, "currency_pair_lookup"))
            self.active_session.add(insert_exchange)
            self.active_session.commit()
            return insert_exchange
        return None

    def truncate(self):
        self.db_engine.execute("DELETE FROM dim_exchange")

    