from jose import jwt
def encrypt_jwt(data: dict):
    return jwt.encode(data, algorithm="HS256")

def decrypt_jwt(token: str):
    return jwt.decode(token, algorithm="HS256")
