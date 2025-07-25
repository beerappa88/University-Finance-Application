import uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
from .base import BaseModel
from .user import User, Role

class College(BaseModel):
    __tablename__ = "colleges"

    name: Mapped[str] = mapped_column(nullable=False, unique=True)
    code: Mapped[str] = mapped_column(nullable=False, unique=True)
    address: Mapped[str | None] = mapped_column(nullable=True)

    # Relationships
    users: Mapped[list["User"]] = relationship("User", back_populates="college")
    roles: Mapped[list["Role"]] = relationship("Role", back_populates="college")