from flask import Flask, render_template, request, Markup
from chatbot import *
from database import *

# Flask 객체 인스턴스 생성
app = Flask(__name__)

# MongoDB
db, collection = connect_database()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == "GET":
        return render_template('main_layout.html', site_name="Tripvial", content="dashboard.html")
        # return render_template('index.html', chat_logs=Markup("".join(chatting_logs)).unescape())
        
    chat = request.form.get('chat')
    chatting_logs.append(create_chat_reverse(chat))
    response = detect_intent(chat)
    chatting_logs.append(create_chat(response.query_result.fulfillment_text))
    # print(response)
    return render_template('main_layout.html', site_name="Tripvial", content="dashboard.html")

# 완성 페이지에 넣지 않을 페이지
@app.route('/buttons', methods=['GET']) 
def buttons():
    return render_template('main_layout.html', site_name="Tripvial", content="buttons.html")

# 완성 페이지에 넣지 않을 페이지
@app.route('/cards', methods=['GET'])
def cards():
    return render_template('main_layout.html', site_name="Tripvial", content="cards.html")

# 완성 페이지에 넣지 않을 페이지
@app.route('/utilities-color', methods=['GET']) 
def colors():
    return render_template('main_layout.html', site_name="Tripvial", content="utilities-color.html")

# 완성 페이지에 넣지 않을 페이지
@app.route('/utilities-border', methods=['GET'])
def borders():
    return render_template('main_layout.html', site_name="Tripvial", content="utilities-border.html")

# 완성 페이지에 넣지 않을 페이지
@app.route('/utilities-animation', methods=['GET']) 
def animations():
    return render_template('main_layout.html', site_name="Tripvial", content="utilities-animation.html")

# 완성 페이지에 넣지 않을 페이지
@app.route('/utilities-other', methods=['GET'])
def other():
    return render_template('main_layout.html', site_name="Tripvial", content="utilities-other.html")

# 완성 페이지에 넣지 않을 페이지
@app.route('/_charts', methods=['GET'])
def charts():
    return render_template('main_layout.html', site_name="Tripvial", content="charts.html")

# 완성 페이지에 넣지 않을 페이지
@app.route('/tables', methods=['GET'])
def tables():
    return render_template('main_layout.html', site_name="Tripvial", content="tables.html")

@app.route('/login', methods=['GET'])
def login():
    return render_template('main_layout.html', site_name="Tripvial", content="!login.html")

@app.route('/register', methods=['GET'])
def register():
    return render_template('main_layout.html', site_name="Tripvial", content="!register.html")

@app.route('/forgot-password', methods=['GET'])
def forgot_password():
    return render_template('main_layout.html', site_name="Tripvial", content="!forgot-password.html")

# 완성 페이지에 넣지 않을 페이지
@app.route('/404', methods=['GET'])
def notfound():
    return render_template('main_layout.html', site_name="Tripvial", content="404.html")

# 완성 페이지에 넣지 않을 페이지
@app.route('/blank', methods=['GET'])
def blank():
    return render_template('main_layout.html', site_name="Tripvial", content="blank.html")

# App Start
if __name__=="__main__":
    # chatting_logs = []
    oauth()    # 사용자 정보 인증
    # app.run(debug=True)
    app.run(host="127.0.0.1", port="3000", debug=True)