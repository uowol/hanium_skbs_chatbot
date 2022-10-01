import os
import csv
import pandas as pd
import pymongo

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

db = connect_database("trip")
by_spot = use(db, "by_spot")
by_region = use(db, "by_region")

# 관광지별 데이터 저장
path = r"C:\Users\삼성\Desktop\재성\한이음 챗봇\데이터\관광지별"
os.chdir(path)
filelist = os.listdir(path)
for file in filelist:
    spot_save(path+"\\"+file, by_spot, file)


# 지역별 데이터 저장
path = r"C:\Users\삼성\Desktop\재성\한이음 챗봇\데이터\지역별"
os.chdir(path)
filelist = os.listdir(path)
for file in filelist:
    spot_save(path+"\\"+file, by_region, file)