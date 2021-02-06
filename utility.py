import qol_db.db as qol_db
import pandas as pd

qol = qol_db.Database_QOL()

def get_Data(filter):
    city_json = get_data_from_db(filter)
    weight_df = pd.read_json(city_json)
    cols = ['climate_index','traffic_index','property_price_to_income_ratio']
    if weight_df.empty:
        return city_json
    else:
        for x in cols:
            max = weight_df[x].max()
            weight_df[x] = weight_df[x] / max

        weight_df['Sum'] = 0.2 * weight_df['climate_index'] + 0.2 * weight_df['traffic_index'] + 0.6 * weight_df['property_price_to_income_ratio']
        weight_df = weight_df.sort_values('Sum', ascending = False).reset_index()
        city_json = weight_df.to_json(orient = 'records')

        return city_json


def get_data_from_db(filter):
    print(filter)
    criterias = [f.split(' ')[0] for f in filter]
    print(criterias)
    return qol.get_cities_by_user_input(criterias)
    

filters = [0,1,2,3]