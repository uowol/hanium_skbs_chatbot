from database import *
from mmethods import _result, parse_json, load_json
from mconsts import *
from flask import Flask, request, redirect, jsonify, session

# 세션 다루는 파트, 나중에 업데이트 할 때 유용하게 사용할 것으로 보임.
# from flask_cors import CORS, cross_origin
# from flask_session import Session

app = Flask(__name__)
app.secret_key = '여행 de Gaja'
# CORS(app)
# Session(app)

db = connect_database("skbs")
collection = use(db, "user")


# App Start
if __name__=="__main__":
    # app.config['SESSION_TYPE'] = 'filesystem'
    app.run(host="127.0.0.1", port=PORT_CHATBOT, debug=True)