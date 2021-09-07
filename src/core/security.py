from passlib.context import CryptContext


class PasswordHashing:
    def __init__(self) -> None:
        self._crypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def generate_hash(self, password: str) -> str:
        return self._crypt_context.hash(password)

    def verify_hash(self, password: str, hash: str) -> bool:
        return self._crypt_context.verify(password, hash)


password_hashing = PasswordHashing()
