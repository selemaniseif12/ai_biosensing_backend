from datetime import datetime, timedelta
from passlib.context import CryptContext
from jose import jwt

# Password hashing configuration
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT configuration
SECRET_KEY = "CHANGE_THIS_SECRET_KEY"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60


def _prepare_password(password: str) -> bytes:
    """
    Convert password to bytes and truncate to 72 bytes.
    Bcrypt requires <= 72 bytes.
    """
    if isinstance(password, str):
        password = password.encode("utf-8")
    return password[:72]


def hash_password(password: str) -> str:
    """
    Hash a password using bcrypt with safe truncation.
    """
    prepared = _prepare_password(password)
    return pwd_context.hash(prepared)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a password using bcrypt with safe truncation.
    """
    prepared = _prepare_password(plain_password)
    return pwd_context.verify(prepared, hashed_password)


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    """
    Create a JWT access token with expiration.
    """
    to_encode = data.copy()

    expire = datetime.utcnow() + (
        expires_delta if expires_delta else timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )

    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
