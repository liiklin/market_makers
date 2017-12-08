from model import CurrencyPair
from sqlalchemy import asc, create_engine, desc
from sqlalchemy.orm import sessionmaker
from providers.logging_base import LoggingBase

class CurrencyPairRepository(LoggingBase):
    active_session = None
    db_engine = None
    session = None
    def __init__(self, config_provider=None):
        super(CurrencyPairRepository, self).__init__(config_provider=config_provider)
        if not CurrencyPairRepository.db_engine:
            self.connection = config_provider.data["connection"]
            CurrencyPairRepository.db_engine = create_engine(self.connection)
            CurrencyPairRepository.session = sessionmaker(bind=self.db_engine)
            CurrencyPairRepository.active_session = CurrencyPairRepository.session()

    def get_count(self):
        return self.active_session.query(CurrencyPair).count()

    def get_pairs(self):
        items = self.active_session.query(CurrencyPair).all()
        return items

    def add_get(self, CurrencyPair):
        """
        Add the provided CurrencyPair info to the database if it DNE
        expects dict of CurrencyPair values {"name":"", ...}
        """
        value_or_empty = lambda e, f: e[f] if f in e else ""
        query = CurrencyPairRepository.active_session.query(CurrencyPair).filter_by(\
            name=CurrencyPair.name)
        if query.count() > 0:
            return query.first()
        else:
            self.logger.info("Inserted new CurrencyPair %s", CurrencyPair.name)
            insert_CurrencyPair = CurrencyPair
            CurrencyPairRepository.active_session.add(insert_CurrencyPair)
            CurrencyPairRepository.active_session.commit()
            return insert_CurrencyPair
        return None

    def truncate(self):
        self.db_engine.execute("DELETE FROM dim_currency_pair")

    