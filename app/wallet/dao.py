from app.dao.base import BaseDAO
from app.models import Wallet


class WalletDAO(BaseDAO):
    model = Wallet
