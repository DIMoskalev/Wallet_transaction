from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.exceptions import WalletAlreadyExistsException, NoWalletIdException, InvalidTypeOperation, \
    NotEnoughMoneyException
from app.models import User, Wallet
from app.users.dependencies import get_current_user
from app.wallet.dao import WalletDAO
from app.wallet.schemas import Operation

router = APIRouter(prefix="/api/v1/wallets", tags=["Операции с кошельками"])


@router.post("/create_wallet/", summary="Создать кошелек")
async def create_wallet(db: AsyncSession = Depends(get_db), user: User = Depends(get_current_user)):
    wallet = await WalletDAO.get_one_or_none(user_id=user.id)
    if wallet:
        raise WalletAlreadyExistsException
    new_wallet = Wallet(user_id=user.id)
    db.add(new_wallet)
    await db.commit()
    await db.refresh(new_wallet)
    return {'message': 'Вы успешно добавили кошелек!'}


@router.get("/{wallet_id}/", summary="Получить данные кошелька")
async def get_wallet_info(db: AsyncSession = Depends(get_db),
                          user_data: User = Depends(get_current_user)):
    result = await db.execute(select(Wallet).filter(Wallet.user_id == user_data.id))
    wallet = result.scalars().first()

    if not wallet:
        raise NoWalletIdException

    return wallet


@router.get("/{wallet_id}/balance", summary="Получить баланс кошелька")
async def get_wallet_balance(db: AsyncSession = Depends(get_db),
                             user_data: User = Depends(get_current_user)):
    result = await db.execute(select(Wallet).filter(Wallet.user_id == user_data.id))
    wallet = result.scalars().first()

    if not wallet:
        raise NoWalletIdException

    return f'Баланс кошелька {wallet.balance}'


@router.post("/{wallet_id}/operation", summary="Выполнить операцию изменения баланса")
async def perform_operation(operation: Operation, db: AsyncSession = Depends(get_db),
                            user_data: User = Depends(get_current_user)):
    result_wallet = await db.execute(select(Wallet).filter(Wallet.user_id == user_data.id))
    wallet = result_wallet.scalars().first()

    if not wallet:
        raise NoWalletIdException

    if operation.operation_type not in ["DEPOSIT", "WITHDRAW"]:
        raise InvalidTypeOperation

    if operation.operation_type == "DEPOSIT":
        amount = operation.amount
    elif operation.operation_type == "WITHDRAW" and wallet.balance >= abs(round(float(operation.amount), 2)):
        amount = -operation.amount
    else:
        raise NotEnoughMoneyException
    wallet.balance += round(float(amount), 2)
    await db.commit()
    await db.refresh(wallet)

    return f'Баланс изменен, текущий баланс {wallet.balance}'
