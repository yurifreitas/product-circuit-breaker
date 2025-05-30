import os
import jwt
from fastapi import HTTPException
from datetime import datetime, timedelta
from typing import Optional
from passlib.context import CryptContext
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Depends
# Definir a chave secreta e o algoritmo para o JWT
SECRET_KEY = os.getenv("SECRET_KEY")
if not SECRET_KEY:
    raise ValueError("SECRET_KEY não está configurado no ambiente.")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60  # O token expira em 60 minutos

# Definindo o esquema OAuth2
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Função para gerar o token de acesso
def create_access_token(data: dict, expires_delta: Optional[int] = None) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=expires_delta) if expires_delta else datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Função para gerar o refresh token
def create_refresh_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=7)  # Refresh token expira em 7 dias
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

http_bearer = HTTPBearer()

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(http_bearer)) -> str:
    token = credentials.credentials  # Pega o token do cabeçalho Authorization
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=403, detail="Token inválido: 'sub' ausente")
        return username
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=403, detail="Token expirado. Faça login novamente.")
    except jwt.PyJWTError:
        raise HTTPException(status_code=403, detail="Token inválido ou malformado.")

# Função para verificar a senha
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# Função para criar o hash da senha
def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)
