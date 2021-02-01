import pandas as pd
import json
import requests
import csv
from pprint import pprint
import qol_db.db as db

api_key = "oez5tbfb8gztav"

def read_cities():
    filepath = "Resources/cities.csv"
    cities_df = pd.read_csv(filepath, index_col=0)
    us_cities = cities_df.loc[cities_df['Country'] == 'United States']

def request_cities_in_usa():
    url = f'https://www.numbeo.com/api/cities?api_key={api_key}&country=United States'
    print(url)
    response = requests.get(url)
    response.raise_for_status()
    
    json_file_name = "Resources/cities_in_usa.json"
    with open(json_file_name, "w") as json_file:
        json.dump(response.json(), json_file)

def write_cities_to_csv():
    with open('Resources/cities_in_usa.json') as data_file: 
        data = json.load(data_file)
        df = pd.DataFrame.from_dict(data['cities'], orient='columns')
        print(df.head())
    df.to_csv("Resources/cities_in_usa.csv", index=False)

def request_indices_for_us_cities():
    header = ['city_id', 'health_care_index', 'crime_index','restaurant_price_index',
                'climate_index','pollution_index','quality_of_life_index','cpi_index','property_price_to_income_ratio',
                'purchasing_power_incl_rent_index', 'traffic_index']
    i = 0
    with open("Resources/clean_us_cities.csv",mode='w') as clean_cities_file:
        clean_cities_writer = csv.writer(clean_cities_file, delimiter=',')
        with open("Resources/cities_indices.csv",mode='w') as indices_file:
            index_writer = csv.writer(indices_file, delimiter=',')
            index_writer.writerow(header)
            with open("Resources/cities_in_usa.csv",'r') as csvfile:
                zeroCols = 0
                reader = csv.DictReader(csvfile)
                      
                for row in reader:
                    if i==0:
                        clean_cities_writer.writerow(row)
                        pass 
                    i+=1                    
                    city_id = row['city_id']
                    url = f'https://www.numbeo.com/api/indices?api_key={api_key}&city_id={city_id}'
                    response = requests.get(url)
                    response_json = response.json()
                
                    data = []
                    #data.append(row['city'])
                    data.append(row['city_id'])
                    if response_json.get('health_care_index'):
                        data.append(response_json.get('health_care_index'))
                    else:
                        data.append(0)
                        zeroCols += 1
                    if response_json.get('crime_index'):
                        data.append(response_json.get('crime_index'))
                    else:
                        data.append(0)
                        zeroCols += 1
                    if response_json.get('restaurant_price_index'):
                        data.append(response_json.get('restaurant_price_index'))
                    else:
                        data.append(0)
                        zeroCols += 1
                    if response_json.get('climate_index'):
                        data.append(response_json.get('climate_index'))
                    else:
                        zeroCols += 1
                        data.append(0)
                    if response_json.get('pollution_index'):
                        data.append(response_json.get('pollution_index'))
                    else:
                        zeroCols += 1
                        data.append(0)
                    if response_json.get('quality_of_life_index'):
                        data.append(response_json.get('quality_of_life_index'))
                    else:
                        zeroCols += 1
                        data.append(0)        
                    if response_json.get('cpi_index'):
                        data.append(response_json.get('cpi_index'))
                    else:
                        zeroCols += 1
                        data.append(0)
                    if response_json.get('property_price_to_income_ratio'):
                        data.append(response_json.get('property_price_to_income_ratio'))
                    else:
                        zeroCols += 1
                        data.append(0)
                    if response_json.get('purchasing_power_incl_rent_index'):
                        data.append(response_json.get('purchasing_power_incl_rent_index'))
                    else:
                        zeroCols += 1
                        data.append(0)
                    if response_json.get('traffic_index'):
                        data.append(response_json.get('traffic_index'))
                    else:
                        zeroCols += 1
                        data.append(0)
                    if zeroCols <= 3:  
                        index_writer.writerow(data)
                        city = list(row.values())
                        clean_cities_writer.writerow(city)
                        print(row.values(),city)
                    zeroCols = 0

def request_cost_of_living_rankings():
    url = f'https://www.numbeo.com/api/rankings_by_city_current?api_key={api_key}&section=1'
    response = requests.get(url)
    response_json = response.json()
    df = pd.DataFrame.from_dict(response_json)
    df = df.loc[df['country'] == 'United States']
    df.to_csv("Resources/col_rankings.csv")

    url = f'https://www.numbeo.com/api/rankings_by_city_current?api_key={api_key}&section=2'
    response = requests.get(url)
    response_json = response.json()
    df = pd.DataFrame.from_dict(response_json)
    df = df.loc[df['country'] == 'United States']
    df.to_csv("Resources/property_prices.csv")

    url = f'https://www.numbeo.com/api/rankings_by_city_current?api_key={api_key}&section=7'
    response = requests.get(url)
    response_json = response.json()
    df = pd.DataFrame.from_dict(response_json)
    df = df.loc[df['country'] == 'United States']
    df.to_csv("Resources/crime_rankings.csv")

    url = f'https://www.numbeo.com/api/rankings_by_city_current?api_key={api_key}&section=8'
    response = requests.get(url)
    response_json = response.json()
    df = pd.DataFrame.from_dict(response_json)
    df = df.loc[df['country'] == 'United States']
    df.to_csv("Resources/pollution_rankings.csv")

    url = f'https://www.numbeo.com/api/rankings_by_city_current?api_key={api_key}&section=12'
    response = requests.get(url)
    response_json = response.json()
    df = pd.DataFrame.from_dict(response_json)
    df = df.loc[df['country'] == 'United States']
    df.to_csv("Resources/qol_rankings.csv")

def clean_median_income():
    filepath = "Resources/merge3.csv"
    median_df = pd.read_csv(filepath)
    median_df = median_df.drop(['country','cities','state','latitude','longitude','Zip_Code','ALand','ALand'], axis=1)
    print(median_df.head())
    median_df = median_df.rename(columns={"Mean": "mean", "Median": "median", "Stdev": "std_dev"}, errors="raise")
    median_df.to_csv("Resources/median_income_db.csv")

def rearrange_columns_for_db():
    filepath = "Resources/clean_us_cities.csv"
    cities_df = pd.read_csv(filepath, index_col=0)
    cols_to_order=['city','latitude','longitude','city_id']
    new_columns = cols_to_order + (cities_df.columns.drop(cols_to_order).tolist())
    cities_df = cities_df[new_columns]
    filepath = "Resources/clean_us_cities_db.csv"
    cities_df.to_csv(filepath)
   
def take_care_of_zeros():
    filepath = "Resources/cities_indices.csv"
    indices_df = pd.read_csv(filepath, index_col=0)
    indices_df['health_care_index']=indices_df['health_care_index'].replace(0,indices_df['health_care_index'].mean())
    indices_df['crime_index']=indices_df['crime_index'].replace(0,indices_df['crime_index'].mean())
    indices_df['restaurant_price_index']=indices_df['restaurant_price_index'].replace(0,indices_df['restaurant_price_index'].mean())
    indices_df['climate_index']=indices_df['climate_index'].replace(0,indices_df['climate_index'].mean())
    indices_df['pollution_index']=indices_df['pollution_index'].replace(0,indices_df['pollution_index'].mean())
    indices_df['quality_of_life_index']=indices_df['quality_of_life_index'].replace(0,indices_df['quality_of_life_index'].mean())
    indices_df['cpi_index']=indices_df['cpi_index'].replace(0,indices_df['cpi_index'].mean())
    indices_df['property_price_to_income_ratio']=indices_df['property_price_to_income_ratio'].replace(0,indices_df['property_price_to_income_ratio'].mean())
    indices_df['purchasing_power_incl_rent_index']=indices_df['purchasing_power_incl_rent_index'].replace(0,indices_df['purchasing_power_incl_rent_index'].mean())
    indices_df['traffic_index']=indices_df['traffic_index'].replace(0,indices_df['traffic_index'].mean())
    indices_df = indices_df.round(3)
    filepath = "Resources/cities_indices_db.csv"
    indices_df.to_csv(filepath)
        
#ETL Part here...

    if __name__ == "__main__":
        #Request all cities from usa from nombeo site
        #request_cities_in_usa()
        #write_to_csv()
        #request_indices_for_us_cities()
        #request_cost_of_living_rankings()
        #rearrange_columns_for_db()
        #take_care_of_zeros()
        clean_median_income()
