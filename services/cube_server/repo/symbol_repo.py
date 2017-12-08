from model import Symbol
from sqlalchemy import asc, create_engine, desc
from sqlalchemy.orm import sessionmaker
from providers.logging_base import LoggingBase

class SymbolRepository(LoggingBase):
    active_session = None
    db_engine = None
    session = None
    def __init__(self, config_provider=None):
        super(SymbolRepository, self).__init__(config_provider=config_provider)
        if not SymbolRepository.db_engine:
            self.connection = config_provider.data["connection"]
            SymbolRepository.db_engine = create_engine(self.connection)
            SymbolRepository.session = sessionmaker(bind=self.db_engine)
            SymbolRepository.active_session = SymbolRepository.session()

    def get_count(self):
        return self.active_session.query(Symbol).count()

    def get_exchanges(self):
        items = self.active_session.query(Symbol).all()
        return items

    def add_get(self, symbol):
        """
        Add the provided symbol info to the database if it DNE
        expects dict of symbol values {"name":"", ...}
        """
        value_or_empty = lambda e, f: e[f] if f in e else ""
        query = SymbolRepository.active_session.query(Symbol).filter_by(\
            name=symbol.name)
        if query.count() > 0:
            return query.first()
        else:
            self.logger.info("Inserted new symbol %s", symbol.name)
            insert_symbol = symbol
            SymbolRepository.active_session.add(insert_symbol)
            SymbolRepository.active_session.commit()
            return insert_symbol
        return None

    def truncate(self):
        self.db_engine.execute("DELETE FROM dim_symbol")

    