from lib_database import *

import os
import csv
import pandas as pd

# 관광데이터 포털에서 가져온 지역별 모든 데이터를 몽고db에 저장
# 지역데이터 전체 다운로드 눌렀을 때 받아지는 파일
# db에 저장하는 함수
def test1(path, collection):
    db = connect_database("trip")
    col_name = use(db, collection)
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
        insert(col_name, data)

# 사용 예시
# test1(r"저장된 path", "원하는 컬렉션")
# 몽고db 열어보면 저장된 것 확인 가능



# 몽고 db에 구분 없이 저장된 지역별 모든 데이터를
# csv 파일 별로 리스트에 저장하는 함수
# 추후 데이터를 합칠 때 대비해 지역 입력하면 추가되도록 함
def test2(collection, region):
    db = connect_database("trip")
    col_name = use(db, collection)
    cur = find(col_name)
    data_list = []
    key_names = []
    temp = []
    merged_data = []
    for doc in cur:
        doc.update(지역 = region)
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
def test3(data):
    df_list = []
    for i in range(len(data)):
        df_list.append(pd.DataFrame(data[i]))
    return df_list