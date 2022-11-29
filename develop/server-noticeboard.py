#%%
from mimetypes import init
from lib_database import *
from requests import get, post 
from global_methods import _result, parse_json, load_json
from global_consts import *
from flask_cors import CORS
from flask import Flask, request, redirect, jsonify
import datetime as dt
import sys


if len(sys.argv) > 1:
    is_test = sys.argv[1]
else:
    is_test = False

connect_to = "127.0.0.1" if is_test else "ec2-54-65-184-107.ap-northeast-1.compute.amazonaws.com"


global_dataset = []

app = Flask(__name__)
CORS(app)
db = connect_database("skbs")
db_posts = use(db, "posts")
#%%

# 게시글 업데이트
@app.route("/noticeboard/init", methods=["GET"])
def update_dataset_list():
    global global_dataset
    try:
        global_dataset = list(find(db_posts, {}))
        global_dataset.reverse()
        status = STATUS_SUCCESS
    except e:
        status = STATUS_FAIL
    finally:
        print(f"init_dataset/result: {status}")
        return _result(status, parse_json(global_dataset))


# 게시글 개수 리턴
@app.route("/noticeboard/length", methods=["GET"])
def get_length():
    if len(global_dataset) == 0:
        update_dataset_list()
    try:
        return _result(STATUS_SUCCESS, len(global_dataset))
    except:
        return _result(STATUS_FAIL, 0)


# 게시판 데이터 불러오기
@app.route("/noticeboard/raw", methods=["GET"])
def get_dataset():
    if len(global_dataset) == 0:
        update_dataset_list()
    return _result(STATUS_SUCCESS, parse_json(global_dataset))


@app.route("/noticeboard/free", methods=["POST"])
def write_free():
    global max_index
    params = load_json(request.get_data())
    print(params)
    title = params['title']
    content = params['content']
    image_list = params['image_list']
    user_nick = params['user_nick']
    try:
        insert(
            collection=db_posts,
            data_list=[
                {
                    "_id": max_index+1,
                    "post_user_nick": user_nick,
                    "post_title": title,
                    "post_text": content,
                    "post_image": image_list,
                    "post_recommend": 0,
                    "post_view": 0,
                    "post_time": dt.datetime.now().strftime("%Y/%m/%d"),
                    "post_comment": 0,
                    "type":"free"
                }
            ],
        )
        max_index = max_index+1
    except Exception as e:
        return _result(STATUS_FAIL, {})
    return _result(STATUS_SUCCESS, {})


@app.route("/noticeboard/free/<int:num>", methods=["GET"])
def read_free(num):
    post = list(find(db_posts, {"_id":num}))[0]
    update(db_posts, {"_id":num}, {"$set": {"post_view":post['post_view']+1}})
    return _result(STATUS_SUCCESS, parse_json(post))

@app.route("/noticeboard/free/<int:num>/recommend", methods=["POST"])
def recommend_free(num):
    post = list(find(db_posts, {"_id":num}))[0]
    # try:
    #     res = get(f"http://{connect_to}:{PORT_USER}/user?user_id")
    #     if res.status_code == 200:  # 서버와 통신
    #         user_data = res.json()['body']
    #         # print(user_data)
    # except Exception as e: 
    #     print(e)
    # if user_data != {}:
    #     update(db_posts, {"_id":num}, {"$set": {"post_recommend":post['post_recommend']+1}})
    #     return _result(STATUS_SUCCESS, {})
    # else: 
    #     return _result(STATUS_FAIL, {})
    update(db_posts, {"_id":num}, {"$set": {"post_recommend":post['post_recommend']+1}})
    return _result(STATUS_SUCCESS, {})
    
@app.route("/noticeboard/free", methods=["GET"])
def get_list_free():
    dataset = list(find(db_posts, {"type":"free"}))
    dataset.reverse()
    # update_dataset_list()
    return _result(STATUS_SUCCESS, parse_json(dataset))


@app.route("/noticeboard/review", methods=["POST"])
def write_review():
    global max_index
    params = load_json(request.get_data())
    title = params['title']
    content = params['content']
    image_list = params['image_list']
    user_nick = params['user_nick'] if params['user_nick'] else "익명"
    try:
        insert(
            collection=db_posts,
            data_list=[
                {
                    "_id": max_index+1,
                    "post_user_nick": user_nick,
                    "post_title": title,
                    "post_text": content,
                    "post_image": image_list,
                    "post_recommend": 0,
                    "post_view": 0,
                    "post_time": dt.datetime.now().strftime("%Y/%m/%d"),
                    "post_comment": 0,
                    "type": "review"
                }
            ],
        )
        max_index = max_index+1
    except Exception as e:
        return _result(STATUS_FAIL, {})
    return _result(STATUS_SUCCESS, {})


@app.route("/noticeboard/review/<int:num>", methods=["GET"])
def read_review(num):
    post = list(find(db_posts, {"_id":num}))[0]
    update(db_posts, {"_id":num}, {"$set": {"post_view":post['post_view']+1}})
    return _result(STATUS_SUCCESS, parse_json(post))

@app.route("/noticeboard/review/<int:num>/recommend", methods=["POST"])
def recommend_review(num):
    post = list(find(db_posts, {"_id":num}))[0]
    update(db_posts, {"_id":num}, {"$set": {"post_recommend":post['post_recommend']+1}})
    return _result(STATUS_SUCCESS, {})
    
@app.route("/noticeboard/review", methods=["GET"])
def get_list_review():
    dataset = list(find(db_posts, {"type":"review"}))
    dataset.reverse()
    # update_dataset_list()
    return _result(STATUS_SUCCESS, parse_json(dataset))


@app.route("/noticeboard/tip", methods=["POST"])
def write_tip():
    global max_index
    params = load_json(request.get_data())
    title = params['title']
    content = params['content']
    image_list = params['image_list']
    user_nick = params['user_nick'] if params['user_nick'] else "익명"
    try:
        insert(
            collection=db_posts,
            data_list=[
                {
                    "_id": max_index+1,
                    "post_user_nick": user_nick,
                    "post_title": title,
                    "post_text": content,
                    "post_image": image_list,
                    "post_recommend": 0,
                    "post_view": 0,
                    "post_time": dt.datetime.now().strftime("%Y/%m/%d"),
                    "post_comment": 0,
                    "type": "tip"
                }
            ],
        )
        max_index = max_index+1
    except Exception as e:
        return _result(STATUS_FAIL, {})
    return _result(STATUS_SUCCESS, {})


@app.route("/noticeboard/tip/<int:num>", methods=["GET"])
def read_tip(num):
    post = list(find(db_posts, {"_id":num}))[0]
    update(db_posts, {"_id":num}, {"$set": {"post_view":post['post_view']+1}})
    return _result(STATUS_SUCCESS, parse_json(post))

@app.route("/noticeboard/tip/<int:num>/recommend", methods=["POST"])
def recommend_tip(num):
    post = list(find(db_posts, {"_id":num}))[0]
    update(db_posts, {"_id":num}, {"$set": {"post_recommend":post['post_recommend']+1}})
    return _result(STATUS_SUCCESS, {})
    
@app.route("/noticeboard/tip", methods=["GET"])
def get_list_tip():
    dataset = list(find(db_posts, {"type":"tip"}))
    dataset.reverse()
    # update_dataset_list()
    return _result(STATUS_SUCCESS, parse_json(dataset))

# App Start
if __name__ == "__main__":
    global max_index
    update_dataset_list()
    max_index = len(global_dataset)

    app.secret_key = "여행 de Gaja"
    # app.config['SESSION_TYPE'] = 'filesystem'
    app.run(host=connect_to, port=PORT_NOTICEBOARD, debug=True)