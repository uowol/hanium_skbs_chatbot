from flask import Flask, render_template, request, Markup
from chatbot import *
from database import *

# Flask 객체 인스턴스 생성
app = Flask(__name__)

# MongoDB
db, collection = connect_database()

@app.route('/', methods=("GET", "POST")) # 접속하는 url
def index():
    if request.method == "GET":
        return render_template('index.html', site_name="Travel")
        # return render_template('index.html', chat_logs=Markup("".join(chatting_logs)).unescape())
        
    chat = request.form.get('chat')
    chatting_logs.append(create_chat_reverse(chat))
    response = detect_intent(chat)
    chatting_logs.append(create_chat(response.query_result.fulfillment_text))
    # print(response)
    return render_template('index.html', chat_logs=Markup("".join(chatting_logs)).unescape())

# @app.route('/', methods=("GET", "POST")) # 접속하는 url


# App Start
if __name__=="__main__":
    # chatting_logs = []
    oauth()    # 사용자 정보 인증
    # app.run(debug=True)
    app.run(host="127.0.0.1", port="3000", debug=True)