
from passlib.context import CryptContext

# bcrypt 설정
pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)


def hash_password(password: str) -> str:

    return pwd_context.hash(password)


def verify_password(password: str, password_hash: str) -> bool:
  
    try:
        return pwd_context.verify(password, password_hash)
    except Exception:
        return False