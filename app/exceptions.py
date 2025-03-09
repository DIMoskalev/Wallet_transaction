from fastapi import status, HTTPException

UserAlreadyExistsException = HTTPException(status_code=status.HTTP_409_CONFLICT,
                                           detail="Пользователь уже существует")

IncorrectEmailOrPasswordException = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                                  detail="Неверная почта или пароль")

TokenExpiredException = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                      detail='Токен истек')

TokenNoFound = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                             detail='Токен не найден')

NoJwtException = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                               detail='Токен не валидный!')

NoUserIdException = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                  detail='Не найден ID пользователя')

ForbiddenException = HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Недостаточно прав!')

WalletAlreadyExistsException = HTTPException(status_code=status.HTTP_409_CONFLICT,
                                             detail="Кошелек уже существует")

NoWalletIdException = HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                    detail='Кошелек не найден')

InvalidTypeOperation = HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                     detail='Не верный тип операции')

ProductIsUnActive = HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                  detail='Товар с текущим id не активен')

NotEnoughMoneyException = HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                        detail='Текущий баланс меньше запрашиваемой суммы')
