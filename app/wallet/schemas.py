from pydantic import BaseModel, Field, condecimal


class WalletBase(BaseModel):
    pass


class WalletCreate(WalletBase):
    pass


class WalletGet(WalletBase):
    uuid: str
    balance: condecimal(max_digits=15, decimal_places=2)


class Operation(BaseModel):
    operation_type: str
    amount: condecimal(max_digits=15, decimal_places=2)
