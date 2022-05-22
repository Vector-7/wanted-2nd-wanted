import bcrypt


def hash_password(password: str):
    """
    패스워드 암호화 할 때 사용
    """
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password.decode('utf-8')


def match_password(password: str, user_password: str):
    """
    패스워드 매칭
    """
    return bcrypt.checkpw(password.encode('utf-8'), user_password.encode('utf-8'))
