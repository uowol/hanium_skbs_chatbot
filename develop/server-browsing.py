from flask import Flask, render_template, request, Markup, redirect, flash, session, jsonify
from flask_login import LoginManager, login_user, logout_user, UserMixin, login_required, current_user
from requests import get, post 
from mmethods import _result, parse_json, load_json
from mconsts import *

# Flask 객체 인스턴스 생성
app = Flask(__name__)
lm = LoginManager()
lm.init_app(app)

params = {
    "site_name": "GAZA-GO",
    "session": session,
    "current_user": current_user
}

@app.route('/init', methods=['GET'])
def init_chat_list():
    session['chat_list'] = ''
    return redirect('/')


@app.route('/', methods=['GET'])
def index():
    # 다른 모든 route에 추가해야 할 것으로 예상
    if not 'chat_list' in session:
        return redirect('/init')
    return render_template('main_layout.html', params=params, chatbot_talk="메인 페이지입니다.", content="contents/main.html")

#%% Login

# 사용자 정보를 조회
@lm.user_loader
def user_loader(user_id):
    user_info = User.get_user_info(user_id)
    login_info = User(user_id=user_info['user_id'])
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
        global params
        print(f"get_user_info/user_id: {user_id}")
        user_info = None
        try:
            res = get(f"http://127.0.0.1:5001/user?user_id={user_id}")
            if res.status_code == 200:  # 서버와 통신
                res = res.json()['body']
                if res['count'] == 1:   # 유저 정보가 존재
                    user_info = load_json(res['data'])[0]                
        except:
            print(f"error: get_user_info()")
        print(f"get_user_info/user_info: {user_info}")
        return user_info

@app.route('/login', methods=['GET'])
def login():
    return render_template('main_layout.html', params=params, chatbot_talk="로그인 페이지입니다.", content="login.html")

@app.route('/login', methods=["POST"])
def loginCallback():
    global params

    user_id = request.form.get('inputEmail')
    user_pw = request.form.get('inputPassword')

    # 사용자가 입력한 정보가 회원가입된 사용자인지 확인
    user_info = User.get_user_info(user_id)
    
    if user_info:
        if user_info['user_pw'] != user_pw: return redirect('/login/error')
        login_info = User(user_id=user_info['user_id']) # 사용자 객체 생성
        login_user(login_info)                          # 사용자 객체를 session에 저장
        session['user_id'] = user_id
        session['user_nick'] = user_info['user_nick']

        return redirect('/')
    else:
        return redirect('/login/error')

@app.route('/logout', methods=["GET"])
def logout():
    logout_user()
    session['user_id'] = None
    session['user_nick'] = None
    return redirect('/')

@app.route('/login/error')
def login_error():
    return render_template('main_layout.html', params=params, chatbot_talk="", content="login.html", retry=True)

@app.route('/register', methods=['GET'])
def register():
    return render_template('main_layout.html', params=params, chatbot_talk="회원가입 페이지입니다.", content="register.html")

@app.route('/register/error')
def register_error():
    return render_template('main_layout.html', params=params, chatbot_talk="", content="register.html", retry=True)

@app.route('/register', methods=["POST"])
def register_callback():
    user_id = request.form.get('inputEmail')
    user_nick = request.form.get('inputNick')
    user_pw = request.form.get('inputPassword')
    user_rp = request.form.get('repeatPassword')

    print(f"register_callback/user_id: {user_id}")
    if user_pw != user_rp:
        return redirect('/register/error')

    user_info = User.get_user_info(user_id)
    if user_info:
        return redirect('/register/error')

    params = {
        "user_id": user_id,
        "user_nick": user_nick,
        "user_pw": user_pw,
    }
    res = post("http://127.0.0.1:5001/user", data=parse_json(params))
    if res.status_code == 200:
        print(f"register_callback/res: {res.json()}")
        if res.json()['status'] == STATUS_FAIL: return redirect('/register/error')
        return redirect('/login')
    else:
        return redirect('/register/error')

@app.route('/forgot-password', methods=['GET'])
def forgot_password():
    return render_template('main_layout.html', params=params, chatbot_talk="비밀번호를 잊어버리셨나요?", content="forgot-password.html", user_info = -1)

@app.route('/forgot-password/find-user', methods=['GET', 'POST'])
def forgot_password_find_user():
    user_id = request.form.get('inputEmail')
    print(f"forgot_password_find_user/user_id: {user_id}")

    # 사용자가 입력한 정보가 회원가입된 사용자인지 확인
    user_info = User.get_user_info(user_id)
    if user_info:
        print(f"forgot_password_find_user/user_pw: {user_info['user_pw']}")

    return render_template(
        'main_layout.html',
        content='forgot-password.html', 
        params=params, chatbot_talk="",
        user_info = user_info
    )

#%% Dashboard    
# @app.route('/dashboard', methods=['GET'])
# def dashboard():
#     return render_template('main_layout.html', params=params, chatbot_talk="", content="contents/dashboard.html")

#%% Chart
# @app.route('/charts', methods=['GET'])
# def charts():
#     return render_template('main_layout.html', params=params, chatbot_talk="", content="contents/charts.html")

#%% Concept
@app.route('/concept', methods=['GET'])
def concept():
    return render_template('main_layout.html', params=params, chatbot_talk="", content="contents/concept.html")
    
#%% Noticeboard
@app.route('/noticeboard', methods=['GET'])
def noticeboard():
    return redirect("/noticeboard/free")

# 게시판 서버로 보낼 것
@app.route('/noticeboard/write', methods=['GET'])
def noticeboard_write():
    return render_template('main_layout.html', params=params, chatbot_talk="", content="contents/noticeboard_write.html",
        tag="free")

@app.route('/noticeboard/write', methods=['POST'])
def noticeboard_callback():

    # 글 쓰기: 게시판 서버와 통신

    return render_template('main_layout.html', params=params, chatbot_talk="", content="contents/noticeboard_write.html",
        table_contents=[], tag="free")

# 게시판 서버로 보낼 것
@app.route('/noticeboard/free', methods=['GET'])
def noticeboard_free():

    # 게시판 서버로부터 데이터 받아오기

    return render_template('main_layout.html', params=params, chatbot_talk="", content="contents/noticeboard.html",
        table_contents=[], tag="free")
        
# 게시판 서버로 보낼 것
@app.route('/noticeboard/free/<int:i>', methods=['GET'])
def noticeboard_free_content(i):

    # 게시판 서버로부터 데이터 받아오기
    
    return render_template('main_layout.html', params=params, chatbot_talk="", content="contents/noticeboard_content.html",
        title=str(i)+"번째 게시물", noticeboard_content=str(i)+"번째 본문")

# 게시판 서버로 보낼 것
# @app.route('/noticeboard/review', methods=['GET'])
# def noticeboard_review():
#     return render_template('main_layout.html', params=params, chatbot_talk="", content="contents/noticeboard.html",
#         table_contents=[], tag="review")

# # 게시판 서버로 보낼 것
# @app.route('/noticeboard/tip', methods=['GET'])
# def noticeboard_tip():
#     return render_template('main_layout.html', params=params, chatbot_talk="", content="contents/noticeboard.html",
#         table_contents=[], tag="tip")

#%% Region
@app.route('/region', methods=['GET'])
def region():
    return render_template('main_layout.html', params=params, chatbot_talk="", content="contents/region.html")
    
#%% Search
@app.route('/search', methods=['GET'])
def search():
    return render_template('main_layout.html', params=params, chatbot_talk="", content="contents/search.html")
    
# # @app.route('/votes', methods=['GET'])
# # def votes():
# #     return render_template('main_layout.html', params=params, chatbot_talk="", content="contents/votes.html")

#%% Chatbot
# date_time = "23 Jan 2:05 pm"
# name_bot = "bot"
# name_user = "bot"
# def chat_question(text):
#     try:
#         if session['user_nick'] != '':
#             name = session['user_nick']
#         else:
#             name = "anonymous"
#     except:
#         name = "anonymous"

#     return f"""<div class="d-flex justify-content-between">
#                     <p class="small mb-1 text-muted">{date_time}</p>
#                     <p class="small mb-1">{name}</p>
#                 </div>
#                 <div class="d-flex flex-row justify-content-end mb-4 pt-1">
#                     <div>
#                         <p class="small p-2 me-3 mb-3 text-white rounded-3 bg-warning">{text}</p>
#                     </div>
#                     <img src="https://mdbcdn.b-cdn.net/img/Photos/new-templates/bootstrap-chat/ava6-bg.webp"
#                         alt="avatar 1" style="width: 45px; height: 100%;">
#                 </div>"""

# def chat_answer(text):
#     return f"""<div class="d-flex justify-content-between">
#                     <p class="small mb-1">{name_bot}</p>
#                     <p class="small mb-1 text-muted">{date_time}</p>
#                 </div>
#                 <div class="d-flex flex-row justify-content-start">
#                     <img src="https://mdbcdn.b-cdn.net/img/Photos/new-templates/bootstrap-chat/ava5-bg.webp"
#                         alt="avatar 1" style="width: 45px; height: 100%;">
#                     <div>
#                         <p class="small p-2 ms-3 mb-3 rounded-3" style="background-color: #f5f6f7;">{text}</p>
#                     </div>
#                 </div>"""

# @app.route('/chatbot', methods=['GET'])
# def chatbot():
#     return render_template('main_layout.html', params=params, chatbot_talk="", content="chatbot.html")
    
@app.route('/chatbot', methods=['POST'])
def chatbot_callback():
    # chatbot session 에 채팅 상황 저장
    session['chat_list'] = request.json['chat_list']
    print(f"chatbot_callback/chat_list: updated")

    last_chat = request.json['last_chat']
    print(f"chatbot_callback/last_chat: {last_chat}")    

    return _result(STATUS_SUCCESS, '')
    
@app.route('/chatbot', methods=['DELETE'])
def chatbot_delete():
    # chatbot 채팅 상황 제거
    session.pop('chat_list')
    print(f"chatbot_delete/chat_list: deleted")
    return _result(STATUS_SUCCESS, '')
    
#%% App Start
if __name__=="__main__":
    # oauth()    # 사용자 정보 인증
    # app.run(debug=True)
    app.secret_key = '여행 de Gaja'
    # app.config['SESSION_TYPE'] = 'filesystem'
    app.run(host="127.0.0.1", port=PORT_BROWSING, debug=True)