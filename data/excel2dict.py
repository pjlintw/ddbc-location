import pandas as pd
import os

def excel_to_dict_from_xlsx(fn):
    """Read excel form file
    """
    data = pd.read_excel(fn, index_col=0)

    output_dict = dict()
    for ids, row in data.iterrows():
        output_dict[ids] = row.tolist()

    return output_dict

source_fn = '../../續高僧傳遊方表格01.xlsx'
fn = 'openpyxl_6000.xlsx'
excel_dict = excel_to_dict_from_xlsx(fn)

#print(excel_dict['中國'])

data = pd.read_excel(source_fn)

for ids, row in data.iterrows():
    # 國、州、郡、縣、公署、地景、宮殿、關塞、寺廟、山、川
    loc_list = row[5:17].tolist()
    loc_list.reverse()

    for loc_name in loc_list:
        if type(loc_name) == str and loc_name in excel_dict:
            #print(loc_name)
            database_ids, loc_long, loc_lat, dynasty, district = excel_dict[loc_name]
            data.loc[ids, 'data_ids'] = database_ids
            data.loc[ids, 'long'] = loc_long
            data.loc[ids, 'lat'] = loc_lat
            data.loc[ids, 'dynasty'] = dynasty
            data.loc[ids, 'district'] = str(district)
        else:
            continue


data.to_excel('new.xlsx')
