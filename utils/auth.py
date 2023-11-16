"""
@File: auth.py
@Author: 秦宇
@Created: 2023/11/5 14:11
@Description: Created in 咸鱼-自动化-AutoXhs.
"""
import hashlib
import hmac
import os
import time
import uuid
from datetime import datetime

import jwt
import pytz


class Password:
    @staticmethod
    def encrypt(password: str, salt: bytes = None) -> tuple:
        if salt is None:
            salt = os.urandom(16)
        sha256_hash = hashlib.sha256()
        sha256_hash.update(salt + password.encode('utf-8'))
        hashed_password = sha256_hash.hexdigest()
        return hashed_password, salt

    @staticmethod
    def verify(password: str, hashed_password: str, salt: bytes) -> bool:
        calculated_hash, _ = Password.encrypt(password, salt)
        return calculated_hash == hashed_password


class Token:
    __valid_time = 3600

    @classmethod
    def setValidTime(cls, duration: int):
        cls.__valid_time = duration

    @classmethod
    def create(cls, uname: str, upwd: str, secret_key: str) -> str:
        payload = {
            'tokenId': str(uuid.uuid4()),
            'uname': uname,
            'upwd': upwd,
            'exp': int(time.time()) + cls.__valid_time,
        }
        token = jwt.encode(payload, secret_key, algorithm='HS256')
        return token

    @staticmethod
    def unravel(token: str, secret_key: str) -> dict:
        """
        解析token
        :param token:
        :param secret_key:
        :return: tokenId, uname, upwd, exp
        """
        try:
            payload = jwt.decode(token, secret_key, algorithms=['HS256'])
            return payload
        except Exception as e:
            return {
                'tokenId': str(uuid.uuid4()),
                'uname': None,
                'upwd': None,
                'exp': None,
                'error': e
            }

    @staticmethod
    def isValid(token: str, secret_key: str) -> bool:
        try:
            payload = jwt.decode(token, secret_key, algorithms=['HS256'])
            if payload['exp'] > int(time.time()):
                return True
            else:
                return False
        except jwt.InvalidTokenError:
            return False
        except Exception:
            return False


def verifyGPAValues(secret_key, api_path, gpa_s, gpa_t):
    message = f"{api_path}:{gpa_t}"
    expected_gpa_s = hmac.new(secret_key.encode(), message.encode(), hashlib.sha256).hexdigest()
    if hmac.compare_digest(expected_gpa_s, gpa_s):
        now = int(time.mktime(datetime.now(pytz.utc).timetuple()))
        if now - gpa_t <= 60:
            return True
    return False


if __name__ == '__main__':
    pass
