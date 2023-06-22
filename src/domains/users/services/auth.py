import bcrypt


def verify_password(plain_password: str, hashed_password: str) -> bool:
    password_encoded = plain_password.encode('utf-8')
    hashed_password_encoded = hashed_password.encode('utf-8')
    return bcrypt.checkpw(password_encoded, hashed_password_encoded)


def get_password_hash(password: str) -> str:
    encoded_password = password.encode('utf-8')
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(encoded_password, salt).decode()
