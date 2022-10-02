import os
import csv
import pandas as pd
import pymongo
from lib_dialogflow_response import *

# database 연결
def connect_database(db):
    connect_to = pymongo.MongoClient("mongodb://localhost:27017")
    mdb = connect_to[db]
    return mdb

# collection 연결
def use(db, collection):
    return db[collection]

def insert(collection, data_list):
    collection.insert_many(data_list)

def find(collection, options = {}):
    searched = collection.find(options)
    return searched

def update(collection, options = {}):
    collection.update_many(options)

def delete(collection, options = {}):
    collection.delete_many(options)








#원하는 db에 여행지 정보 저장
#path는 데이터 파일들 존재 경로
#collection은 저장될 collection
#region은 db에 "지역" : "region"으로 추가될 지역 이름
def save_region(path, collection, region):
    os.chdir(path)
    filelist = os.listdir(path)
    for file in filelist:
        df = pd.read_csv(file, encoding = "CP949")
        header = df.columns.values.tolist()
        c_file = open(file, encoding = "CP949")
        f_read = csv.DictReader(c_file)
        data = []
        for each in f_read:
            row = {}
            for field in header:
                row[field] = each[field]
            data.append(row)
        insert(collection, data)
    cur = list(find(collection))
    count = 0
    for i in range(len(cur)):
        if "지역" in list(cur[i].keys()):
            count = count + 1
    if count == 0:
        collection.update_many({}, {"$set":{"지역":region}})
    else:
        collection.update_many({"지역": {"$exists": False}}, {"$set":{"지역":region}})

        

# 몽고 db에 구분 없이 저장된 지역별 모든 데이터를
# 파일별로 나누어 리스트에 저장하는 함수
def db_to_list(collection):
    cur = find(collection)
    data_list = []
    key_names = []
    temp = []
    merged_data = []
    for doc in cur:
        data_list.append(doc)
    for i in range(len(data_list)):
        key_names.append(data_list[i].keys())
    for key in key_names:
        if key not in temp:
            temp.append(key)
    for j in range(len(temp)):
        tmp = []
        for data in data_list:
            if data.keys() == temp[j]:
                tmp.append(data)
        merged_data.append(tmp)
    return merged_data

#데이터프레임 리스트로 불러오는 함수
def to_dflist(data):
    df_list = []
    for i in range(len(data)):
        df_list.append(pd.DataFrame(data[i]))
    return df_list

def df_join(data):
    df = pd.concat(data, ignore_index=True)
    return df


#원하는 db에 여행지 정보 저장
#path는 데이터 파일들 존재 경로
#collection은 저장될 collection
#spot은 db에 "분류" : "spot"으로 추가될 지역 이름
def spot_save(path, collection, spot):
    try:
        os.chdir(path)
        filelist = os.listdir(path)
        for file in filelist:
            df = pd.read_csv(file, encoding = "CP949")
            header = df.columns.values.tolist()
            c_file = open(file, encoding = "CP949")
            f_read = csv.DictReader(c_file)
            data = []
            for each in f_read:
                row = {}
                for field in header:
                    row[field] = each[field]
                data.append(row)
            insert(collection, data)
        cur = list(find(collection))
        count = 0
        for i in range(len(cur)):
            if "분류" in list(cur[i].keys()):
                count = count + 1
        if count == 0:
            collection.update_many({}, {"$set":{"분류":spot}})
        else:
            collection.update_many({"분류": {"$exists": False}}, {"$set":{"분류":spot}})
    except:
        pass


    ##############
    # db에 넣기  #
    ##############

#db = connect_database("trip")
#by_spot = use(db, "by_spot")
#by_region = use(db, "by_region")

# # 관광지별 데이터 저장
# path = r"C:\Users\삼성\Desktop\재성\한이음 챗봇\데이터\관광지별"
# os.chdir(path)
# filelist = os.listdir(path)
# for file in filelist:
#     spot_save(path+"\\"+file, by_spot, file)


# # 지역별 데이터 저장
# path = r"C:\Users\삼성\Desktop\재성\한이음 챗봇\데이터\지역별"
# os.chdir(path)
# filelist = os.listdir(path)
# for file in filelist:
#     spot_save(path+"\\"+file, by_region, file)



##  동반유형에 따른 지역 추천
def recommend_with(df, text):
    res_dict = Res_Verify(text)
    t_type = res_dict['동반 유형']
    df_copy = df.copy()
    header = df_copy.columns.values.tolist()
    dongban_df = df_copy[['동반유형_빈도수','여행유형/트렌드_빈도수','동반유형','동반유형 관련 키워드','여행유형/트렌드','여행유형/트렌드 관련 키워드','지역']].dropna(thresh = 6)
    sub_df = df_copy[['관광지명','주소','분류','지역', '외지인 검색 수']].dropna(thresh=4)
    sub_df = sub_df.loc[sub_df['분류'] != '교통시설']
    sub_df = sub_df.loc[sub_df['분류'] != '쇼핑몰']
    sub_df['외지인 검색 수'] = pd.to_numeric(sub_df['외지인 검색 수'])
    dongban_df['동반유형_빈도수'] = pd.to_numeric(dongban_df['동반유형_빈도수'])
    dongban_df['여행유형/트렌드_빈도수'] = pd.to_numeric(dongban_df['여행유형/트렌드_빈도수'])
    
    new_df = sub_df.sort_values(by='외지인 검색 수' ,ascending=False).reset_index(drop = True).drop_duplicates(['관광지명'])
    t_type_list = list(set(dongban_df['동반유형'].to_list()))
    keyword_list = []
    for t in t_type_list:
        list1 = dongban_df.loc[dongban_df['동반유형']==t]['동반유형 관련 키워드'].to_list()
        list2 = []
        for tag in list1:
            list2.append(tag.split('_'))
        tem_list = []
        tem_list.append(t)
        tem_list = tem_list + list(set(sum(list2,[])))
        keyword_list.append(tem_list)
    temp = []
    for keyword in keyword_list:
        if t_type in keyword:
            target_df = dongban_df.loc[dongban_df['동반유형'] == keyword[0]]
            recommend_df = target_df.sort_values(by='동반유형_빈도수' ,ascending=False).reset_index(drop = True)
    for i in range(20):
        temp.append(sub_df.loc[sub_df["지역"]==list(recommend_df['지역'])[i]].head(3))
    
    answer_df = pd.concat(temp, ignore_index = True)
    
    return answer_df


## 지역에 따른 여행지 추천

def recommend_region(df, text):
    res_dict = Res_Verify(text)
    t_type = [res_dict['도'], res_dict['시/군'], res_dict['구']]
    df_copy = df.copy()
    sub_df = df_copy[['관광지명','주소','분류','지역', '외지인 검색 수']].dropna()
    sub_df = sub_df.loc[sub_df['분류'] != '교통시설']
    sub_df = sub_df.loc[sub_df['분류'] != '쇼핑몰']
    
    if t_type[0] == None and t_type[1] != None:
        region = t_type[1]
    elif t_type[1] == None and t_type[0] != None:
        region = t_type[0]
    elif t_type[0] != None and t_type[1] != None:
        region = t_type[0] + " " + t_type[1]
    
    answer_df = sub_df.loc[sub_df['지역'] == region].reset_index(drop = True)
    return answer_df

## 기간에 따라 여행지 추천
def recommend_day(df, text):
    res_dict = Res_Verify(text)
    t_type = int(res_dict['기간'][0])
    df_copy = df.copy()
    main_df = df_copy[['체류유형','지역']].dropna()
    sub_df = df_copy[['관광지명','주소','분류','지역', '외지인 검색 수']].dropna()
    sub_df = sub_df.loc[sub_df['분류'] != '교통시설']
    sub_df['외지인 검색 수'] = pd.to_numeric(sub_df['외지인 검색 수'])
    if t_type == 1:
        sub_df = sub_df.loc[sub_df['분류'] != '자연경관(하천/해양)']
        sub_df = sub_df.loc[sub_df['분류'] != '호텔']
        sub_df = sub_df.loc[sub_df['분류'] != '콘도미니엄']
        sub_df = sub_df.loc[sub_df['분류'] != '모텔']
        target_df_a = main_df.loc[main_df['체류유형'] == "경유형"]
        target_df_b = main_df.loc[main_df['체류유형'] == "체험형"]
        target_df = pd.concat([target_df_a, target_df_b], ignore_index = True)
    elif t_type > 1:
        sub_df = sub_df.loc[sub_df['분류'] != '쇼핑몰']
        target_df_a = main_df.loc[main_df['체류유형'] == "휴식형"]
        target_df_b = main_df.loc[main_df['체류유형'] == "체류형"]
        target_df = pd.concat([target_df_a, target_df_b], ignore_index = True)
    region_list = list(target_df['지역'])
    temp_list = []
    for region in region_list:
        temp_list.append(sub_df.loc[sub_df['지역'] == region])
    answer_df = pd.concat(temp_list, ignore_index = True).sort_values(by='외지인 검색 수' ,ascending=False).reset_index(drop = True).drop_duplicates(['관광지명'])
    return answer_df

#테마 리스트 작성
#추후 로깅을 통해 추가
th_list = [["바다", "해안", "해변", "해수욕장", "해수욕", "바닷가"], ["캠핑", "글램핑", "캠핑장"], ["스키", "스키장", "보드", "스키 여행"]]
t_n_list = ['바다', '캠핑','스키']
th_dict = dict(zip(t_n_list, th_list))
th_dict['바다']

#테마에 따라 여행지 추천
#다른 함수와 다르게 테마 딕셔너리가 필요
def recommend_th(df, text, th):
    res_dict = Res_Verify(text)
    t_type = res_dict['테마']
    df_copy = df.copy()
    header = df_copy.columns.values.tolist()
    dongban_df = df_copy[['여행유형/트렌드_빈도수','여행유형/트렌드','여행유형/트렌드 관련 키워드','지역']].dropna(thresh=4)
    sub_df = df_copy[['관광지명','주소','분류','지역', '외지인 검색 수']].dropna(thresh=4)
    th_dict = th
    
    attr_list = list(set(df_copy["관광지명"].dropna()))
    ski_list = []
    for attr in attr_list:
        if "스키" in attr:
            if sum(("샵" not in attr, "호텔" not in attr)) == 2:
                ski_list.append(attr)
    sea_list = []
    for attr in attr_list:
        if sum(("해수욕장" in attr, "해변" in attr, "항" in attr, "선착장" in attr, "해안" in attr)) == 1:
            if sum(("장점" not in attr, "변점" not in attr,"항점" not in attr,"영장" not in attr,"호텔" not in attr,"터미널" not in attr,"/" not in attr,"동점" not in attr,"예정" not in attr,
                    "골프" not in attr,"자점" not in attr,"노브랜드" not in attr,"공항" not in attr)) == 13:
                sea_list.append(attr)
    camping_list = []
    for attr in attr_list:
        if "캠핑" in attr:
            camping_list.append(attr)
    camping_list = [t for t in camping_list if "/" not in t and "예정" not in t and "예정" not in t and "리스트" not in t and "11번가" not in t]
    
    df_list = []
    if t_type in th_dict['스키']:
        for ski in ski_list:
            df_list.append(sub_df.loc[df1['관광지명'] == ski])
        df_ = pd.concat(df_list, ignore_index=True)
        df_['외지인 검색 수'] = pd.to_numeric(df_['외지인 검색 수'])
    if t_type in th_dict['바다']:
        for sea in sea_list:
            df_list.append(sub_df.loc[df1['관광지명'] == sea])
        df_ = pd.concat(df_list, ignore_index=True)
        df_['외지인 검색 수'] = pd.to_numeric(df_['외지인 검색 수'])
    if t_type in th_dict['캠핑']:
        for camping in camping_list:
            df_list.append(sub_df.loc[df1['관광지명'] == camping])
        df_ = pd.concat(df_list, ignore_index=True)
        df_['외지인 검색 수'] = pd.to_numeric(df_['외지인 검색 수'])

    return df_.sort_values(by='외지인 검색 수' ,ascending=False).reset_index(drop = True).drop_duplicates(['관광지명'])



# 지역과 기간이 동시에 들어왔을 때의 답변
# (answer, is_good)의 튜플 형태로 답을 돌려줌
# answer는 추천 여행지 df
# is_good은 당일치기를 원하는데 해당 지역이 "휴식형"", "체류형"과 같이 적합하지 않은 경우 bad
# 반대로 당일치기를 원하는데 해당 지역이 "경유형", "체험형" 여행지가 많을 경우 good

def recommend_region_day(df, text):
    df_copy = df.copy()
    res_dict = Res_Verify(text)
    t_type_R = [res_dict['도'], res_dict['시/군'], res_dict['구']]
    t_type_D = int(res_dict['기간'][0])

    main_df = df_copy[['체류유형','지역']].dropna()
    sub_df = df_copy[['관광지명','주소','분류','지역', '외지인 검색 수']].dropna()
    sub_df = sub_df.loc[sub_df['분류'] != '교통시설']
    sub_df['외지인 검색 수'] = pd.to_numeric(sub_df['외지인 검색 수'])
    
    if t_type_D == 1:
        new_df = sub_df.loc[sub_df['분류'] != '모텔']
        new_df = new_df.loc[sub_df['분류'] != '호텔']
        target_df_a = main_df.loc[main_df['체류유형'] == "경유형"]
        target_df_b = main_df.loc[main_df['체류유형'] == "체험형"]
        target_df = pd.concat([target_df_a, target_df_b], ignore_index = True)
    elif t_type_D > 1:
        new_df = sub_df.loc[sub_df['분류'] != '쇼핑몰']
        new_df = new_df.loc[sub_df['분류'] != '시장']
        target_df_a = main_df.loc[main_df['체류유형'] == "휴식형"]
        target_df_b = main_df.loc[main_df['체류유형'] == "체류형"]
        target_df = pd.concat([target_df_a, target_df_b], ignore_index = True)
    region_list = list(target_df['지역'])
    temp_list = []
    for region in region_list:
        temp_list.append(new_df.loc[new_df['지역'] == region])
    day_df = pd.concat(temp_list, ignore_index = True).sort_values(by='외지인 검색 수' ,ascending=False).reset_index(drop = True).drop_duplicates(['관광지명'])
    
    if t_type_R[0] == None and t_type_R[1] != None:
        region = t_type_R[1]
    elif t_type_R[1] == None and t_type_R[0] != None:
        region = t_type_R[0]
    elif t_type_R[0] != None and t_type_R[1] != None:
        region = t_type_R[0] + " " + t_type_R[1]
    
    if sum(day_df['지역'].str.contains(region)) != 0:
        answer = day_df[day_df['지역'].str.contains(region)].reset_index(drop = True)
        is_good = "good"
    else:
        answer = sub_df[sub_df['지역'].str.contains(region)].reset_index(drop = True)
        is_good = "bad"
    
    return answer ,is_good


# 지역 + 동반유형 여행지 추천
def recommend_region_with(df, text):
    df_copy = df.copy()
    sub_df = df_copy[['관광지명','주소','분류','지역', '외지인 검색 수']].dropna()
    sub_df = sub_df.loc[sub_df['분류'] != '교통시설']
    sub_df['외지인 검색 수'] = pd.to_numeric(sub_df['외지인 검색 수'])

    res_dict = Res_Verify(text)
    t_type_W = res_dict['동반 유형']
    t_type_R = [res_dict['도'], res_dict['시/군'], res_dict['구']]
    if t_type_R[0] == None and t_type_R[1] != None:
        region = t_type_R[1]
    elif t_type_R[1] == None and t_type_R[0] != None:
        region = t_type_R[0]
    elif t_type_R[0] != None and t_type_R[1] != None:
        region = t_type_R[0] + " " + t_type_R[1]
    
    answer = sub_df.loc[sub_df['지역'] == region].reset_index(drop = True)
    
    dongban_df = df_copy[['동반유형_빈도수','여행유형/트렌드_빈도수','동반유형','동반유형 관련 키워드','여행유형/트렌드','여행유형/트렌드 관련 키워드','지역']].dropna(thresh = 6)
    dongban_df['동반유형_빈도수'] = pd.to_numeric(dongban_df['동반유형_빈도수'])
    dongban_df['여행유형/트렌드_빈도수'] = pd.to_numeric(dongban_df['여행유형/트렌드_빈도수'])
    region_df = dongban_df.loc[dongban_df['지역'] == region]
    t_type_list = list(set(region_df['동반유형'].to_list()))
    keyword_list = []
    for t in t_type_list:
        list1 = region_df.loc[region_df['동반유형']==t]['동반유형 관련 키워드'].to_list()
        list2 = []
        for tag in list1:
            list2.append(tag.split('_'))
        tem_list = []
        tem_list.append(t)
        tem_list = tem_list + list(set(sum(list2,[])))
        keyword_list.append(tem_list)
    
    for keyword in keyword_list:
        if t_type_W in keyword:
            target_df = dongban_df.loc[dongban_df['동반유형'] == keyword[0]]
            recommend_df = target_df.sort_values(by='동반유형_빈도수' ,ascending=False).reset_index(drop = True)
    return answer, recommend_df