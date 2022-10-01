from mimetypes import init
from database import *
from mmethods import _result, parse_json, load_json
from mconsts import *
from flask import Flask, request, redirect, jsonify


connect_to = '127.0.0.1'
dataset = []


app = Flask(__name__)
db = connect_database("skbs")
collection = use(db, "post")


def init_dataset_list():
    global dataset
    try:
        dataset = list(find(collection, {}))
        status = STATUS_SUCCESS
    except e:
        status = STATUS_FAIL
    finally:
        print(f"init_dataset/result: {status}")
        return _result(status, dataset)

# 게시글 개수 리턴
@app.route('/noticeboard-length', methods=['GET'])
def get_length():
    if len(dataset) == 0: init_dataset_list()
    try:
        return _result(STATUS_SUCCESS, len(dataset))
    except:
        return _result(STATUS_FAIL, 0)

# 게시판 데이터 불러오기
@app.route('/noticeboard-dataset', methods=['GET'])
def get_dataset():
    if len(dataset) == 0: init_dataset_list()
    return _result(STATUS_SUCCESS, parse_json(dataset))

# 글 쓰기
@app.route('/noticeboard-document', methods=['POST'])
def write(title, content, image_list):

    return _result()

# 글 읽기
@app.route('/noticeboard-document/<int:num>', methods=['GET'])
def write(num):

    return _result()

# App Start
if __name__=="__main__":
    app.secret_key = '여행 de Gaja'
    # app.config['SESSION_TYPE'] = 'filesystem'
    app.run(host=connect_to, port=PORT_NOTICEBOARD, debug=True)