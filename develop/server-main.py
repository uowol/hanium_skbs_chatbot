from flask import Flask, render_template, request, Markup, redirect, flash, session, jsonify
from flask_login import (
    LoginManager,
    login_user,
    logout_user,
    UserMixin,
    login_required,
    current_user,
)
from requests import get, post
from flask_cors import CORS
from global_methods import _result, parse_json, load_json
from global_consts import *


connect_to = "127.0.0.1"
params = {"site_name": "Tour-List", "session": session, "current_user": current_user}


# Flask 객체 인스턴스 생성
app = Flask(__name__)
CORS(app)
lm = LoginManager()
lm.init_app(app)


@app.route("/init", methods=["GET"])
def init_chat_list():
    session["chat_list"] = ""
    return redirect("/")


@app.route("/", methods=["GET"])
def index():
    # 다른 모든 route에 추가해야 할 것으로 예상
    if not "chat_list" in session:
        return redirect("/init")
    return render_template(
        "main_layout.html", params=params, chatbot_talk="메인 페이지입니다.", content="contents/main.html"
    )


#%% Detail
@app.route("/detail", methods=["GET"])
def detail():
    req = request.args.to_dict()
    dest = None

    if "dest" in req:
        dest = req["dest"]

    print(f"detail/dest: {dest}")

    # 대충 여행지 DB 상호작용하는 서버에게 요청보내고 받은 여행지 데이터를 활용하여 관련 정보 시각화하기

    # params = {
    #     "dest": dest
    # }

    # res = post("http://0.0.0.0:5004/dests", data=parse_json(params))

    # if res.status_code == 200:
    #     print(f"register_callback/res: {res.json()}")
    #     if res.json()['status'] == STATUS_FAIL: return redirect('/register/error')
    #     return redirect('/login')
    # else:
    #     return redirect('/register/error')

    return render_template(
        "main_layout.html",
        params=params,
        chatbot_talk="여행지 세부 정보 페이지입니다.",
        content="contents/detail.html",
    )


#%% Login
# 사용자 정보를 조회
@lm.user_loader
def user_loader(user_id):
    user_info = User.get_user_info(user_id)
    login_info = User(user_id=user_info["user_id"])
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
            res = get(f"http://{connect_to}:5001/user?user_id={user_id}")
            if res.status_code == 200:  # 서버와 통신
                res = res.json()["body"]
                if res["count"] == 1:  # 유저 정보가 존재
                    user_info = load_json(res["data"])[0]
        except:
            print(f"error: get_user_info()")
        print(f"get_user_info/user_info: {user_info}")
        return user_info


@app.route("/login", methods=["GET"])
def login():
    return render_template(
        "main_layout.html", params=params, chatbot_talk="로그인 페이지입니다.", content="login.html"
    )


@app.route("/login", methods=["POST"])
def loginCallback():
    global params

    user_id = request.form.get("inputEmail")
    user_pw = request.form.get("inputPassword")

    # 사용자가 입력한 정보가 회원가입된 사용자인지 확인
    user_info = User.get_user_info(user_id)

    if user_info:
        if user_info["user_pw"] != user_pw:
            return redirect("/login/error")
        login_info = User(user_id=user_info["user_id"])  # 사용자 객체 생성
        login_user(login_info)  # 사용자 객체를 session에 저장
        session["user_id"] = user_id
        session["user_nick"] = user_info["user_nick"]

        return redirect("/")
    else:
        return redirect("/login/error")


@app.route("/logout", methods=["GET"])
def logout():
    logout_user()
    session["user_id"] = None
    session["user_nick"] = None
    return redirect("/")


@app.route("/login/error")
def login_error():
    return render_template(
        "main_layout.html", params=params, chatbot_talk="", content="login.html", retry=True
    )


@app.route("/register", methods=["GET"])
def register():
    return render_template(
        "main_layout.html", params=params, chatbot_talk="회원가입 페이지입니다.", content="register.html"
    )


@app.route("/register/error")
def register_error():
    return render_template(
        "main_layout.html", params=params, chatbot_talk="", content="register.html", retry=True
    )


@app.route("/register", methods=["POST"])
def register_callback():
    user_id = request.form.get("inputEmail")
    user_nick = request.form.get("inputNick")
    user_pw = request.form.get("inputPassword")
    user_rp = request.form.get("repeatPassword")

    print(f"register_callback/user_id: {user_id}")
    if user_pw != user_rp:
        return redirect("/register/error")

    user_info = User.get_user_info(user_id)
    if user_info:
        return redirect("/register/error")

    params = {
        "user_id": user_id,
        "user_nick": user_nick,
        "user_pw": user_pw,
    }
    res = post(f"http://{connect_to}:5001/user", data=parse_json(params))
    if res.status_code == 200:
        print(f"register_callback/res: {res.json()}")
        if res.json()["status"] == STATUS_FAIL:
            return redirect("/register/error")
        return redirect("/login")
    else:
        return redirect("/register/error")


@app.route("/forgot-password", methods=["GET"])
def forgot_password():
    return render_template(
        "main_layout.html",
        params=params,
        chatbot_talk="비밀번호를 잊어버리셨나요?",
        content="forgot-password.html",
        user_info=-1,
    )


@app.route("/forgot-password/find-user", methods=["GET", "POST"])
def forgot_password_find_user():
    user_id = request.form.get("inputEmail")
    print(f"forgot_password_find_user/user_id: {user_id}")

    # 사용자가 입력한 정보가 회원가입된 사용자인지 확인
    user_info = User.get_user_info(user_id)
    if user_info:
        print(f"forgot_password_find_user/user_pw: {user_info['user_pw']}")

    return render_template(
        "main_layout.html",
        content="forgot-password.html",
        params=params,
        chatbot_talk="",
        user_info=user_info,
    )


#%% blank
@app.route("/blank", methods=["GET"])
def blank():
    return render_template(
        "main_layout.html", params=params, chatbot_talk="", content="contents/blank.html"
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
def mk_card_view(src, title, context, href):
    return f"""<div class="card shadow mr-3 mb-4" style="width: 18rem;padding-right:0; padding-left:0;">
            <img class="card-img-top" src="{src}" alt="Card image cap">
            <div class="card-body">
                <h5 class="card-title">{title}</h5>
                <p class="card-text">{context}</p>
                <a href="{href}" class="btn btn-primary">Go</a>
            </div>
        </div>"""


# 가장 정상으로 만든 부분인 것 같음
# 여기서 해당 서버로 요청을 보내 데이터 불러오고 사이트를 띄운다. 끗 깔끔
@app.route("/concept", methods=["GET"])
def concept():
    try:
        res = get(
            f"http://{connect_to}:{PORT_DEST}/theme"
        )  # 통으로 데이터 받고 여기서 처리? 너무 더러워져서 해당 서버에서 처리하는걸로
        if res.status_code == 200:  # 서버와 통신
            theme = res.json()["body"]

            print(theme)
    except:
        print(f"error: concept()")

    return render_template(
        "main_layout.html", params=params, chatbot_talk="", content="contents/concept.html"
    )


#%% Noticeboard
@app.route("/noticeboard", methods=["GET"])
def noticeboard():
    return redirect("/noticeboard/free")


# 게시판 화면 보이기
@app.route("/noticeboard/write", methods=["GET"])
def noticeboard_write():
    return render_template(
        "main_layout.html",
        params=params,
        chatbot_talk="",
        type=dict(request.args)['type'],
        content="contents/noticeboard_write.html",
        tag="free",
    )


# 게시물 작성하기
@app.route("/noticeboard/write", methods=["POST"])
def noticeboard_callback():
    title = request.form.get("title")
    contents = request.form.get("contents")
    type = request.form.get("type")
    # image_list = request.form.get("inputPassword")
    user_nick = session["user_nick"] if session["user_nick"] else "익명"
    try:
        query = {"title": title, "content": contents, "image_list": [], "user_nick": user_nick}
        res = post(
            f"http://{connect_to}:{PORT_NOTICEBOARD}/noticeboard/{type}", data=parse_json(query)
        )
        if res.status_code == 200:  # 서버와 통신
            print("/noticeboard/write: DONE")
        else:
            print("/noticeboard/write: FAIL")
    except:
        pass

    return redirect(f"/noticeboard/{type}")


@app.route("/noticeboard/free", methods=["GET"])
def noticeboard_free():
    try:
        res = get(f"http://{connect_to}:{PORT_NOTICEBOARD}/noticeboard/free")
        if res.status_code == 200:  # 서버와 통신
            table_contents = load_json(res.json()["body"])
    except:
        pass

    return render_template(
        "main_layout.html",
        params=params,
        chatbot_talk="",
        content="contents/noticeboard.html",
        table_contents=table_contents,
        tag="free",
    )


# 게시물 내용 받아오기
@app.route("/noticeboard/free/<int:i>", methods=["GET"])
def noticeboard_free_content(i):

    try:
        res = get(f"http://{connect_to}:{PORT_NOTICEBOARD}/noticeboard/free/{i}")
        if res.status_code == 200:  # 서버와 통신
            post = load_json(res.json()["body"])
    except:
        pass

    return render_template(
        "main_layout.html",
        params=params,
        chatbot_talk="",
        content="contents/noticeboard_content.html",
        post=post,
    )


@app.route("/noticeboard/review", methods=["GET"])
def noticeboard_review():
    try:
        res = get(f"http://{connect_to}:{PORT_NOTICEBOARD}/noticeboard/review")
        if res.status_code == 200:  # 서버와 통신
            table_contents = load_json(res.json()["body"])
    except:
        pass

    return render_template(
        "main_layout.html",
        params=params,
        chatbot_talk="",
        content="contents/noticeboard.html",
        table_contents=table_contents,
        tag="review",
    )


# 게시물 내용 받아오기
@app.route("/noticeboard/review/<int:i>", methods=["GET"])
def noticeboard_review_content(i):

    try:
        res = get(f"http://{connect_to}:{PORT_NOTICEBOARD}/noticeboard/review/{i}")
        if res.status_code == 200:  # 서버와 통신
            post = load_json(res.json()["body"])
    except:
        pass

    return render_template(
        "main_layout.html",
        params=params,
        chatbot_talk="",
        content="contents/noticeboard_content.html",
        post=post,
    )


@app.route("/noticeboard/tip", methods=["GET"])
def noticeboard_tip():
    try:
        res = get(f"http://{connect_to}:{PORT_NOTICEBOARD}/noticeboard/tip")
        if res.status_code == 200:  # 서버와 통신
            table_contents = load_json(res.json()["body"])
    except:
        pass

    return render_template(
        "main_layout.html",
        params=params,
        chatbot_talk="",
        content="contents/noticeboard.html",
        table_contents=table_contents,
        tag="tip",
    )


# 게시물 내용 받아오기
@app.route("/noticeboard/tip/<int:i>", methods=["GET"])
def noticeboard_tip_content(i):

    try:
        res = get(f"http://{connect_to}:{PORT_NOTICEBOARD}/noticeboard/tip/{i}")
        if res.status_code == 200:  # 서버와 통신
            post = load_json(res.json()["body"])
    except:
        pass

    return render_template(
        "main_layout.html",
        params=params,
        chatbot_talk="",
        content="contents/noticeboard_content.html",
        post=post,
    )


#%% Region
@app.route("/region", methods=["GET"])
def region():
    return render_template(
        "main_layout.html", params=params, chatbot_talk="", content="contents/region.html"
    )


#%% Search
@app.route("/search", methods=["GET"])
def search():
    return render_template(
        "main_layout.html", params=params, chatbot_talk="", content="contents/search.html"
    )


@app.route("/chatbot", methods=["POST"])
def chatbot_callback():
    # chatbot session 에 채팅 상황 저장
    session["chat_list"] = request.json["chat_list"]
    print(f"chatbot_callback/chat_list: updated")

    last_chat = request.json["last_chat"]
    print(f"chatbot_callback/last_chat: {last_chat}")

    return _result(STATUS_SUCCESS, "")


@app.route("/chatbot", methods=["DELETE"])
def chatbot_delete():
    # chatbot 채팅 상황 제거
    session.pop("chat_list")
    print(f"chatbot_delete/chat_list: deleted")
    return _result(STATUS_SUCCESS, "")


#%% App Start
if __name__ == "__main__":
    app.secret_key = "여행 de Gaja"
    try:
        # 서버 시작 시 게시판 데이터 불러오기
        res = get(f"http://{connect_to}:{PORT_NOTICEBOARD}/noticeboard/init")
        if res.status_code == 200:  # 서버와 통신
            theme = res.json()["body"]
            print("init-noticeboard: DONE")
    except:
        print(f"init-noticeboard: FALSE")

    app.run(host=f"{connect_to}", port=PORT_BROWSING, debug=True)
