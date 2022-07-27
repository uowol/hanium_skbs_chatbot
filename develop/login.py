import collections
from flask import Flask, request, redirect
from flask_login import LoginManager, login_user, logout_user, UserMixin, login_required, current_user
from database import *
import json

db = connect_database("skbs")
collection = use(db, collection="user")

# Flask 객체 인스턴스 생성
app = Flask(__name__)

# Flask Login Manager
lm = LoginManager()
lm.session_protection = "strong"
lm.init_app(app)

USER = None

@app.route('/islogin', methods=['GET'])
def islogin():
    parameter_dict = request.args.to_dict()
    if len(parameter_dict) == 0:
        return {
            "content": False
        }
    user_id = parameter_dict["user_id"]
    print(f"user_id: {user_id}")
    current_user = find_user(user_id=user_id)
    if not current_user:
        return {
            "content": False
        }
    print(f"islogin: {current_user.is_authenticated}")
    return {
        "content": current_user.is_authenticated
    }

@app.route('/add-user', methods=['POST'])
def addUser():
    """
        needs
            nick
            id
            pw
    """

    params = json.loads(request.get_data())

    user_nick = params['user_nick']
    user_id = params['user_id']
    user_pw = params['user_pw']

    user_info = User.get_user_info(user_id)
    if user_info['count'] != 0:
        return {
            "result": False,
            "content": "중복된 아이디입니다." 
        }

    try:
        insert(collection=collection, data_list=[{
            "user_nick": user_nick,
            "user_id": user_id,
            "user_pw": user_pw,
            "user_thumbnail": "temp.jpg"
        }])
    except:
        return {
            "result": False,
            "content": "오류가 발생하였습니다." 
        }

    return {
        "result": True,
        "content": "회원가입이 정상적으로 처리되었습니다."
    }

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
    print(res)
    return {
        "content": dumps(res),
    }

@app.route('/login-handler', methods=['POST'])
def login():
    # global USER

    params = json.loads(request.get_data())
    # print(params)
    user_id = params["user_id"]
    user_pw = params["user_pw"]

    if user_id is None or user_pw is None:
        return {
            "result": False,
            "content": "다시 입력해주세요."
        }

    # 사용자가 입력한 정보가 회원가입된 사용자인지 확인
    user_info = User.get_user_info(user_id)
    # print(user_info)

    if user_info['result'] != 'fail' and user_info['count'] != 0:
        login_info = User(user_id=user_info['data'][0]['user_id'])  # 사용자 객체 생성
        # !!! - not working
        login_user(login_info)                                      # 사용자 객체를 session에 저장
        # print(f"islogin: {login_info.is_authenticated}")
        # print(f"user: {user_info['data']}")
        # USER = login_info
        return {
            "result": True,
            "content": {
                "id": user_info['data'][0]['user_id'],
                "nick": user_info['data'][0]['user_nick']
            }
        }

    else:
        return {
            "result": False,
            "content": "아이디와 비밀번호를 다시 확인해주세요."
        }


@app.route('/logout-handler', methods=['GET'])
def logout():
    parameter_dict = request.args.to_dict()
    if len(parameter_dict) == 0:
        return {
            "content": False
        }
    user_id = parameter_dict["user_id"]
    print(f"logout_user_id: {user_id}")
    user = find_user(user_id=user_id)
    if not user:
        return {
            "content": False
        }
    login_user(user)
    logout_user()
    print(f"logout_user_id: {current_user.is_authenticated}")
    return {
        "content": "로그아웃이 정상적으로 처리되었습니다."
    }

@app.route('/forgot-password/find_user', methods=['GET', 'POST'])
def forgot_password_find_user():
    user_id = request.form.get('inputEmail')

    # 사용자가 입력한 정보가 회원가입된 사용자인지 확인
    user_info = User.get_user_info(user_id)

    return render_template(
        'main_layout.html',
        site_name=SITE_NAME, 
        content='forgot-password.html', 
        user_info = user_info
    )

def find_user(user_id):
    user_info = User.get_user_info(user_id)

    if user_info['result'] != 'fail' and user_info['count'] != 0:
        login_info = User(user_id=user_info['data'][0]['user_id'])  # 사용자 객체 생성
        return login_info

    return None

# 사용자 정보를 조회
@lm.user_loader
def user_loader(user_id):
    """
    skbs(db)
    ㄴuser(collection)
      ㄴuser_id
        user_pw
        user_thumbnail
        user_nick
    """
    user_info = User.get_user_info(user_id)
    login_info = User(user_id=user_info['data'][0]['user_id'])

    return login_info

# 로그인되어 있지 않은 경우
@lm.unauthorized_handler
def unauthorized():
    return redirect("/")

# Login User 객체
class User(UserMixin):
    def __init__(self, user_id):
        self.user_id = user_id
    
    def get_id(self):
        return str(self.user_id)
    
    @staticmethod
    def get_user_info(user_id):
        result = dict()
        try:
            option = {
                "user_id": user_id
            }
            result['result'] = "success"
            result['data'] = list(find(collection, option))
            result['count'] = len(result['data'])
        except e:
            result['result'] = 'fail'
            result['data'] = e
        finally:
            return result

            
# App Start
if __name__=="__main__":
    app.secret_key = '여행 de Gaja'
    # app.config['SESSION_TYPE'] = 'filesystem'
    app.run(host="127.0.0.1", port="5001", debug=True)