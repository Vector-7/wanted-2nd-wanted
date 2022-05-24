import os
import jwt
import time
import datetime

from core.miniframework_on_django.exc import TokenExpiredError

JWT_KEY = os.environ.get('JWT_KEY')
JWT_ALGORITHM = os.environ.get('JWT_ALGORITHM')
DATE_FORMAT = '%Y-%m-%d %H:%M:%S'


def write_jwt(app_name: str, issue: str, audience: str, expire_len: int):
    raw_data = dict()

    raw_data['fro'] = app_name
    raw_data['iss'] = issue
    raw_data['email'] = audience

    iat = datetime.datetime.now()
    exp = iat + datetime.timedelta(seconds=expire_len*60)
    raw_data['iat'] = time.mktime(iat.timetuple())
    raw_data['exp'] = time.mktime(exp.timetuple())
    return jwt.encode(raw_data, JWT_KEY, JWT_ALGORITHM)


def read_jwt(jwt_token: str, target_app_name: str):
    # check jwt
    decoded_data = jwt.decode(jwt_token, JWT_KEY, algorithms=[JWT_ALGORITHM])

    app_name = decoded_data['fro']
    issue = decoded_data['iss']
    audience = decoded_data['email']
    expired_date = decoded_data['exp']

    # 만료 확인
    if time.time() > expired_date:
        raise TokenExpiredError("token expired")
    if app_name != target_app_name:
        raise PermissionError("app name is not equal")

    return issue, audience
