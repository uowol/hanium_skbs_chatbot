import re
from database import *
from mmethods import _result, parse_json, load_json
from mconsts import *
from flask import Flask, request, redirect, jsonify, session
from dialogflow_response import *

# 세션 다루는 파트, 나중에 업데이트 할 때 유용하게 사용할 것으로 보임.
from flask_cors import CORS, cross_origin

# from flask_session import Session


connect_to = '127.0.0.1'


app = Flask(__name__)
app.secret_key = "여행 de Gaja"
CORS(app)
# Session(app)


db = connect_database("skbs")
col_chatbot     = use(db, "test-chatbot")
col_dest        = use(db, "test-dest")


# 대화 내용 저장: 내용 / 시간 / 유저 nick(익명일 수도)
@app.route("/chat", methods=["POST"])
def save_chat():

    return _result(STATUS_SUCCESS, "")


# 그 밖에 로그 저장
@app.route("/log", methods=["POST"])
def save_log():

    return _result(STATUS_SUCCESS, "")


# 꼬리질문에 대한 답변 리턴
@app.route('/answer/follow', methods=["GET"])
def answer_on_follow():
    # if not response: return _result(STATUS_FAIL, '')

    # 

    req = request.args.to_dict()
    intent = req['intent']
    args = req['args']
    print("answer_on_follow/intent: "+intent)
    print("answer_on_follow/args: "+args)
    
    # args가 리스트형식이라면 형변환
    if ',' in args: args = args.split(',') # !!! args엔 다른 ','가 들어가선 안됨

    if intent == "recommend":
        query = ''
        is_changed = False
        for q in args[2].split('_'):
            print("!!!" + q)
            key, val = q.split('=')
            if key == args[0]:  # 이미 쿼리 안에 존재하면 변경
                val = args[1]
                is_changed = True
            query += f'{key}={val}_'
        if not is_changed: query += (args[0] + '=' + args[1] + '_') # 존재하지 않으면 추가
        query = query[0:-1]

        print("answer_on_follow/query: "+query)

        # 위 정보로 관광지 데이터베이스 필터링, 개수 반환 #
        cnt = 1987

        answer = f"text]관련 관광지가 <strong>{cnt}</strong>개 있습니다. <br>{query.replace('_',', ')} <br>\
            더 자세한 결과를 원하신다면 아래 선택지를 클릭하거나 더 자세하게 질문해주세요.\
            |btn]결과<br>확인하기@location.href='/search?{query.replace('_','&').replace('_','&')}'\
            |btn]지역<br>설정하기@followed_chat('+지역', 'recommend', '시/군', '{query}')\
            |btn]동반유형<br>결정하기@followed_chat('+동반유형', 'recommend', '동반유형', '{query}')\
            |btn]테마<br>결정하기@followed_chat('+테마', 'recommend', '테마', '{query}')"

    return _result(STATUS_SUCCESS, answer)


# 의도에 따른 답변 리턴
@app.route("/answer", methods=["GET"])
def answer():
    req = request.args.to_dict()
    question = req['question']
    print("answer/question: "+question)
    #

    response, intent = Res_Verify(question)
    print("answer/(response, intent): "+str(response)+','+intent)
    # 

    if intent == 'empty':
        answer = "text]" + response
        return _result(STATUS_SUCCESS, answer);
    if intent == 'recommend':
        due = response['기간']
        type = response['동반 유형']
        region = response['도']
        region_detail = response['시/군'] if response['시/군'] != 'null' else response['구']
        # gue = response['구']
        theme = response['테마']

        query = ''
        for key in response:
            if response[key] != None: query += f'{key}={response[key]}_'
        query = query[0:-1]
        # print(query)

        # 위 정보로 관광지 데이터베이스 필터링, 개수 반환 #
        cnt = 1987

        answer = f"text]관련 관광지가 <strong>{cnt}</strong>개 있습니다. <br>{query.replace('_',', ')} <br>\
            더 자세한 결과를 원하신다면 아래 선택지를 클릭하거나 더 자세하게 질문해주세요.\
            |btn]결과<br>확인하기@location.href='/search?{query.replace('_','&')}'\
            |btn]지역<br>설정하기@followed_chat('+지역', 'recommend', '시/군', '{query}')\
            |btn]동반유형<br>결정하기@followed_chat('+동반유형', 'recommend', '동반유형', '{query}')\
            |btn]테마<br>결정하기@followed_chat('+테마', 'recommend', '테마', '{query}')"

        return _result(STATUS_SUCCESS, answer);
    if intent == '더 추가할 것 있으면':
        return _result(STATUS_SUCCESS, answer);
    

# App Start
if __name__ == "__main__":
    # app.config['SESSION_TYPE'] = 'filesystem'
    app.run(host=f"{connect_to}", port=PORT_CHATBOT, debug=True)