from flask import redirect
from flask_login import LoginManager, login_user, logout_user, UserMixin, login_required, current_user
from database import *

db = connect_database("skbs")
lm = LoginManager()

# 사용자 정보를 조회
@lm.user_loader
def user_loader(user_id):
    """
    user_info_db
    ㄴuser_info
      ㄴuser_id
        user_pw
    """
    user_info = User.get_user_info(user_id)
    login_info = User(user_id=user_info['data'][0]['user_id'])

    return login_info

# 로그인되어 있지 않은 경우
@lm.unauthorized_handler
def unauthorized():
    return redirect("/")

# Login User 객체
class User(UserMixin):
    def __init__(self, user_id):
        self.user_id = user_id
    
    def get_id(self):
        return str(self.user_id)
    
    @staticmethod
    def get_user_info(user_id, user_pw=None):
        result = dict()
        try:
            option = {
                "user_id": user_id
            }
            result['result'] = "success"
            result['data'] = list(find(collection, option))
            result['count'] = len(result['data'])
        except e:
            result['result'] = 'fail'
            result['data'] = e
        finally:
            return result