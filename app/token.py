from fastapi import APIRouter, HTTPException, status
from app.auth import create_access_token,verify_token, verify_password, get_password_hash
from pydantic import BaseModel


router = APIRouter()

# Modelo para a requisição de login
class User(BaseModel):
    username: str
    password: str

# Modelo de resposta do token
class Token(BaseModel):
    access_token: str
    token_type: str

# Rota para login
@router.post("/token", response_model=Token)
async def login_for_access_token(user: User):
    # Aqui você normalmente faria a verificação contra o banco de dados
    fake_db_password = get_password_hash("mysecretpassword")  # Exemplo de senha armazenada no banco

    # Verificar se a senha está correta
    if not verify_password(user.password, fake_db_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciais inválidas",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Gerar o token de acesso
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}