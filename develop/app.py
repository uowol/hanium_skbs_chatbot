import os
from flask import Flask, render_template, request, Markup
from google.cloud import dialogflow_v2beta1 as dialogflow
from google.api_core.exceptions import InvalidArgument
import pymongo

DIALOGFLOW_PROJECT_ID = 'who-am-i-afhy'
DIALOGFLOW_LANGUAGE_CODE = 'ko-KR'
GOOGLE_APPLICATION_CREDENTIALS = 'who-am-i-afhy-fbacb61c9b97'
SESSION_ID = '1'

chatting_logs = []

def create_chat(text):
    return f"""<div class="d-flex flex-row justify-content-start mb-4">
        <img src="https://mdbcdn.b-cdn.net/img/Photos/new-templates/bootstrap-chat/ava1-bg.webp"
          alt="avatar 1" style="width: 45px; height: 100%;">
        <div class="p-3 ms-3" style="border-radius: 15px; background-color: rgba(57, 192, 237,.2);">
          <p class="small mb-0">{text}</p>
        </div>
      </div>"""
    
def create_chat_reverse(text):
    return f"""<div class="d-flex flex-row justify-content-end mb-4">
          <div class="p-3 me-3 border" style="border-radius: 15px; background-color: #fbfbfb;">
            <p class="small mb-0">{text}</p>
          </div>
          <img src="https://mdbcdn.b-cdn.net/img/Photos/new-templates/bootstrap-chat/ava2-bg.webp"
            alt="avatar 1" style="width: 45px; height: 100%;">
        </div>"""


def detect_intent(text):
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(DIALOGFLOW_PROJECT_ID, SESSION_ID)
    text_input = dialogflow.types.TextInput(
        text=text, language_code=DIALOGFLOW_LANGUAGE_CODE
    )
    query_input = dialogflow.types.QueryInput(text=text_input)
    response = {
        "response_id": "",
        "query_result": {
            "query_text": "",
            "action": "",
            "parameters": {},
            "all_required_params_present": "",
            "fulfillment_text": {},
            "fulfillment_messages": {
                "text": {
                    "text": {} 
                }
            },
            "output_contexts": {
                "name": "",
                "lifespan_count": 0,
                "parameters": {
                    "fields": {
                        "key": "no-input",
                        "value": {
                            "number_value": 0
                        }
                    },
                    "fields": {
                        "key": "no-match",
                        "value": {
                            "number_value": 0
                        }
                    }
                }
            },
            "intent": {
                "name": "",
                "display_name": "",
                "is_fallback": ""
            },
            "intent_detection_confidence": 0,
            "language_code": "ko"
            }
    }
    try:    
        response = session_client.detect_intent(session=session, query_input=query_input)
    except InvalidArgument:    
        print("Query text:", response.query_result.query_text)
        print("Detected intent:", response.query_result.intent.display_name)
        print("Detected intent confidence:", response.query_result.intent_detection_confidence)
        print("Fulfillment text:", response.query_result.fulfillment_text)
    return response

# 인증 정보 경로 설정
def oauth():
    credential_path = r"C:\Users\alllh\OneDrive\바탕 화면\한이음 공모전\개발\who-am-i-afhy-7af8d105cf22.json"
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credential_path

# mongo database 연결
def connect_database():
    connect_to = pymongo.MongoClient("localhost", 27017)
    mdb = connect_to.chat_db
    return mdb, mdb.chat

def insert(collection, data_list):
    collection.insert_many(data_list)

def find(collection, options = {}):
    searched = collection.find(options)
    return searched

def update(collection, options = {}):
    collection.update_many(options)

def delete(collection, options = {}):
    collection.delete_many(options)

# Flask 객체 인스턴스 생성
app = Flask(__name__)

# MongoDB
db, collection = connect_database()

@app.route('/', methods=("GET", "POST")) # 접속하는 url
def index():
    if request.method == "GET":
        return render_template('index.html', chat_logs=Markup("".join(chatting_logs)).unescape())
        
    chat = request.form.get('chat')
    chatting_logs.append(create_chat_reverse(chat))
    response = detect_intent(chat)
    chatting_logs.append(create_chat(response.query_result.fulfillment_text))
    # print(response)
    return render_template('index.html', chat_logs=Markup("".join(chatting_logs)).unescape())

# App Start
if __name__=="__main__":
    # chatting_logs = []
    oauth()    # 사용자 정보 인증
    # app.run(debug=True)
    app.run(host="127.0.0.1", port="3000", debug=True)