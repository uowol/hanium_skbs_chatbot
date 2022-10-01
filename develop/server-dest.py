import re
from lib_database import *
from lib_dialogflow_response import *
from global_methods import _result, parse_json, load_json
from global_consts import *
from flask import Flask, request, redirect, jsonify, session
import pandas as pd

# 세션 다루는 파트, 나중에 업데이트 할 때 유용하게 사용할 것으로 보임.
from flask_cors import CORS, cross_origin
# from flask_session import Session


connect_to = '127.0.0.1'


app = Flask(__name__)
app.secret_key = '여행 de Gaja'
CORS(app)
# Session(app)


db                  = connect_database("skbs")
col_region_test     = use(db, "region_test")


# 지역 리스트 가져오기
@app.route('/region', methods=["GET"])
def get_region_list():
    df = pd.read_csv('../data_process/output/region_dict.csv', encoding='CP949')
    answer = df.to_dict()
    return _result(STATUS_SUCCESS, answer);

@app.route('/dest', methods=["GET"])
def get_dest_list():
    df = pd.read_csv('../data_process/output/dest_dict.csv', encoding='CP949')
    answer = df.to_dict()
    return _result(STATUS_SUCCESS, answer);

# App Start
if __name__=="__main__":
    # app.config['SESSION_TYPE'] = 'filesystem'
    app.run(host=connect_to, port=PORT_DEST, debug=True)