import re
from lib_database import *
from lib_dialogflow_response import *
from lib_db_fun import *
from lib_flask_logging import user_say_logger, res_logger
from global_methods import _result, parse_json, load_json
from global_consts import *
from flask import Flask, request, redirect, jsonify, session
import pandas as pd
from datetime import datetime

# 세션 다루는 파트, 나중에 업데이트 할 때 유용하게 사용할 것으로 보임.
from flask_cors import CORS, cross_origin

# from flask_session import Session

connect_to = "127.0.0.1"

app = Flask(__name__)
app.secret_key = "여행 de Gaja"
CORS(app)
# Session(app)


# db = connect_database("skbs")
# db = connect_database("trip")
# col_chatbot     = use(db, "test-chatbot")
# col_dest        = use(db, "test-dest")
# region = use(db, "region")
# df_temp = to_dflist(db_to_list(region))
# df_region = df_join(df_temp)


##### 업데이트 할 내용
# 데이터는 데이터베이스에 접근해서 가져오기
df_region = pd.read_csv(r"../storage/지역 전체.csv")


# # 대화 내용 저장: 내용 / 시간 / 유저 nick(익명일 수도)
# @app.route("/chat", methods=["POST"])
# def save_chat():

#     return _result(STATUS_SUCCESS, "")


# # 그 밖에 로그 저장
# @app.route("/log", methods=["POST"])
# def save_log():

#     return _result(STATUS_SUCCESS, "")


# 꼬리질문에 대한 답변 리턴
@app.route("/answer/follow", methods=["GET"])
def answer_on_follow():
    req = request.args.to_dict()
    intent = req["intent"]
    args = req["args"]
    print("answer_on_follow/intent: " + intent)
    print("answer_on_follow/args: " + args)

    # args가 리스트형식이라면 형변환
    if "," in args:
        args = args.split(",")  # !!! args엔 다른 ','가 들어가선 안됨

    if intent == "recommend":
        query = ""
        is_changed = False
        if args[2]:
            for q in args[2].split("_"):
                print("!!!" + q)
                key, val = q.split("=")
                if key == args[0]:  # 이미 쿼리 안에 존재하면 변경
                    val = args[1]
                    is_changed = True
                query += f"{key}={val}_"
        if not is_changed:
            query += args[0] + "=" + args[1] + "_"  # 존재하지 않으면 추가
        query = query[0:-1]

        print("answer_on_follow/query: " + query)

        # 위 정보로 관광지 데이터베이스 필터링, 개수 반환 #
        cnt = 1987

        answer = f"text]관련 관광지가 <strong>{cnt}</strong>개 있습니다. <br>{query.replace('_',', ')} <br>\
            더 자세한 결과를 원하신다면 아래 선택지를 클릭하거나 더 자세하게 질문해주세요.\
            |btn]결과 <br>확인@location.href='/search?{query.replace('_','&').replace('_','&')}'\
            |btn]목적지 <br>설정@followed_chat('+지역', 'recommend', '도', '{query}')\
            |btn]출발지 <br>설정@followed_chat('+출발지', 'recommend', '출발지', '{query}')\
            |btn]동반유형 <br>결정@followed_chat('+동반유형', 'recommend', '동반유형', '{query}')\
            |btn]테마 <br>결정@followed_chat('+테마', 'recommend', '테마', '{query}')"

        if args[0] == "도" or args[0] == "세부지역":
            answer = f"text]관련 관광지가 <strong>{cnt}</strong>개 있습니다. <br>{query.replace('_',', ')} <br>\
                더 자세한 결과를 원하신다면 아래 선택지를 클릭하거나 더 자세하게 질문해주세요.\
                |btn]결과<br>확정@location.href='/search?{query.replace('_','&').replace('_','&')}'\
                |btn]다른 목적지 <br>설정@followed_chat('+지역', 'recommend', '도', '{query}')\
                |btn]세부 목적지 <br>설정@followed_chat('+시/군', 'recommend', '시/군', '{query}')\
                |btn]출발지 <br>설정@followed_chat('+출발지', 'recommend', '출발지', '{query}')\
                |btn]동반유형 <br>결정@followed_chat('+동반유형', 'recommend', '동반유형', '{query}')\
                |btn]테마 <br>결정@followed_chat('+테마', 'recommend', '테마', '{query}')"

        if args[0] == "출발지" or args[0] == "세부출발지":
            answer = f"text]관련 관광지가 <strong>{cnt}</strong>개 있습니다. <br>{query.replace('_',', ')} <br>\
                더 자세한 결과를 원하신다면 아래 선택지를 클릭하거나 더 자세하게 질문해주세요.\
                |btn]결과 <br>확정@location.href='/search?{query.replace('_','&').replace('_','&')}'\
                |btn]목적지 <br>설정@followed_chat('+지역', 'recommend', '도', '{query}')\
                |btn]다른 출발지 <br>설정@followed_chat('+출발지', 'recommend', '출발지', '{query}')\
                |btn]세부 출발지<br>설정@followed_chat('+세부출발지', 'recommend', '세부출발지', '{query}')\
                |btn]동반유형 <br>결정@followed_chat('+동반유형', 'recommend', '동반유형', '{query}')\
                |btn]테마 <br>결정@followed_chat('+테마', 'recommend', '테마', '{query}')"

        if args[0] == "동반유형":
            answer = f"text]관련 관광지가 <strong>{cnt}</strong>개 있습니다. <br>{query.replace('_',', ')} <br>\
                더 자세한 결과를 원하신다면 아래 선택지를 클릭하거나 더 자세하게 질문해주세요.\
                |btn]결과 <br>확정@location.href='/search?{query.replace('_','&').replace('_','&')}'\
                |btn]목적지 <br>설정@followed_chat('+지역', 'recommend', '도', '{query}')\
                |btn]출발지 <br>설정@followed_chat('+출발지', 'recommend', '출발지', '{query}')\
                |btn]동반유형 <br>결정@followed_chat('+동반유형', 'recommend', '동반유형', '{query}')\
                |btn]테마 <br>결정@followed_chat('+테마', 'recommend', '테마', '{query}')"

        if args[0] == "테마":
            answer = f"text]관련 관광지가 <strong>{cnt}</strong>개 있습니다. <br>{query.replace('_',', ')} <br>\
                더 자세한 결과를 원하신다면 아래 선택지를 클릭하거나 더 자세하게 질문해주세요.\
                |btn]결과 <br>확정@location.href='/search?{query.replace('_','&').replace('_','&')}'\
                |btn]목적지 <br>설정@followed_chat('+지역', 'recommend', '도', '{query}')\
                |btn]출발지 <br>설정@followed_chat('+출발지', 'recommend', '출발지', '{query}')\
                |btn]동반유형 <br>결정@followed_chat('+동반유형', 'recommend', '동반유형', '{query}')\
                |btn]테마 <br>결정@followed_chat('+테마', 'recommend', '테마', '{query}')"

    return _result(STATUS_SUCCESS, answer)


##### 가이드라인 : 챗봇 레이아웃을 구성하는 html 쿼리문을 아래 함수를 이용하여 작성할 수 있음.


def convert_text(content):
    return f"text]{content}"


def convert_button(content, callback):
    return f"btn]{content}@{callback}"


def convert_bold(content):
    return f"<strong>{content}</strong>"


def add_enter():
    return "<br>"


def replace_text(text, target, word):
    return text.replace(target, word)


def add_separator():
    return "|"


def callback_API(address):
    return f"location.href={address}"


def callback_followed_chat(target, query):
    return f"followed_chat('+{target}', 'recommend', '{target}', '{query}')"


# 의도에 따른 답변 리턴
@app.route("/answer", methods=["GET"])
def answer():
    req = request.args.to_dict()
    question = req["question"]
    user_say_logger.log.info(f"[user_id][{datetime.now()}] > " + question)

    print("answer/question: " + question)  # 질문이 무엇이었는지 출력

    response, intent = Res_Verify(question)
    print("answer/(response, intent): " + str(response) + "," + intent)  # 분류된 의도와 response를 출력

    ##### 가이드라인: 로그를 수집할 때 위 코드의 question, intent, response 변수를 사용할 수 있음.

    if intent == "empty":
        answer = "text]" + response
        return _result(STATUS_SUCCESS, answer)
    if intent == "recommend":
        due = response["기간"]
        type = response["동반 유형"]
        region = response["도"]
        region_detail = response["시/군"] if response["시/군"] != "null" else response["구"]
        # gue = response['구']
        theme = response["테마"]

        cnt = 1987

        if due != None and (type, region, region_detail, theme) == (None, None, None, None):
            answer_df = recommend_day(df_region, question)
            cnt = len(answer_df["관광지명"].unique())

        query = ""
        for key in response:
            if response[key] != None:
                query += f"{key}={response[key]}_"
        query = query[0:-1]
        # print(query)

        # 위 정보로 관광지 데이터베이스 필터링, 개수 반환 #

        answer = f"text]관련 관광지가 <strong>{cnt}</strong>개 있습니다. <br>{query.replace('_',', ')} <br>\
            더 자세한 결과를 원하신다면 아래 선택지를 클릭하거나 더 자세하게 질문해주세요.\
            |btn]결과 <br>확인@location.href='/search?{query.replace('_','&')}'\
            |btn]목적지 <br>설정@followed_chat('+지역', 'recommend', '도', '{query}')\
            |btn]출발지 <br>설정@followed_chat('+출발지', 'recommend', '출발지', '{query}')\
            |btn]동반유형 <br>결정@followed_chat('+동반유형', 'recommend', '동반유형', '{query}')\
            |btn]테마 <br>결정@followed_chat('+테마', 'recommend', '테마', '{query}')"

        response["지역"] = ""
        if response["도"] != None:
            response["지역"] += response["도"] + " "
        if response["시/군"] != None:
            response["지역"] += response["시/군"]
        res_logger.log.info(str(response).replace("'", '"'))

        # answer = (
        #     convert_text(
        #         "관련 관광지가"
        #         + convert_bold(cnt)
        #         + "개 있습니다."
        #         + add_enter()
        #         + replace_text(query, "_", ", ")
        #         + add_enter()
        #         + "더 자세한 결과를 원하신다면 아래 선택지를 클릭하거나 더 자세하게 질문해주세요."
        #     )
        #     + add_separator()
        #     + convert_button(
        #         "결과" + add_enter() + "확정",
        #         callback_API(f"/search?{replace_text(query, '_', '&')}"),
        #     )
        #     + add_separator()
        #     + convert_button("지역" + add_enter() + "설정", callback_followed_chat("지역", query))
        #     + add_separator()
        #     + convert_button("동반유형" + add_enter() + "설정", callback_followed_chat("동반유형", query))
        #     + add_separator()
        #     + convert_button("테마" + add_enter() + "설정", callback_followed_chat("테마", query))
        # )

        return _result(STATUS_SUCCESS, answer)
    if intent == "더 추가할 것 있으면":
        return _result(STATUS_SUCCESS, answer)


# App Start
if __name__ == "__main__":
    # app.config['SESSION_TYPE'] = 'filesystem'
    app.run(host=f"{connect_to}", port=PORT_CHATBOT, debug=True)