# Import SQLAlchemy `automap` and other dependencies here
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, inspect, func
from   config import posgres_sql
from   config import posgres_user
import datetime as dt
import pandas as pd

class Database_QOL:
    def __init__(self):
        #################################################
        # Database Setup
        #################################################
        self.engine = create_engine(f'postgresql://{posgres_user}:{posgres_sql}@localhost:5433/qol_us_cities')
        # Use the Inspector to explore the database and print the table names
        self.inspector = inspect(self.engine)
        # reflect an existing database into a new model
        self.Base = automap_base()
        # reflect the tables
        self.Base.prepare(self.engine, reflect=True)
        self.session = Session(self.engine)
        self.Cities = self.Base.classes.cities
        self.Metrics = self.Base.classes.qol_indices

    def database_test(self):
        print(self.inspector.get_table_names())


    def get_cities_by_user_input(self, crime_index = 20, health_care_index = 60, pollution_index = 20):
        select_stmt = [ self.Metrics.city_id,
                self.Cities.city,
                self.Metrics.crime_index,
                self.Metrics.restaurant_price_index,
                self.Metrics.pollution_index,
                self.Metrics.health_care_index,
                self.Metrics.property_price_to_income_ratio,
                self.Metrics.traffic_index]
        results = self.session.query(*select_stmt).\
                                    filter(self.Metrics.crime_index <= crime_index). \
                                        filter(self.Metrics.health_care_index >= health_care_index). \
                                            filter(self.Metrics.pollution_index <= pollution_index). \
                                                filter(self.Metrics.city_id == self.Cities.city_id). \
                                                all()
        
        df = pd.DataFrame(results)
        print(df.head(20))
        return df.to_json(orient="records")

        