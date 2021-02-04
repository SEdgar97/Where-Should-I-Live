# Import SQLAlchemy `automap` and other dependencies here
import sqlalchemy
from sqlalchemy import or_
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
        self.Metrics = self.Base.classes.us_income_qol_indices

    def database_test(self):
        print(self.inspector.get_table_names())


    def get_cities_by_user_input(self, criterias):
        
        numbers = [int(x) for x in criterias[0].split('-')]
        crime_index_cond = [self.Metrics.crime_index > numbers[0], self.Metrics.crime_index <= numbers[1]]

        numbers = [int(x) for x in criterias[1].split('-')]
        health_care_index_cond = [self.Metrics.health_care_index > numbers[0], self.Metrics.health_care_index <= numbers[1]]

        numbers = [int(x) for x in criterias[2].split('-')]
        pollution_index_cond = [self.Metrics.pollution_index > numbers[0], self.Metrics.pollution_index <= numbers[1]]

        numbers = [int(x) for x in criterias[3].split('-')]
        restaurant_index = [self.Metrics.restaurant_price_index > numbers[0], self.Metrics.restaurant_price_index <= numbers[1]]

        select_stmt = [ self.Metrics.city_id,
                self.Cities.city,
                self.Cities.latitude,
                self.Cities.longitude,
                self.Metrics.crime_index,
                self.Metrics.climate_index,
                self.Metrics.restaurant_price_index,
                self.Metrics.pollution_index,
                self.Metrics.health_care_index,
                self.Metrics.property_price_to_income_ratio,
                self.Metrics.traffic_index,
                self.Metrics.median]
                
        results = self.session.query(*select_stmt).\
                                    filter(or_(*crime_index_cond)). \
                                        filter(or_(*health_care_index_cond)). \
                                            filter(or_(*pollution_index_cond)). \
                                                filter(or_(*restaurant_index)).\
                                                    filter(self.Metrics.city_id == self.Cities.city_id).all()                                                  
                                                
        df = pd.DataFrame(results)
        print(df.head(20))
        return df.to_json(orient="records")

        
