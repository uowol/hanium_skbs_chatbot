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

import pandas as pd

# connect_to = 'ec2-3-115-15-84.ap-northeast-1.compute.amazonaws.com'
is_test = False

connect_to = "127.0.0.1" if is_test else "3.115.15.84"

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
def init_detail():
    global df_detail
    df_detail = pd.read_csv("../data_process/output/dest_id.csv")


init_detail()


@app.route("/detail", methods=["GET"])
def detail():
    req = request.args.to_dict()
    id = None

    if "dest" in req:
        dest = req["dest"]
        # print(df_detail['destination'])
        tmp = df_detail[df_detail["destination"] == dest]
        print("*" * 20, len(tmp))
        if len(tmp):
            id = list(df_detail[df_detail["destination"] == dest]["id"])[0]

    print("=" * 20 + f"detail/dest: {dest}\tid: {id}" + "=" * 20)

    if id:
        return render_template(
            "main_layout.html",
            params=params,
            chatbot_talk="여행지 세부 정보<br>페이지입니다.",
            content="contents/detail.html",
            dest_id=id,
        )
    return render_template(
        "main_layout.html",
        params=params,
        chatbot_talk="관련 정보가 없습니다.<br>다시 시도해주세요.",
        content="contents/detail.html",
        dest_id=id,
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

#%% theme
import numpy as np

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
@app.route("/theme", methods=["GET"])
def theme():
    theme_list = []
    theme_info = {
        ""
    }
    def template(title):
        n = np.random.randint(5)
        return [
            f"{title}은 정말 완벽한 여행지에요!",
            f"힐링이 필요할 때, {title}은 어떤가요?",
            f"오늘같이 훌쩍 떠나고 싶을 때 {title}로 가보는 것은 어떤가요?",
            f"요즘 핫한 그곳! {title}로 떠나요!",
            f"이번 휴가엔 {title}에서 즐거운 시간 어떤가요?"
        ][n]
    for theme in df_search.iloc[:,-2].unique():
        if theme=='수목원/휴양림': theme = '수목원휴양림'
        if theme=='기타_하천/해양': theme = '기타하천해양'
        if theme=='요트/보트': theme = '요트보트'
        if theme=='리조트/온천': theme = '리조트온천'
        theme_list.append({
            "title": theme,
            "info": template(theme),
            "image": f"../../static/img/tags/{theme}.jpg"
        })

    return render_template(
        "main_layout.html", params=params, chatbot_talk="", content="contents/theme.html", theme_list=theme_list
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
        type=dict(request.args)["type"],
        content="contents/noticeboard_write.html",
        tag="free",
    )


# 게시물 작성하기
@app.route("/noticeboard/write", methods=["POST"])
def noticeboard_callback():
    title = request.form.get("title")
    contents = request.form.get("contents")
    contents = contents.replace("\n", "<br>")
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
import json

def init_search():
    global df_search, set_with  # , df_search_total1, df_search_total2, df_search_total3
    df_search = pd.read_csv("../data_process/output/data.csv")
    df_search.iloc[:,-1] = df_search.iloc[:,-1].apply(lambda x: json.loads(x.replace("'", '"')))
    set_with = set()
    df_search.iloc[:,-1].map(lambda x: set_with.update(x))
    print("=" * 20 + "init:search is done." + "=" * 20)
    print(set_with)


init_search()


@app.route("/search", methods=["GET"])
def search():
    req = request.args.to_dict()
    df = df_search.copy()
    m_filter = [True for _ in range(len(df))]
    if '관광지명' in req:
        tmp_filter = [False for _ in range(len(df))]
        res = req['관광지명'].split(',')
        for r in res:
            tmp_filter = tmp_filter | (df['관광지명'] == r)
        m_filter = m_filter & tmp_filter
    if '주소' in req:
        tmp_filter = [False for _ in range(len(df))]
        res = req['주소'].split(',')
        for r in res:
            tmp_filter = tmp_filter | (df['주소'].str.contains(r))
        m_filter = m_filter & tmp_filter
        # m_filter = m_filter & (df['주소'].str.contains(req['주소']))
    if '지역' in req:
        tmp_filter = [False for _ in range(len(df))]
        if '특별시,광역시' in req['지역']: 
            print(req['지역'])
            if ' ' in req['지역']: req['지역'] = req['지역'].split(' ')[1]
        res = req['지역'].split(',')
        for r in res:
            tmp_filter = tmp_filter | (df['지역'].str.contains(r))
        m_filter = m_filter & tmp_filter
        # m_filter = m_filter & (df['지역'].str.contains(req['지역']))
    if '태그' in req:
        tmp_filter = [False for _ in range(len(df))]
        res = req['태그'].split(',')
        for r in res:
            tmp_filter = tmp_filter | (df['태그'] == r)
        m_filter = m_filter & tmp_filter
        # m_filter = m_filter & (df['태그'] == req['태그'])
    if '동반 유형' in req:
        tmp_filter = [False for _ in range(len(df))]
        res = req['동반 유형'].split(',')
        for r in res:
            tmp_filter = tmp_filter | (df['동반유형'].astype(str).str.contains(r))
        m_filter = m_filter & tmp_filter
        # m_filter = m_filter & (df['동반유형'].str.contains(req['동반유형']))
    df = df[m_filter]
    # try:
    #     res = get(f"http://{connect_to}:{PORT_DEST}/dest")
    #     if res.status_code == 200:  # 서버와 통신
    #         dest_data = res.json()['body']
    #         df = pd.DataFrame.from_dict(dest_data)
    #         df1 = df[["관광지명", "주소", "분류", "합산 검색 수"]].drop_duplicates().dropna()
    #         dest_data_values = df1.values.tolist()
    #         dest_data_columns = df1.columns.tolist()
    #         # print(dest_data)
    # except:
    #     print(f"error: theme()")
    dest_data_values = df.values.tolist()
    dest_data_columns = df.columns.tolist()
    # print(html_data_values1)
    return render_template(
        "main_layout.html",
        params=params,
        chatbot_talk="",
        data_values=dest_data_values,
        data_columns=dest_data_columns,
        set_with=list(set_with),
        content="contents/search.html",
    )


# @app.route("/search/<int:i>", methods=["GET"])
# def search(i):
#     dest_data_values    = df_search.values.tolist()
#     dest_data_columns   = df_search.columns.tolist()
#     # print(html_data_values1)
#     return render_template('main_layout.html', params=params, chatbot_talk="",
#         data_values=dest_data_values, data_columns=dest_data_columns,
#         content="contents/search.html")


@app.route("/chatbot", methods=["POST"])
def chatbot_callback():
    # chatbot session 에 채팅 상황 저장
    session["chat_list"] = request.json["chat_list"]
    print(f"chatbot_callback/chat_list: updated")

    last_chat = request.json["last_chat"]
    print(f"chatbot_callback/last_chat: {last_chat}")

    if "last_chat_user" in request.json:
        session['last_chat'] = request.json["last_chat_user"]
        print(f"chatbot_callback/last_chat_user: {session['last_chat']}")

    return _result(STATUS_SUCCESS, "")


@app.route("/chatbot", methods=["DELETE"])
def chatbot_delete():
    # chatbot 채팅 상황 제거
    session.pop("chat_list")
    if "last_chat" in session: session.pop("last_chat")
    if "last_chat_user" in session: session.pop("last_chat_user")
    session['chat_list'] = ''
    session['last_chat'] = ''
    session['last_chat_user'] = ''
    print(f"chatbot_delete/chat_list: deleted")
    return _result(STATUS_SUCCESS, "")


#%% App Start
if __name__ == "__main__":
    app.secret_key = "여행 de Gaja"
    try:
        # 서버 시작 시 게시판 데이터 불러오기
        res = get(f"http://{connect_to}:{PORT_NOTICEBOARD}/noticeboard/init")
        if res.status_code == 200:  # 서버와 통신
            print("init-noticeboard: DONE")
    except:
        print(f"init-noticeboard: FALSE")

    app.run(host=f"{connect_to}", port=PORT_BROWSING, debug=True)
