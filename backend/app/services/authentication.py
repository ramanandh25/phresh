from passlib.context import CryptContext
from backend.app.models.users import UserPasswordUpdate

pwd_context = CryptContext(schemes=["argon2"],deprecated="auto")


class AuthException(BaseException):
    pass


   
class AuthService:

    def create_hashed_password(self, *, plaintext_password: str) -> str:
        hashed_password = self.hash_password(password=plaintext_password)
        return UserPasswordUpdate(password=hashed_password)

    def hash_password(self, *, password: str) -> str:
        return pwd_context.hash(password)

    def verify_password(self, *, password: str, hashed_pw: str) -> bool:
        return pwd_context.verify(password, hashed_pw)