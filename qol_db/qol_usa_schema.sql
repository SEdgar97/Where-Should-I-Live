DROP TABLE IF EXISTS cities CASCADE;
DROP TABLE IF EXISTS qol_indices CASCADE;
DROP TABLE IF EXISTS us_income CASCADE;

CREATE TABLE "cities" (
    "country" varchar(256)   NOT NULL,
    "city" varchar(256)   NOT NULL,    
     "latitude"  float NOT NULL,
     "longitude" float NOT NULL,
     "city_id"  int NOT NULL,
	CONSTRAINT "pk_city_id" PRIMARY KEY (
        "city_id"
     )
);

CREATE TABLE "qol_indices" (
    id SERIAL,
    CONSTRAINT "pk_id" PRIMARY KEY (
        "id"
    ),
     "city_id"  int NOT NULL,
	    FOREIGN KEY (city_id) REFERENCES cities(city_id),
    "health_care_index"  float,
    "crime_index" float,
    "restaurant_price_index" float,
    "climate_index" float,
    "pollution_index" float,
    "quality_of_life_index" float,
    "cpi_index" float,
    "property_price_to_income_ratio" float,
    "purchasing_power_incl_rent_index" float,
    "traffic_index" float
);

DROP TABLE IF EXISTS us_income CASCADE;
CREATE TABLE "us_income" (
    id SERIAL,
    CONSTRAINT "pk_us_income_id" PRIMARY KEY (
        "id"
    ),
     "city_id"  int NOT NULL,
	    FOREIGN KEY (city_id) REFERENCES cities(city_id),
    "mean"  float,
    "median" float,
    "std_dev" float,
    "sum_w" float
);

DROP TABLE IF EXISTS pollution_ranking CASCADE;
CREATE TABLE "pollution_ranking" (
    id SERIAL,
    CONSTRAINT "pk_pollution_ranking_id" PRIMARY KEY (
        "id"
    ),
     "city_id"  int NOT NULL,
	    FOREIGN KEY (city_id) REFERENCES cities(city_id),
    "ranking" int,
    "pollution_index"  float,
    "exp_pollution_index" float,
);

DROP TABLE IF EXISTS property_price_ranking CASCADE;
CREATE TABLE "property_price_ranking" (
    id SERIAL,
    CONSTRAINT "pk_property_price_ranking_id" PRIMARY KEY (
        "id"
    ),
     "city_id"  int NOT NULL,
	    FOREIGN KEY (city_id) REFERENCES cities(city_id),
    "ranking" int,
    "house_price_to_income_ratio"  float,
    "affordability_index" float,
);

DROP TABLE IF EXISTS qol_ranking CASCADE;
CREATE TABLE "qol_ranking" (
    id SERIAL,
    CONSTRAINT "pk_qol_ranking_id" PRIMARY KEY (
        "id"
    ),
     "city_id"  int NOT NULL,
	    FOREIGN KEY (city_id) REFERENCES cities(city_id),
    "ranking" int,
    "traffic_time_index"  float,
    "quality_of_life_index" float,
    "healthcare_index" float,
    "purchasing_power_incl_rent_index" float,
    "house_price_to_income_ratio" float,
    "pollution_index" float,
    "climate_index" float,
    "safety_index" float

);
