import re
from database import *
from mmethods import _result, parse_json, load_json
from mconsts import *
from flask import Flask, request, redirect, jsonify, session
from dialogflow_response import *

# 세션 다루는 파트, 나중에 업데이트 할 때 유용하게 사용할 것으로 보임.
from flask_cors import CORS, cross_origin
# from flask_session import Session

app = Flask(__name__)
app.secret_key = '여행 de Gaja'
CORS(app)
# Session(app)

db = connect_database("skbs")
collection = use(db, "test-chatbot")

# 대화 내용 저장: 내용 / 시간 / 유저 nick(익명일 수도)
@app.route('/chat', methods=["POST"])
def save_chat():

    return _result(STATUS_SUCCESS, '')

# 그 밖에 로그 저장
@app.route('/log', methods=["POST"])
def save_log():

    return _result(STATUS_SUCCESS, '')

# dialog flow 와 소통 - 의도 분류
# def detect_intent():
#     intent = None

#     # detect intent 모듈
    
#     return intent;

# 의도에 따른 답변 리턴
@app.route('/answer', methods=["GET"])
def answer():
    req = request.args.to_dict()
    question = req['question']
    print(question)
    answer = Res_Verify(question)
    return _result(STATUS_SUCCESS, parse_json(answer))

    intent = detect_intent()

    if intent == '':
        return ;
    if intent == '':
        return ;
    if intent == '':
        return ;
    

# App Start
if __name__=="__main__":
    # app.config['SESSION_TYPE'] = 'filesystem'
    app.run(host="127.0.0.1", port=PORT_CHATBOT, debug=True)