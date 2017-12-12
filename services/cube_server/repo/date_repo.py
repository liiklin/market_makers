from sqlalchemy import asc, create_engine, desc
from sqlalchemy.orm import sessionmaker
from model import DimDate

class DateRepo(object):
    """
    Repo for Date
    """
    db_url = ""
    session = None
    active_session = None
    def __init__(self, connection=""):
        self.connection = connection
        self.db_engine = create_engine(self.connection)
        self.session = sessionmaker(bind=self.db_engine)
        self.active_session = self.session()

    def add_get(self, date):
        """
        Add the provided date to the database if it DNE
        """
        query = self.get_filter_query(date)
        if query.count() > 0:
            return query.first()
        else:
            insert_date = DimDate(year=date.year, month=date.month,\
                day=date.day, hour=date.hour, minute=date.minute, \
                timestamp=date.timestamp,hash_value=date.hash_value)
            self.active_session.add(insert_date)
            self.active_session.commit()
            return insert_date
    def get_filter_query(self, date):
        return self.active_session.query(DimDate).filter_by(\
            year=date.year, month=date.month, day=date.day, \
            hour=date.hour, minute=date.minute)
    def get_by_id(self, hash_value):
        return self.active_session.query(DimDate).filter_by(hash_value=hash_value).first()

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
        return  self.active_session.query(DimDate).order_by(desc(DimDate.date)).first()

    def get_min(self):
        return  self.active_session.query(DimDate).order_by(asc(DimDate.date)).first()

    def get_range(self, min_date, max_date):
        """
        return range of dates inclusive. If min_date > max_date, consider if that is what you intended.
        """
        return self.active_session.query(DimDate).filter(DimDate.date.between(str(min_date),str(max_date))).all()

