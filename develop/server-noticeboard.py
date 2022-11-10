#%%
from mimetypes import init
from lib_database import *
from global_methods import _result, parse_json, load_json
from global_consts import *
from flask import Flask, request, redirect, jsonify

connect_to = '127.0.0.1'
dataset = []

app = Flask(__name__)
db = connect_database("skbs")
db_posts = use(db, "posts")
#%%

# 게시글 업데이트
@app.route("/noticeboard/init", methods=["GET"])
def update_dataset_list():
    global dataset
    try:
        dataset = list(find(db_posts, {}))
        dataset.reverse()
        status = STATUS_SUCCESS
    except e:
        status = STATUS_FAIL
    finally:
        print(f"init_dataset/result: {status}")
        return _result(status, parse_json(dataset))


# 게시글 개수 리턴
@app.route("/noticeboard/length", methods=["GET"])
def get_length():
    if len(dataset) == 0:
        update_dataset_list()
    try:
        return _result(STATUS_SUCCESS, len(dataset))
    except:
        return _result(STATUS_FAIL, 0)


# 게시판 데이터 불러오기
@app.route("/noticeboard/raw", methods=["GET"])
def get_dataset():
    if len(dataset) == 0:
        update_dataset_list()
    return _result(STATUS_SUCCESS, parse_json(dataset))


@app.route("/noticeboard/free", methods=["POST"])
def write():
    global max_index
    params = load_json(request.get_data())
    print(params, max_index)
    title = params['title']
    content = params['content']
    image_list = params['image_list']
    try:
        insert(
            collection=db_posts,
            data_list=[
                {
                    "_id": max_index+1,
                    "post_user_nick": "김수한무",
                    "post_title": title,
                    "post_text": content,
                    "post_image": image_list,
                    "post_recommend": 0,
                    "post_view": 0,
                    "post_time": 0,
                    "post_comment": 0,
                }
            ],
        )
        max_index = max_index+1
    except Exception as e:
        print("!!!", e)
        return _result(STATUS_FAIL, {})
    print(params, max_index)
    return _result(STATUS_SUCCESS, {})


@app.route("/noticeboard/free/<int:num>", methods=["GET"])
def read(num):
    post = list(find(db_posts, {"_id":num}))[0]
    update(db_posts, {"_id":num}, {"$set": {"post_view":post['post_view']+1}})
    return _result(STATUS_SUCCESS, parse_json(post))


@app.route("/noticeboard/free", methods=["GET"])
def get_list_free():
    update_dataset_list()
    return _result(STATUS_SUCCESS, parse_json(dataset))


# App Start
if __name__ == "__main__":
    global max_index
    update_dataset_list()
    max_index = len(dataset)

    app.secret_key = "여행 de Gaja"
    # app.config['SESSION_TYPE'] = 'filesystem'
    app.run(host=connect_to, port=PORT_NOTICEBOARD, debug=True)