import jwt
import datetime
from jwt import exceptions

# 加的盐
JWT_SALT = "ds()udsjo@jlsdosjf)wjd_#(#)$"


def encode_auth_token(user):
    # 声明类型，声明加密算法
    headers = {
        "typ": "JWT",
        "alg": "HS256",
        'user':user

    }
    # 设置过期时间
    payload = {
        'headers': headers,
        'iss': 'ly',
        'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=20),
        'iat': datetime.datetime.utcnow()
    }
    signature = jwt.encode(payload, JWT_SALT, algorithm="HS256")
    # 返回加密结果
    return signature


def decode_auth_token(auth_token):
    """
    用于解密
    :param token:
    :return:
    """
    try:
        payload = jwt.decode(auth_token, JWT_SALT, options={'verify_exp': False}, algorithms=['HS256'])
        if payload:
            return payload
        else:
            raise jwt.InvalidTokenError

    except jwt.ExpiredSignatureError:
        return 'Token过期'

    except jwt.InvalidTokenError:
        return '无效Token'


if __name__ == '__main__':
    r=encode_auth_token('makaiqiang')
    d=decode_auth_token(r)
    print(d)