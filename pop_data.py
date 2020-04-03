# -*- coding: utf-8 -*-
"""
Created on Wed Apr  1 14:32:29 2020

@author: metalcorebear
"""

import pandas as pd
import os
import glob
import numpy as np

def get_files(output_path):
    out_files = []
    for root, dirs, files in os.walk(output_path):
        for file_ in files:
            if ('.csv') in file_:
                out_files.append(os.path.join(root, file_))
    return out_files

df = pd.read_csv('all_data.csv', encoding='UTF8')

new_df = df[['STNAME', 'CTYNAME', 'YEAR', 'AGEGRP', 'TOT_POP']]

filtered_df = new_df[new_df['YEAR'] == 11

filtered_df['RISK'] = filtered_df.AGEGRP.apply(lambda x: 'HIGH' if x >= 13 else 'LOW')

out_df = filtered_df[['STNAME', 'CTYNAME', 'TOT_POP', 'RISK']]

df_2 = out_df.groupby(['CTYNAME', 'RISK']).sum()

output_path = r'C:\Users\markmbailey\Documents\Python\Helper_Scripts\social_networks\COVID\PROCESSED_DATA'
states = ['Washington', 'Montana', 'North Dakota', 'South Dakota', 'Oregon', 'Idaho', 'Wyoming', 'Colorado', 'Utah', 'Nevada', 'California', 'Arizona']
for state in states:
    n_df = out_df[out_df['STNAME']==state].groupby(['CTYNAME', 'RISK']).sum()
    n_df.to_csv(os.path.join(output_path, state + '.csv'), encoding='UTF8')


hospitals = pd.read_csv('Hospitals.csv')

hospitals_clean = hospitals[hospitals['STATUS']=='OPEN']
hospitals_clean = hospitals_clean[hospitals_clean['BEDS']>=0]

hospitals_out = hospitals_clean[['COUNTY', 'STATE', 'BEDS']]

hospitals_out['COUNTY'] = hospitals_out['COUNTY'].str.capitalize()

hospitals_out['COUNTY'] = hospitals_out.COUNTY.apply(lambda x: x + ' County')

state_symbols = ['WA', 'MT', 'ND', 'SD', 'OR', 'ID', 'WY', 'CO', 'UT', 'NV', 'CA', 'AZ']
for state in state_symbols:
    s_df = hospitals_out[hospitals_out['STATE']==state].groupby('COUNTY').sum()
    s_df.to_csv(os.path.join(output_path, state + '_hospital_beds.csv'), encoding='UTF8')

all_files = get_files(output_path)

df_list = []
for i in range(len(states)):
    state = states[i]
    symbol = state_symbols[i]
    for item in all_files:
        if state in os.path.basename(item):
            state_file = item
        if symbol in os.path.basename(item):
            hospital_file = item
    hospital_df = pd.read_csv(hospital_file)
    #hospital_df.set_index('COUNTY')
    state_df = pd.read_csv(state_file)
    #state_df.set_index('CTYNAME')
    hospital_df['COUNTY'] = hospital_df['COUNTY'].str.title()
    new_df = pd.merge(state_df, hospital_df, left_on='CTYNAME', right_on='COUNTY', how='outer')
    state_list = [state for n in range(len(new_df))]
    state_name_df = pd.DataFrame({'STATE':state_list})
    new_df = new_df.join(state_name_df)
    df_list.append(new_df)
    #new_df.to_csv(os.path.join(merged_path, state + '.csv'))
merged_df = pd.concat(df_list, ignore_index=True, sort=False)
merged_df['TOT_POP_HIGH'] = np.where(merged_df['RISK']=='HIGH', merged_df['TOT_POP'], 0)
merged_df['TOT_POP_LOW'] = np.where(merged_df['RISK']=='LOW', merged_df['TOT_POP'], 0)
merged_df_high = merged_df[merged_df['RISK']=='HIGH']
merged_df_high.drop(['RISK'], axis=1, inplace=True)
merged_df_high.drop(['TOT_POP'], axis=1, inplace=True)
merged_df_low = merged_df[merged_df['RISK']=='LOW']
merged_df_low.drop(['RISK'], axis=1, inplace=True)
merged_df_low.drop(['TOT_POP'], axis=1, inplace=True)

merged_df_low['TOT_POP_HIGH'] = merged_df_low['TOT_POP_HIGH'].replace({0:None})
merged_df_high['TOT_POP_LOW'] = merged_df_high['TOT_POP_LOW'].replace({0:None})

merged_df_out = merged_df_high.combine_first(merged_df_low)

merged_df_out.fillna(0, inplace=True)

merged_df_out['BED_STR'] = merged_df_out.BEDS.apply(lambda x: str(x))

merged_df_out = merged_df_out.astype(str)

new_list = []
for i in range(len(merged_df_out)):
    new_list.append(str(merged_df_out['CTYNAME'][i]) + str(merged_df_out['COUNTY'][i]) + str(merged_df_out['BED_STR'][i]) + str(merged_df_out['STATE'][i]))

merged_df_out['key'] = merged_df_out.CTYNAME + merged_df_out.COUNTY + merged_df_out.BED_STR + merged_df_out.STATE

merged_df_out_high = merged_df_out[merged_df_out['TOT_POP_HIGH'] == '0.0']
merged_df_out_high = merged_df_out_high[['key', 'TOT_POP_LOW']]
merged_df_out_low = merged_df_out[merged_df_out['TOT_POP_LOW'] == '0.0']

merged_df_out_final = pd.merge(merged_df_out_low, merged_df_out_high, on='key', how='outer')

merged_df_final = merged_df_out.groupby(['CTYNAME', 'COUNTY', 'BEDS', 'STATE']).agg(sum)

#final_merged_df = pd.merge(merged_df_high, merged_df_low_out, suffixes=('_high_risk', '_low_risk'), on='CTYNAME', how='outer')
merged_df_out_final.to_csv(os.path.join(merged_path, 'FINAL_JOIN.csv'))

    