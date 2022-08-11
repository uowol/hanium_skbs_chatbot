from flask import Flask, render_template, request, Markup, redirect, flash
from requests import get, post 
from database import *

# Flask 객체 인스턴스 생성
app = Flask(__name__)

params = {
    "site_name": "GAZAIT",
    "user_id": None,
    "user_nick": None
}

def checklogin():
    islogin = False
    print(f"user_id: {params['user_id']}")
    try:
        res = get(f"http://127.0.0.1:5001/islogin?user_id={params['user_id']}")
        if res.status_code == 200:
            res = res.json()
            islogin = res['content']
        else: islogin = False
    except:
        islogin = False
    return islogin

@app.route('/', methods=['GET'])
def index():
    if request.method == "GET":
        return render_template('main_layout.html', params=params, content="contents/main.html", islogin=checklogin())

#%% Login
@app.route('/login', methods=['GET'])
def login():
    return render_template('main_layout.html', params=params, content="login.html")

@app.route('/login/callback', methods=["POST"])
def loginCallback():
    global params

    user_id = request.form.get('inputEmail')
    user_pw = request.form.get('inputPassword')

    params = {
        "user_id": user_id,
        "user_pw": user_pw
    }
    res = post("http://127.0.0.1:5001/login-handler", data=parse_json(params))
    if res.status_code == 200:
        res = res.json()
        if not res['result']: return redirect('/relogin')
        params['user_id'] = res['content']['id']
        params['user_nick'] = res['content']['nick']
        return redirect('/')
    else:
        return redirect('/relogin')

@app.route('/logout', methods=["GET"])
def logout():
    global params
    res = get(f"http://127.0.0.1:5001/logout-handler?user_id={params['user_id']}")
    if res.status_code == 200:
        res = res.json()
    params['user_id'] = None
    return redirect('/')

@app.route('/relogin')
def relogin():
    return render_template('main_layout.html', params=params, content="login.html", retry=True)

@app.route('/register', methods=['GET'])
def register():
    return render_template('main_layout.html', params=params, content="register.html")

@app.route('/reregister')
def reregister():
    return render_template('main_layout.html', params=params, content="register.html", retry=True)

@app.route('/register/callback', methods=["POST"])
def registerCallback():
    user_id = request.form.get('inputEmail')
    user_nick = request.form.get('inputNick')
    user_pw = request.form.get('inputPassword')
    user_rp = request.form.get('repeatPassword')

    if user_pw != user_rp:
        return redirect('/reregister')

    params = {
        "user_id": user_id,
        "user_nick": user_nick,
        "user_pw": user_pw,
    }
    res = post("http://127.0.0.1:5001/add-user", data=parse_json(params))
    if res.status_code == 200:
        if not res.json()['result']: return redirect('/reregister')
        return redirect('/login')
    else:
        return redirect('/reregister')

@app.route('/forgot-password', methods=['GET'])
def forgot_password():
    return render_template('main_layout.html', params=params, content="forgot-password.html")

# @app.route('/dashboard', methods=['GET'])
# def dashboard():
#     return render_template('main_layout.html', params=params, content="contents/dashboard.html")

#%% Chart
@app.route('/charts', methods=['GET'])
def charts():
    return render_template('main_layout.html', params=params, content="contents/charts.html", islogin=checklogin())

#%% Concept
@app.route('/concept', methods=['GET'])
def concept():
    return render_template('main_layout.html', params=params, content="contents/concept.html", islogin=checklogin())
    
#%% Noticeboard
@app.route('/noticeboard', methods=['GET'])
def noticeboard():
    return redirect("/noticeboard/free", islogin=checklogin())

# 게시판 서버로 보낼 것
@app.route('/noticeboard/write', methods=['GET'])
def noticeboard_write():
    return render_template('main_layout.html', params=params, content="contents/noticeboard_write.html",
        table_contents=get_table_contents("free"), tag="free")

# 게시판 서버로 보낼 것
@app.route('/noticeboard/free', methods=['GET'])
def noticeboard_free():
    return render_template('main_layout.html', params=params, content="contents/noticeboard.html",
        table_contents=get_table_contents("free"), tag="free")
        
# 게시판 서버로 보낼 것
@app.route('/noticeboard/free/<int:i>', methods=['GET'])
def noticeboard_free_content(i):
    return render_template('main_layout.html', params=params, content="contents/noticeboard_content.html",
        title=str(i)+"번째 게시물", noticeboard_content=str(i)+"번째 본문")

# 게시판 서버로 보낼 것
@app.route('/noticeboard/review', methods=['GET'])
def noticeboard_review():
    return render_template('main_layout.html', params=params, content="contents/noticeboard.html",
        table_contents=[], tag="review")

# 게시판 서버로 보낼 것
@app.route('/noticeboard/tip', methods=['GET'])
def noticeboard_tip():
    return render_template('main_layout.html', params=params, content="contents/noticeboard.html",
        table_contents=[], tag="tip")

#%% Region
@app.route('/region', methods=['GET'])
def region():
    return render_template('main_layout.html', params=params, content="contents/region.html", islogin=checklogin())
    
#%% Search
@app.route('/search', methods=['GET'])
def search():
    return render_template('main_layout.html', params=params, content="contents/search.html", islogin=checklogin())
    
# @app.route('/votes', methods=['GET'])
# def votes():
#     return render_template('main_layout.html', params=params, content="contents/votes.html")

#%% Chatbot
@app.route('/chatbot', methods=['GET'])
def chatbot():
    return render_template('main_layout.html', params=params, content="blank.html", islogin=checklogin())

#%% App Start
if __name__=="__main__":
    # oauth()    # 사용자 정보 인증
    # app.run(debug=True)
    app.secret_key = '여행 de Gaja'
    # app.config['SESSION_TYPE'] = 'filesystem'
    app.run(host="127.0.0.1", port="5000", debug=True)