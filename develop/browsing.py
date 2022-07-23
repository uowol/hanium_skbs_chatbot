from flask import Flask, render_template, request, Markup, redirect, flash
from login import *
from chatbot import *
from database import *
from myfunctions import *
import time

# Flask 객체 인스턴스 생성
app = Flask(__name__)

# Flask Login Manager
lm.init_app(app)

# MongoDB
db = connect_database("skbs")

SITE_NAME = "GAZAIT"

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == "GET":
        return render_template('main_layout.html', site_name=SITE_NAME, content="contents/main.html")
        # return render_template('index.html', chat_logs=Markup("".join(chatting_logs)).unescape())
        
    chat = request.form.get('chat')
    chatting_logs.append(create_chat_reverse(chat))
    response = detect_intent(chat)
    chatting_logs.append(create_chat(response.query_result.fulfillment_text))
    # print(response)
    return render_template('main_layout.html', site_name=SITE_NAME, content="contents/main.html")

# 완성 페이지에 넣지 않을 페이지
@app.route('/buttons', methods=['GET']) 
def buttons():
    return render_template('main_layout.html', site_name=SITE_NAME, content="buttons.html")

# 완성 페이지에 넣지 않을 페이지
@app.route('/cards', methods=['GET'])
def cards():
    return render_template('main_layout.html', site_name=SITE_NAME, content="cards.html")

# 완성 페이지에 넣지 않을 페이지
@app.route('/utilities-color', methods=['GET']) 
def colors():
    return render_template('main_layout.html', site_name=SITE_NAME, content="utilities-color.html")

# 완성 페이지에 넣지 않을 페이지
@app.route('/utilities-border', methods=['GET'])
def borders():
    return render_template('main_layout.html', site_name=SITE_NAME, content="utilities-border.html")

# 완성 페이지에 넣지 않을 페이지
@app.route('/utilities-animation', methods=['GET']) 
def animations():
    return render_template('main_layout.html', site_name=SITE_NAME, content="utilities-animation.html")

# 완성 페이지에 넣지 않을 페이지
@app.route('/utilities-other', methods=['GET'])
def other():
    return render_template('main_layout.html', site_name=SITE_NAME, content="utilities-other.html")

# 완성 페이지에 넣지 않을 페이지
@app.route('/_charts', methods=['GET'])
def _charts():
    return render_template('main_layout.html', site_name=SITE_NAME, content="charts.html")

# 완성 페이지에 넣지 않을 페이지
@app.route('/tables', methods=['GET'])
def tables():
    return render_template('main_layout.html', site_name=SITE_NAME, content="tables.html")

@app.route('/login', methods=['GET'])
def login():
    return render_template('main_layout.html', site_name=SITE_NAME, content="login.html")

@app.route('/login/get_info', methods=['GET', 'POST'])
def login_get_info():
    user_id = request.form.get('inputEmail')
    user_pw = request.form.get('inputPassword')

    if user_id is None or user_pw is None:
        return redirect('/relogin')

    # 사용자가 입력한 정보가 회원가입된 사용자인지 확인
    user_info = User.get_user_info(user_id, user_pw)

    if user_info['result'] != 'fail' and user_info['count'] != 0:
        login_info = User(user_id=user_info['data'][0]['user_id'])  # 사용자 객체 생성
        login_user(login_info)                                      # 사용자 객체를 session에 저장
        return redirect('/')
    else:
        return redirect('/relogin')

@app.route('/logout', methods=['GET'])
def logout():
    logout_user()                                                   # 사용자 객체를 session에서 제거
    return redirect('/')

@app.route('/relogin')
def relogin():
    return render_template('main_layout.html', site_name=SITE_NAME, content="login.html", retry=True)

@app.route('/register', methods=['GET'])
def register():
    return render_template('main_layout.html', site_name=SITE_NAME, content="register.html")

@app.route('/register/add_user', methods=['GET', 'POST'])
def register_add_user():
    user_nick = request.form.get('nickname')
    user_id = request.form.get('inputEmail')
    user_pw = request.form.get('inputPassword')
    user_repw = request.form.get('repeatPassword')

    user_info = User.get_user_info(user_id)
    if user_info['count'] != 0:
        print("중복")
        return redirect('/register')

    try:
        insert(collection=collection, data_list=[{
            "user_nick": user_nick,
            "user_id": user_id,
            "user_pw": user_pw,
            "user_thumbnail": "temp.jpg"
        }])
    except e:
        print(e)

    return redirect('/')

@app.route('/forgot-password', methods=['GET'])
def forgot_password():
    return render_template('main_layout.html', site_name=SITE_NAME, content="forgot-password.html")

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

@app.route('/dashboard', methods=['GET'])
def dashboard():
    return render_template('main_layout.html', site_name=SITE_NAME, content="contents/dashboard.html")

# 완성 페이지에 넣지 않을 페이지
@app.route('/404', methods=['GET'])
def notfound():
    return render_template('main_layout.html', site_name=SITE_NAME, content="404.html")

# 완성 페이지에 넣지 않을 페이지
@app.route('/blank', methods=['GET'])
def blank():
    return render_template('main_layout.html', site_name=SITE_NAME, content="blank.html")

@app.route('/charts', methods=['GET'])
def charts():
    return render_template('main_layout.html', site_name=SITE_NAME, content="contents/charts.html")

@app.route('/concept', methods=['GET'])
def concept():
    return render_template('main_layout.html', site_name=SITE_NAME, content="contents/concept.html")
    
@app.route('/noticeboard', methods=['GET'])
def noticeboard():
    return redirect("/noticeboard/free")

@app.route('/noticeboard/write', methods=['GET'])
def noticeboard_write():
    return render_template('main_layout.html', site_name=SITE_NAME, content="contents/noticeboard_write.html",
        table_contents=get_table_contents("free"), tag="free")

@app.route('/noticeboard/free', methods=['GET'])
def noticeboard_free():
    return render_template('main_layout.html', site_name=SITE_NAME, content="contents/noticeboard.html",
        table_contents=get_table_contents("free"), tag="free")
        
@app.route('/noticeboard/free/<int:i>', methods=['GET'])
def noticeboard_free_content(i):
    return render_template('main_layout.html', site_name=SITE_NAME, content="contents/noticeboard_content.html",
        title=str(i)+"번째 게시물", noticeboard_content=str(i)+"번째 본문")

@app.route('/noticeboard/review', methods=['GET'])
def noticeboard_review():
    return render_template('main_layout.html', site_name=SITE_NAME, content="contents/noticeboard.html",
        table_contents=[], tag="review")

@app.route('/noticeboard/tip', methods=['GET'])
def noticeboard_tip():
    return render_template('main_layout.html', site_name=SITE_NAME, content="contents/noticeboard.html",
        table_contents=[], tag="tip")

@app.route('/region', methods=['GET'])
def region():
    return render_template('main_layout.html', site_name=SITE_NAME, content="contents/region.html")
    
@app.route('/search', methods=['GET'])
def search():
    return render_template('main_layout.html', site_name=SITE_NAME, content="contents/search.html")
    
@app.route('/votes', methods=['GET'])
def votes():
    return render_template('main_layout.html', site_name=SITE_NAME, content="contents/votes.html")

@app.route('/chatbot', methods=['GET'])
def chatbot():
    return render_template('main_layout.html', site_name=SITE_NAME, content="blank.html")

# App Start
if __name__=="__main__":
    # chatting_logs = []
    oauth()    # 사용자 정보 인증
    # app.run(debug=True)
    app.secret_key = '여행 de Gaja'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.run(host="127.0.0.1", port="5000", debug=True)