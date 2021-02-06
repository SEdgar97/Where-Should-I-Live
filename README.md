# Where-Should-I-Live

## In these unprecedented times…

Given the massive number of history changing events that have happened in the last 12 months many people have found themselves asking just this question. This project aims to provide a simple way for people to find cities in the US that fit a given set of criteria to live in.

Proposed Datasets:
1. Movehub: https://www.kaggle.com/blitzr/movehub-city-rankings?select=movehubcostofliving.csv
2. National Parks Data - https://www.latlong.net/category/national-parks-236-42.html
3. Numbeo: https://www.numbeo.com/api/doc.jsp


We will use this data to compare cities across the US with respect to cost of living, consumer prices, crime rates, education, and other factors. We will then recommend to the user the best places that they may want to consider for a future place to live based upon their input criteria weighted by cost of living in each location.

We will use a sequential database based upon city name as the primary key. We will use a reference table which will contain the locations of each city to be placed on the map. Our flask server will communicate with the front end webpage which will take the user’s filtering preferences in order to generate the correct city names.

### Simple Diagram of Structure
<p><img src = "https://user-images.githubusercontent.com/35506304/105790782-eb071900-5f52-11eb-8001-b727a56894a6.JPG"></p>

serevr.py :  Flask app
static/js: has javascript and Ajax code
qol_db/: has hooks to db
clean_data.py : All request to Nombeo website, cleaning and storing the db
index.html code that has hooks to Plot,db and filters
