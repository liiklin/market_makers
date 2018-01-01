from sqlalchemy import asc, create_engine, desc
from sqlalchemy.orm import sessionmaker
from model import DimDateTime
from providers.logging_base import LoggingBase

class DateRepo(LoggingBase):
    """
    Repo for Date
    """
    db_url = ""
    session = None
    active_session = None
    db_engine = None
    def __init__(self, config_provider=None):
        super(DateRepo, self).__init__(config_provider=config_provider)
        if not DateRepo.db_engine:
            self.connection =  config_provider.data["connection"]
            DateRepo.db_engine = create_engine(self.connection)
            DateRepo.session = sessionmaker(bind=self.db_engine)
            DateRepo.active_session = self.session()

    def add_get(self, date=None, timestamp=None):
        """
        Add the provided date to the database if it DNE
        """
        if timestamp:
            date = DimDateTime(timestamp=timestamp)
        if date:
            query = self.get_filter_query(date)
            if query.count() > 0:
                return query.first()
            else:
                self.logger.info("Inserting DimDateTime %s", date.timestamp)
                self.active_session.add(date)
                self.active_session.commit()
                return date
        else:
            raise Exception("Invalid date or timestamp, cannot add.")

    def get_filter_query(self, date):
        return self.active_session.query(DimDateTime).filter_by(\
            year=date.year, month=date.month, day=date.day, \
            hour=date.hour, minute=date.minute)

    def get_by_id(self, hash_value):
        return self.active_session.query(DimDateTime).filter_by(hash_value=hash_value).first()

    def get(self, date):
        """
        Get the matchin date entry from the database, None if it DNE
        """
        query = self.get_filter_query(date)
        if query.count() > 0:
            return query.first()
        else:
            return None

    def delete(self, date):
        """
        Delete the date entry from the table
        """

        item = self.get_filter_query(date).first()
        self.active_session.delete(item)

    def truncate(self):
        #self.db_engine.execute("DELETE FROM encounter_drug_admin_association;")
        #self.db_engine.execute("DELETE FROM fact_patient_encounter_anesthesia;")
        self.db_engine.execute("DELETE FROM dim_date;")

    def get_max(self):
        return  self.active_session.query(DimDateTime).order_by(desc(DimDateTime.date)).first()

    def get_min(self):
        return  self.active_session.query(DimDateTime).order_by(asc(DimDateTime.date)).first()

    def get_range(self, min_date, max_date):
        """
        return range of dates inclusive. If min_date > max_date, consider if that is what you intended.
        """
        return self.active_session.query(DimDateTime).filter(DimDateTime.date.between(str(min_date),str(max_date))).all()

