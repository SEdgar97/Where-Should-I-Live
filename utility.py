def get_Data(filter):
    import pandas as pd
    if len(filter) < 4:
        print('No no no, get more filters')
    else:
        print(len(filter))
    city_df = pd.read_csv('cities_in_usa.csv')
    city_df = city_df.drop(axis=1,columns = ['country','city_id'])


    return city_df




filters = [0,1,2,3]

print(get_Data(filters).head())