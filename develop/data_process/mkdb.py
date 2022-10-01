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
theme_list = [
    '사원',
    '캠핑',
    '숙소',
    '편의시설',
    '골프',
    '바다',
    '계곡',
    '스키',
    '박물관'
]
df = data_df3.copy()
df['theme'] = '미정'
df

#%%
filter_dest_name = ~df.관광지명.isna()
# temple_list = []
# for attr in attr_list:
#     if sum((attr[-1] == "사", len(attr) == 3)) == 2:
#         temple_list.append(attr)
filter_temple = df.관광지명.apply(lambda x:(str(x).endswith('사')) & (len(str(x)) == 3))
df.theme[filter_temple&filter_dest_name] = '사원'
df
#%%
camping_list = []
for attr in attr_list:
    if "캠핑" in attr:
        camping_list.append(attr)
camping_list = [t for t in camping_list if "/" in t and "예정" not in t and "리스트" not in t and "11번가" not in t]

#%%
sukso_list = []
for attr in attr_list:
    if sum(("호텔" in attr, "모텔" in attr, "스테이" in attr,"펜션" in attr)) == 1:
        sukso_list.append(attr)

fac_list = []
for attr in attr_list:
    if sum(("편의점" in attr, "마트" in attr, "노브랜드" in attr,"마켓" in attr,"다이소" in attr,"세븐일레븐" in attr,"cu" in attr)) == 1:
        fac_list.append(attr)

golf_list = []
for attr in attr_list:
    if sum(("골프" in attr, "CC" in attr, "GC" in attr,"gc" in attr, "cc" in attr,)) == 1:
        golf_list.append(attr)

sea_list = []
for attr in attr_list:
    if sum(("해수욕장" in attr, "해변" in attr, "항" in attr, "선착장" in attr, "해안" in attr)) == 1:
        if sum(("장점" not in attr, "변점" not in attr,"항점" not in attr,"영장" not in attr,"호텔" not in attr,"터미널" not in attr,"/" not in attr,"동점" not in attr,"예정" not in attr,"골프" not in attr,"자점" not in attr,"노브랜드" not in attr)) == 12:
            sea_list.append(attr)

gyegok_list = []
for attr in attr_list:
    if "계곡" in attr:
        if sum(("/" not in attr, "호텔" not in attr, "계곡길" not in attr)) == 3 :
            gyegok_list.append(attr)

ski_list = []
for attr in attr_list:
    if "스키" in attr:
        if sum(("샵" not in attr, "호텔" not in attr, "폐장" not in attr)) == 3:
            ski_list.append(attr)

museum_list = []
for attr in attr_list:
    if "박물관" in attr:
        if "예정" not in attr:
            museum_list.append(attr)
# %%
