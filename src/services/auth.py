import pickle
from typing import Optional

import redis
from jose import JWTError, jwt  # noqa
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from datetime import datetime, timedelta
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.connect import get_db
from src.repository import users as repository_users
from src.conf.config import config
from src.conf import messages
# from src.database.models import Role


class Auth:
    """Class to handle authentication-related operations."""

    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    SECRET_KEY = config.secret_key
    ALGORITHM = config.algorithm
    oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")
    cache = redis.Redis(
        host=config.redis_host,
        port=config.redis_port,
        password=config.redis_password,
        db=0,
    )

    def verify_password(self, plain_password, hashed_password):
        """Class to handle authentication-related operations."""
        return self.pwd_context.verify(plain_password, hashed_password)

    def get_password_hash(self, password: str):
        """Generate a hashed password from a plain password."""
        return self.pwd_context.hash(password)

    async def create_access_token(
        self, data: dict, expires_delta: Optional[float] = None
    ):
        """
        Create an access token.

        Args:
            data (dict): Data to be encoded in the token.
            expires_delta (Optional[float], optional): Expiry time
            in seconds. Defaults to None.

        Returns:
            str: Encoded access token.
        """
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + timedelta(seconds=expires_delta)
        else:
            expire = datetime.utcnow() + timedelta(minutes=60)
        to_encode.update(
            {"iat": datetime.utcnow(), "exp": expire, "scope": "access_token"}
        )
        encoded_access_token = jwt.encode(
            to_encode, self.SECRET_KEY, algorithm=self.ALGORITHM
        )
        return encoded_access_token

    async def create_refresh_token(
        self, data: dict, expires_delta: Optional[float] = None
    ):
        """
        Create a refresh token.

        Args:
            data (dict): Data to be encoded in the token.
            expires_delta (Optional[float], optional): Expiry time in
            seconds. Defaults to None.

        Returns:
            str: Encoded refresh token.
        """
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + timedelta(seconds=expires_delta)
        else:
            expire = datetime.utcnow() + timedelta(days=7)
        to_encode.update(
            {"iat": datetime.utcnow(), "exp": expire, "scope": "refresh_token"}
        )
        encoded_refresh_token = jwt.encode(
            to_encode, self.SECRET_KEY, algorithm=self.ALGORITHM
        )
        return encoded_refresh_token

    def create_email_token(self, data: dict):
        """
        Create a token for email confirmation.

        Args:
            data (dict): Data to be encoded in the token.

        Returns:
            str: Encoded email confirmation token.
        """
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(days=7)
        to_encode.update({"iat": datetime.utcnow(), "exp": expire})
        token = jwt.encode(to_encode, self.SECRET_KEY, algorithm=self.ALGORITHM)
        return token

    async def get_email_from_token(self, token: str):
        """
        Decode and retrieve the email from an email confirmation token.

        Args:
            token (str): Email confirmation token.

        Returns:
            str: Decoded email.
        """
        try:
            payload = jwt.decode(token, self.SECRET_KEY, algorithms=[self.ALGORITHM])
            email = payload["sub"]
            return email
        except JWTError as e:
            print(e)
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=messages.INVALID_SCOPE_TOKEN,
            )

    async def decode_refresh_token(self, refresh_token: str):
        """
        Decode and retrieve the email from a refresh token.

        Args:
            refresh_token (str): Refresh token.

        Returns:
            str: Decoded email.
        """

        try:
            payload = jwt.decode(
                refresh_token, self.SECRET_KEY, algorithms=[self.ALGORITHM]
            )
            if payload["scope"] == "refresh_token":
                email = payload["sub"]
                return email
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=messages.INVALID_SCOPE_TOKEN,
            )
        except JWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=messages.VALIDATE_CREDENTIALS,
            )

    async def get_current_user(
        self, token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)
    ):
        """
        Get the current authenticated user.

        Args:
            token (str, optional): Access token. Defaults to Depends(oauth2_scheme).
            db (AsyncSession, optional): Async database session. Defaults
            to Depends(get_db).

        Returns:
            User: The authenticated user.
        """
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=messages.VALIDATE_CREDENTIALS,
            headers={"WWW-Authenticate": "Bearer"},
        )

        try:
            payload = jwt.decode(token, self.SECRET_KEY, algorithms=[self.ALGORITHM])
            if payload["scope"] == "access_token":
                email = payload["sub"]
                if email is None:
                    raise credentials_exception
            else:
                raise credentials_exception
        except JWTError:
            raise credentials_exception

        # user = self.cache.get(f"user:{email}")
        user = None #<-- cache is a reason why User.role is not changed quickly --!
        if user is None:
            user = await repository_users.get_user_by_email(email, db)
            if user is None:
                raise credentials_exception
            self.cache.set(f"user:{email}", pickle.dumps(user))  # noqa
            self.cache.expire(f"user:{email}", 900)  # noqa
        else:
            user = pickle.loads(user)
        return user


auth_service = Auth()
