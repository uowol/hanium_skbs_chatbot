import re
from lib_database import *
from lib_dialogflow_response import *
from global_methods import _result, parse_json, load_json
from global_consts import *
from flask import Flask, request, redirect, jsonify, session
import pandas as pd

from flask_cors import CORS, cross_origin
# from flask_session import Session


connect_to = '127.0.0.1'


app = Flask(__name__)
app.secret_key = '여행 de Gaja'
CORS(app)
# Session(app)


db                  = connect_database("skbs")
col_region_test     = use(db, "region_test")


##### 업데이트 할 내용
# 지금은 csv로 가져오지만 db로 저장해서 사용하는게 통일성있긴 함.


# 지역 dictionary 가져오기
# 도
# ㄴ 시/군/구
@app.route('/region', methods=["GET"])
def get_region_list():
    df = pd.read_csv('../data_process/output/region_dict.csv')
    answer = df.to_dict()
    return _result(STATUS_SUCCESS, answer);

# 테마 list 가져오기
# [계곡, 바다, ...]
@app.route('/theme', methods=["GET"])
def get_theme_list():
    df = pd.read_csv('../data_process/output/theme.csv')
    answer = df.to_dict()
    return _result(STATUS_SUCCESS, answer);

# 전체 관광지 데이터셋 가져오기
# + theme
# * 지역은 기존에 '지역' 변수에 포함
@app.route('/dest', methods=["GET"])
def get_dest_list():
    df = pd.read_csv('../data_process/output/data_theme_plus.csv')
    answer = df.to_dict()
    return _result(STATUS_SUCCESS, answer);

# 지역별 관광지 dictionary 가져오기
# 지역명(도/시/군/구)
# ㄴ 관광지명
@app.route('/region/dest', methods=["GET"])
def get_region_dest_list():
    df = pd.read_csv('../data_process/output/dest_dict.csv')
    answer = df.to_dict()
    return _result(STATUS_SUCCESS, answer);
    
# 테마별 관광지 dictionary 가져오기
# 테마
# ㄴ 관광지명
@app.route('/theme/dest', methods=["GET"])
def get_theme_dest_list():
    df = pd.read_csv('../data_process/output/data_theme_plus.csv')
    theme = pd.read_csv('../data_process/output/theme.csv').title
    answer = dict()
    for t in theme:
        answer[t] = df.관광지명[df.theme.apply(lambda x: t in x)].to_list()
    return _result(STATUS_SUCCESS, answer);


# App Start
if __name__=="__main__":
    # app.config['SESSION_TYPE'] = 'filesystem'
    app.run(host=connect_to, port=PORT_DEST, debug=True)