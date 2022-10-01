#%%
import sys # 상위 경로의 파일 포함
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from lib_database import *

import os
import pandas as pd
import numpy as np

#%% 
db = connect_database('skbs')
col_region          = use(db, 'region')
col_region_detail   = use(db, 'region_detail')

#%% region info
cur = find(col_region)
data_list = list(cur)
data_df1 = pd.DataFrame(data_list)
# 시군구명 - 강원도 하나의 데이터, 쓰레기

# %% region detail info
cur = find(col_region_detail)
data_list = list(cur)
data_df2 = pd.DataFrame(data_list)

# %%
data_df3 = pd.read_csv(
    r"C:\Users\alllh\Documents\카카오톡 받은 파일\지역 전체.csv"
)

# %%
import csv

region_names = data_df3.지역.unique()
region_dict = dict()
for region in region_names:
    x = region.split()
    if len(x) == 1: continue
    region_dict.setdefault(x[0], [])
    region_dict[x[0]].append(' '.join(x[1:]))

with open('output/region_dict.csv','w', encoding='utf8') as f:
    w = csv.writer(f)
    w.writerow(region_dict.keys())
    w.writerow(region_dict.values())

#%%

# <todo>
# source
# ㄴregion
#     ㄴregion_detail

dest_dict = dict()
for region, region_details in region_dict.items():
    dest_dict.setdefault(region, [])
    dest_dict[region] = data_df3.관광지명[(~data_df3.관광지명.isna())&(data_df3.지역==region)].to_list()
    for detail in region_details:
        region_detail = region + ' ' + detail
        dest_dict.setdefault(region_detail, [])
        dest_dict[region_detail] = data_df3.관광지명[(~data_df3.관광지명.isna())&(data_df3.지역==region_detail)].to_list()

with open('output/dest_dict.csv','w', encoding='utf8') as f:
    w = csv.writer(f)
    w.writerow(dest_dict.keys())
    w.writerow(dest_dict.values())

# %%
df = pd.read_csv('output/dest_dict.csv')
df
# %%
