from fastapi import APIRouter, Response, Depends

from app.exceptions import UserAlreadyExistsException, IncorrectEmailOrPasswordException
from app.models import User
from app.users.auth import get_password_hash, authenticate_user, create_access_token
from app.users.dao import UsersDAO
from app.users.dependencies import get_current_user, get_current_admin_user
from app.users.schemas import UserCreate, UserGet, UserLogin

router = APIRouter(prefix="/users", tags=["Работа с пользователями"])


@router.post("/register/", summary="Зарегистрировать пользователя")
async def register_user(user_data: UserCreate) -> dict:
    user = await UsersDAO.get_one_or_none(email=user_data.email)
    if user:
        raise UserAlreadyExistsException
    user_dict = user_data.model_dump()
    user_dict['hashed_password'] = get_password_hash(user_data.hashed_password)
    await UsersDAO.add(**user_dict)
    return {'message': 'Вы успешно зарегистрированы!'}


@router.post("/login/", summary="Войти в систему")
async def login_user(response: Response, user_data: UserLogin) -> dict:
    check = await authenticate_user(email=user_data.email, phone=user_data.phone, password=user_data.hashed_password)
    if check is None:
        raise IncorrectEmailOrPasswordException
    access_token = create_access_token({"sub": str(check.id)})
    response.set_cookie(key="users_access_token", value=access_token, httponly=True)
    return {'ok': True, 'access_token': access_token, 'refresh_token': None, 'message': "Авторизация выполнена!"}


@router.post("/logout/", summary="Выйти из системы")
async def logout_user(response: Response):
    response.delete_cookie(key="users_access_token")
    return {'ok': True, 'message': "Вы успешно вышли из системы!"}


@router.get("/all_users/", summary="Получить всех пользователей", response_model=list[UserGet])
async def get_all_users(user_data: User = Depends(get_current_admin_user)):
    return await UsersDAO.get_all()


@router.get("/me/", summary="Получить информацию о текущем пользователе")
async def get_me(user_data: User = Depends(get_current_user)):
    return user_data
