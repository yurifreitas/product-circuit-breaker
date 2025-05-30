from fastapi import APIRouter, HTTPException, status
from app.auth import create_access_token,verify_token, verify_password, get_password_hash
from app.schemas import Token,User

router = APIRouter()

@router.post("/token", response_model=Token)
async def login_for_access_token(user: User):
    fake_db_password = get_password_hash("mysecretpassword")
    if not verify_password(user.password, fake_db_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciais inválidas",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}