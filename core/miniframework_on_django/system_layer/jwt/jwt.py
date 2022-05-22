import os

import jwt
import datetime

JWT_FORMAT = {
    'fro': '',  # from
    'iss': '',  # issue
    'aud': '',  # audience
    'iat': '',  # 발행 날짜
    'exp': '',  # 만료 날짜
}
JWT_KEY = os.environ.get('JWT_KEY')
JWT_ALGORITHM = os.environ.get('JWT_ALGORITHM')
DATE_FORMAT = '%Y-%m-%d %H:%M:%S'


def write_jwt(app_name: str, issue: str, audience: str, expire_len: datetime.timedelta):
    raw_data = JWT_FORMAT.copy()

    raw_data['fro'] = app_name
    raw_data['iss'] = issue
    raw_data['aud'] = audience

    now_date = datetime.datetime.now()
    raw_data['iat'] = now_date.strftime(DATE_FORMAT)
    raw_data['exp'] = (now_date + expire_len).strftime(DATE_FORMAT)

    return jwt.encode(raw_data, JWT_KEY, JWT_ALGORITHM)


def read_jwt(jwt_token: str, target_app_name: str):
    # check jwt
    decoded_data = jwt.decode(jwt_token, JWT_KEY, algorithms=[JWT_ALGORITHM])

    app_name = decoded_data['fro']
    issue = decoded_data['iss']
    audience = decoded_data['aud']
    expired_date = datetime.datetime.strptime(decoded_data['exp'], DATE_FORMAT)

    # 만료 확인
    if datetime.datetime.now() < expired_date:
        raise PermissionError("token expired")
    if app_name != target_app_name:
        raise PermissionError("app name is not equal")

    return issue, audience
