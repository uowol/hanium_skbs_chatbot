import os

credential_path = r"C:\Users\삼성\Desktop\재성\한이음 챗봇\trip-recommend-chatbot-9lcf-abc299a72150.json"
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = credential_path

from google.cloud import dialogflow_v2beta1 as dialogflow
from google.api_core.exceptions import InvalidArgument

DIALOGFLOW_PROJECT_ID = "trip-recommend-chatbot-9lcf"
DIALOGFLOW_LANGUAGE_CODE = "ko-KR"
SESSION_ID = "1"


def DetectIntent(text):
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(DIALOGFLOW_PROJECT_ID, SESSION_ID)
    text_input = dialogflow.types.TextInput(text=text, language_code=DIALOGFLOW_LANGUAGE_CODE)
    query_input = dialogflow.types.QueryInput(text=text_input)
    try:
        response = session_client.detect_intent(session=session, query_input=query_input)
    except InvalidArgument:
        print("Query text:", response.query_result.query_text)
        print("Detected intent:", response.query_result.intent.display_name)
        print("Detected intent confidence:", response.query_result.intent_detection_confidence)
        print("Fulfillment text:", response.query_result.fulfillment_text)
    return response


# text에 대하여 응답을 변환하는 함수. 이것의 타입이 str이면 그대로 출력하고 dict면 DB와 연동해서 출력하는 느낌으로.
def Res_Verify(text):
    response = DetectIntent(text).query_result.fulfillment_text
    res_list = response.split("/")

    if res_list[0] == "없음":
        return res_list[1], "empty"

    elif res_list[0] == "추천":
        for i in range(len(res_list)):
            if "None" in res_list[i]:
                res_list[i] = None
            continue

        res_dict = {
            "도": res_list[1],
            "시/군": res_list[2],
            "구": res_list[3],
            "기간": res_list[4],
            "테마": res_list[5],
            "동반 유형": res_list[6],
            "지역": (res_list[1] + " " + res_list[2] + " " + res_list[3]).replace("None", "").strip(),
        }
        return res_dict, "recommend"
    return "잘 모르겠어요. 다시 질문해주세요. ", "empty"


# print(Res_Verify('안녕'))
# print(Res_Verify('충북에 2개월 동안 여자친구랑 갈만한 여행지 추천해 줘'))
