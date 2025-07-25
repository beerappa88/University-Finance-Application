import uuid
from sqlalchemy import String, Boolean, ForeignKey, Table
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
from .base import BaseModel, Base
from .college import College

# Association table for user <-> role
user_roles = Table(
    "user_roles",
    Base.metadata,
    # Use ondelete for cascading deletes
    mapped_column("user_id", UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), primary_key=True),
    mapped_column("role_id", UUID(as_uuid=True), ForeignKey("roles.id", ondelete="CASCADE"), primary_key=True),
)

# Association table for role <-> permission
role_permissions = Table(
    "role_permissions",
    Base.metadata,
    mapped_column("role_id", UUID(as_uuid=True), ForeignKey("roles.id", ondelete="CASCADE"), primary_key=True),
    mapped_column("permission_id", UUID(as_uuid=True), ForeignKey("permissions.id", ondelete="CASCADE"), primary_key=True),
)


class User(BaseModel):
    __tablename__ = "users"

    # Multi-tenancy: link to college
    college_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("colleges.id", ondelete="CASCADE"), nullable=False, index=True)
    college: Mapped["College"] = relationship("College", back_populates="users")

    email: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)
    username: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String, nullable=False)
    first_name: Mapped[str] = mapped_column(String, nullable=False)
    last_name: Mapped[str] = mapped_column(String, nullable=False)
    student_id: Mapped[str | None] = mapped_column(String, unique=True, nullable=True)
    employee_id: Mapped[str | None] = mapped_column(String, unique=True, nullable=True)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    roles: Mapped[list["Role"]] = relationship(
        "Role", secondary=user_roles, back_populates="users"
    )
    financial_records: Mapped[list["FinancialRecord"]] = relationship(
        "FinancialRecord", back_populates="user"
    )

class Role(BaseModel):
    __tablename__ = "roles"

    # Multi-tenancy: link to college
    college_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("colleges.id", ondelete="CASCADE"), nullable=False, index=True)
    college: Mapped["College"] = relationship("College", back_populates="roles")

    name: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str | None] = mapped_column(String, nullable=True)

    users: Mapped[list["User"]] = relationship(
        "User", secondary=user_roles, back_populates="roles"
    )
    permissions: Mapped[list["Permission"]] = relationship(
        "Permission", secondary=role_permissions, back_populates="roles"
    )

class Permission(BaseModel):
    __tablename__ = "permissions"

    # Multi-tenancy: link to college (optional, if permissions can be college-specific)
    college_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("colleges.id", ondelete="CASCADE"), nullable=True, index=True)
    # If permissions are global, you can set this to nullable=True or remove it

    name: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    description: Mapped[str | None] = mapped_column(String, nullable=True)
    resource: Mapped[str] = mapped_column(String, nullable=False)
    action: Mapped[str] = mapped_column(String, nullable=False)

    roles: Mapped[list["Role"]] = relationship(
        "Role", secondary=role_permissions, back_populates="permissions"
    )