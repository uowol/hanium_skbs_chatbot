from flask import Flask, render_template, request, Markup, redirect
from chatbot import *
from database import *
import time

# Flask 객체 인스턴스 생성
app = Flask(__name__)

# MongoDB
db, collection = connect_database()

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

@app.route('/register', methods=['GET'])
def register():
    return render_template('main_layout.html', site_name=SITE_NAME, content="register.html")

@app.route('/forgot-password', methods=['GET'])
def forgot_password():
    return render_template('main_layout.html', site_name=SITE_NAME, content="forgot-password.html")

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
    return render_template('main_layout.html', site_name=SITE_NAME, content="contents/noticeboard.html")
    
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
    app.run(host="127.0.0.1", port="3000", debug=True)