def get_Data(filter):
    import pandas as pd
    if len(filter) < 4:
        print('No no no, get more filters')
    else:
        print(len(filter))
    city_df = pd.read_csv('cities_in_usa.csv')
    city_df = city_df.drop(axis=1,columns = ['country','city_id'])
    city_df = city_df.dropna()

    city_json = city_df.to_json()

    return city_json




filters = [0,1,2,3]