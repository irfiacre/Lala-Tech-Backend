import jwt
import os
import uuid
from dotenv import load_dotenv

# JWT Token -> https://pyjwt.readthedocs.io/en/stable/

def encodeJWT(data)->str:
    try:
        load_dotenv()
        result = jwt.encode(
            data, 
            os.environ.get("JWT_KEY"), 
            algorithm=os.environ.get("JWT_ALGO"),
        )
        return result
    except Exception as ex:
        raise ex

def decodeJWT(jwtStr: str)->str:
    try:
        load_dotenv()
        result = jwt.decode(jwtStr, os.environ.get("JWT_KEY"), algorithms=[os.environ.get("JWT_ALGO")])
        return result
    except jwt.ExpiredSignatureError:
        return 'Expired'
