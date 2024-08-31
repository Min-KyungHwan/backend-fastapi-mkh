from passlib.context import CryptContext


my_pass = CryptContext(schemes=["sha256_crypt"])


def hash_password(password: str) -> str:
    hashe_pass = my_pass.hash(password)
    return hashe_pass


def hash_verify(hashe_pass: str, password: str) -> bool:
    return my_pass.verify(password, hashe_pass)
