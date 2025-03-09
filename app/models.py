from uuid import uuid4, UUID

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, relationship, mapped_column
from sqlalchemy.dialects.postgresql import UUID as UUIDType

from app.database import Base, str_uniq, str_null_false, bool_default_true, bool_default_false, int_pk, \
    float_null_false


class User(Base):
    id: Mapped[int_pk]
    full_name: Mapped[str]
    email: Mapped[str_uniq]
    phone: Mapped[str_uniq]
    hashed_password: Mapped[str_null_false]
    is_active: Mapped[bool_default_true]
    is_admin: Mapped[bool_default_false]

    wallets: Mapped["Wallet"] = relationship("Wallet", back_populates="users", lazy="selectin")

    def __str__(self):
        return (f"{self.__class__.__name__}(id={self.id}, "
                f"fullname={self.full_name!r},"
                f"email={self.email!r})")

    def __repr__(self):
        return str(self)


class Wallet(Base):
    uuid: Mapped[UUID] = mapped_column(UUIDType(as_uuid=True), primary_key=True, default=uuid4, nullable=False)
    balance: Mapped[float_null_false]
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)

    users: Mapped["User"] = relationship("User", back_populates="wallets", lazy="selectin")

    def __str__(self):
        return f"{self.__class__.__name__}, balance={self.balance}"

    def __repr__(self):
        return str(self)
