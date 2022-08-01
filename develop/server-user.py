from database import *
from mmethods import _result, parse_json, load_json
from mconsts import *
from flask import Flask, request, redirect, jsonify

app = Flask(__name__)
db = connect_database("skbs")
collection = use(db, "user")

# 유저 찾기
@app.route('/find_user', methods=['GET'])
def find_user():
    parameter_dict = request.args.to_dict()
    result = dict()
    status = STATUS_FAIL
    try:
        user_id = parameter_dict['user_id']
        print(f"find_user/user_id: {user_id}")
        option = {
            "user_id": user_id
        }
        result['data'] = parse_json(list(find(collection, option)))
        result['count'] = len(list(find(collection, option)))
        status = STATUS_SUCCESS
    except e:
        result['data'] = e
        result['count'] = 0
    finally:
        print(f"find_user/result: {result}")
        return _result(status, result)

@app.route('/add-user', methods=['POST'])
def addUser():
    """
        needs
            nick
            id
            pw
    """

    params = load_json(request.get_data())

    user_nick = params['user_nick']
    user_id = params['user_id']
    user_pw = params['user_pw']

    try:
        insert(collection=collection, data_list=[{
            "user_nick": user_nick,
            "user_id": user_id,
            "user_pw": user_pw,
            "user_thumbnail": "temp.jpg"
        }])
    except:
        return _result(0, "오류가 발생하였습니다.")

    return _result(1, "회원가입이 정상적으로 처리되었습니다.")

@app.route('/delete-user', methods=['POST'])
def delUser():
    if True:
        return {
            "content": "미구현" 
        }

    return {
        "content": "유저 탈퇴가 정상적으로 처리되었습니다."
    }

@app.route('/show-user-list', methods=['GET'])
def showUserList():
    res = list(find(collection, {}))
    return _result(1, parse_json(res))

# App Start
if __name__=="__main__":
    app.secret_key = '여행 de Gaja'
    # app.config['SESSION_TYPE'] = 'filesystem'
    app.run(host="127.0.0.1", port="5001", debug=True)