DROP TABLE IF EXISTS cities CASCADE;
DROP TABLE IF EXISTS qol_numbers CASCADE;
DROP TABLE IF EXISTS qol_indices CASCADE;

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