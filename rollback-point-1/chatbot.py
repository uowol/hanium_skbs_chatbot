import os
from google.cloud import dialogflow_v2beta1 as dialogflow
from google.api_core.exceptions import InvalidArgument

DIALOGFLOW_PROJECT_ID = 'who-am-i-afhy'
DIALOGFLOW_LANGUAGE_CODE = 'ko-KR'
GOOGLE_APPLICATION_CREDENTIALS = 'who-am-i-afhy-7af8d105cf22'
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
        
# 인증 정보 경로 설정
def oauth():
    credential_path = r"C:\Users\alllh\OneDrive\바탕 화면\한이음 공모전\개발" + f"/{GOOGLE_APPLICATION_CREDENTIALS}.json"
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credential_path


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