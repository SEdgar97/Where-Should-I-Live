import qol_db.db as qol_db

qol = qol_db.Database_QOL()

def get_Data(filter):
    city_json = get_data_from_db(filter)
    return city_json
"""
    import pandas as pd
    if len(filter) < 4:
        print('No no no, get more filters')
    else:
        # Send the filters to the database


        print(len(filter))


    city_df = pd.read_csv('cities_in_usa.csv')
    city_df = city_df.drop(axis=1,columns = ['country','city_id'])
    city_df = city_df.dropna()

    city_json = city_df.to_json()

    return city_json
"""

def get_data_from_db(filter):
    print(filter)
    criterias = [f.split(' ')[0] for f in filter] 
    return qol.get_cities_by_user_input(criterias)
    

filters = [0,1,2,3]