import pandas as pd
import json
import requests
import csv
from pprint import pprint

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
    header = ['city', 'city_id', 'health_care_index', 'crime_index','restaurant_price_index',
                'climate_index','pollution_index','quality_of_life_index','cpi_index','property_price_to_income_ratio',
                'purchasing_power_incl_rent_index']
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
                    data.append(row['city'])
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

        

if __name__ == "__main__":
    #request_cities_in_usa()
    #write_to_csv()
    request_indices_for_us_cities()
    request_cost_of_living_rankings()
        
