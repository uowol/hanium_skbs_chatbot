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
    r"C:\Users\alllh\Documents\카카오톡 받은 파일\지역 전체.csv",
).iloc[:,1:]

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

#%% 관광지별

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

#%% 테마별
# attr_list = list(set(data_df3["관광지명"].dropna()))
# attr_list
df = data_df3.copy()
df['theme'] = [[] for _ in range(len(df))]
df_list = set()

#%%
filter_dest_name = ~df.관광지명.isna()

filter_temple = df.관광지명.apply(lambda x:(str(x).endswith('사')) & (len(str(x)) == 3))
df.theme[filter_temple&filter_dest_name].apply(lambda x: x.append('사원'))
#%%
df_list.add('캠핑')
filter_camp = df.관광지명.apply(lambda x:
    ('캠핑' in str(x))
    & ("/" not in str(x)) 
    & ('예정' not in str(x))
    & ('리스트' not in str(x))
    & ('11번가' not in str(x))
)
df.theme[filter_camp&filter_dest_name].apply(lambda x: x.append('캠핑'))
df.theme
#%%
df_list.add('숙소')
filter_sukso = df.관광지명.apply(lambda x:
    ("호텔" in str(x)) 
    | ('모텔' in str(x))
    | ('스테이' in str(x))
    | ('펜션' in str(x))
    | ('쏠비치' in str(x)) 
    | ('리조트' in str(x)) 
)
df.theme[filter_sukso&filter_dest_name].apply(lambda x: x.append('숙소'))
df.theme
#%%
df_list.add('섬')
filter_island = df.관광지명.apply(lambda x:
    (str(x).endswith('섬')) 
    | (str(x).endswith('도'))
)
df.theme[filter_island&filter_dest_name].apply(lambda x: x.append('섬'))
df.theme
#%%
df_list.add('편의시설')
filter_fac = df.관광지명.apply(lambda x:
    ("편의점" in str(x)) 
    | ('마트' in str(x))
    | ('노브랜드' in str(x))
    | ('마켓' in str(x))
    | ('다이소' in str(x))
    | ('세븐일레븐' in str(x))
    | ('cu' in str(x))
)
df.theme[filter_fac&filter_dest_name].apply(lambda x: x.append('편의시설'))
df.theme
#%%
df_list.add('골프')
filter_golf = df.관광지명.apply(lambda x:
    ("골프" in str(x)) 
    | ('CC' in str(x))
    | ('GC' in str(x))
    | ('gc' in str(x))
    | ('cc' in str(x))
)
df.theme[filter_golf&filter_dest_name].apply(lambda x: x.append('골프'))
df.theme
#%%
df_list.add('바다')
filter_sea = df.관광지명.apply(lambda x:
    ("해수욕장" in str(x)) 
    | ('해변' in str(x))
    | ('항' in str(x))
    | ('선착장' in str(x))
    | ('해안' in str(x))
    | ('쏠비치' in str(x))
    & ('장점' not in str(x))
    & ('변점' not in str(x))
    & ('항점' not in str(x))
    & ('영장' not in str(x))
    & ('호텔' not in str(x))
    & ('터미널' not in str(x))
    & ('/' not in str(x))
    & ('동점' not in str(x))
    & ('예정' not in str(x))
    & ('골프' not in str(x))
    & ('자점' not in str(x))
    & ('노브랜드' not in str(x))
)
df.theme[filter_sea&filter_dest_name].apply(lambda x: x.append('바다'))
df.theme
#%%
df_list.add('계곡')
filter_gyegok = df.관광지명.apply(lambda x:
    ("계곡" in str(x)) 
    & ("/" not in str(x)) 
    & ('계곡길' not in str(x))
)
df.theme[filter_gyegok&filter_dest_name].apply(lambda x: x.append('계곡'))
df.theme
#%%
df_list.add('스키')
filter_ski = df.관광지명.apply(lambda x:
    ("스키" in str(x)) 
    & ('샵' not in str(x))
    & ('호텔' not in str(x))
    & ('폐장' not in str(x))
)
df.theme[filter_ski&filter_dest_name].apply(lambda x: x.append('스키'))
df.theme
#%%
df_list.add('박물관')
filter_museum = df.관광지명.apply(lambda x:
    ("박물관" in str(x)) 
    & ('예정' not in str(x))
)
df.theme[filter_museum&filter_dest_name].apply(lambda x: x.append('박물관'))
#%%
df_list.add('시장')
filter_sijang = df.관광지명.apply(lambda x:
    ("시장" in str(x)) 
)
df.theme[filter_sijang&filter_dest_name].apply(lambda x: x.append('시장'))
#%%
# theme_list = list(df.theme.unique())
df_list, df.theme
# %%
df.to_csv('output/data_theme_plus.csv', index=False)
# %%
df.관광지명[df.theme.apply(len)==0].dropna()

# %%
