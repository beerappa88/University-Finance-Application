from sqlalchemy import String, Numeric, DateTime, Text, Enum, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
from enum import Enum as PyEnum
import uuid
from .base import BaseModel

class TransactionType(PyEnum):
    COLLEGE_FEE = "college_fee"
    HOSTEL_RENT = "hostel_rent"
    MESS_DUES = "mess_dues"
    LIBRARY_DUES = "library_dues"
    SCHOLARSHIP = "scholarship"
    REFUND = "refund"

class TransactionStatus(PyEnum):
    PENDING = "pending"
    PAID = "paid"
    OVERDUE = "overdue"
    CANCELLED = "cancelled"
    REFUNDED = "refunded"

class PaymentMethod(PyEnum):
    CASH = "cash"
    CARD = "card"
    BANK_TRANSFER = "bank_transfer"
    UPI = "upi"
    CHEQUE = "cheque"

class FinancialRecord(BaseModel):
    __tablename__ = "financial_records"

    college_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("colleges.id", ondelete="CASCADE"), nullable=False, index=True)
    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    transaction_type: Mapped[TransactionType] = mapped_column(Enum(TransactionType), nullable=False)
    amount: Mapped[float] = mapped_column(Numeric(10, 2, asdecimal=True), nullable=False)
    due_date: Mapped[DateTime] = mapped_column(DateTime, nullable=False)
    paid_date: Mapped[DateTime | None] = mapped_column(DateTime, nullable=True)
    status: Mapped[TransactionStatus] = mapped_column(Enum(TransactionStatus), default=TransactionStatus.PENDING)
    payment_method: Mapped[PaymentMethod | None] = mapped_column(Enum(PaymentMethod), nullable=True)
    reference_number: Mapped[str | None] = mapped_column(String, unique=True, nullable=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    late_fee: Mapped[float] = mapped_column(Numeric(10, 2, asdecimal=True), default=0)
    academic_year: Mapped[str] = mapped_column(String, nullable=False)
    semester: Mapped[str | None] = mapped_column(String, nullable=True)

    user: Mapped["User"] = relationship("User", back_populates="financial_records")
    college: Mapped["College"] = relationship("College", back_populates="financial_records")
    audit_logs: Mapped[list["AuditLog"]] = relationship("AuditLog", back_populates="financial_record")

class FeeStructure(BaseModel):
    __tablename__ = "fee_structures"

    college_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("colleges.id", ondelete="CASCADE"), nullable=False, index=True)
    program_name: Mapped[str] = mapped_column(String, nullable=False)
    academic_year: Mapped[str] = mapped_column(String, nullable=False)
    semester: Mapped[str] = mapped_column(String, nullable=False)
    tuition_fee: Mapped[float] = mapped_column(Numeric(10, 2, asdecimal=True), nullable=False)
    lab_fee: Mapped[float] = mapped_column(Numeric(10, 2, asdecimal=True), default=0)
    library_fee: Mapped[float] = mapped_column(Numeric(10, 2, asdecimal=True), default=0)
    sports_fee: Mapped[float] = mapped_column(Numeric(10, 2, asdecimal=True), default=0)
    development_fee: Mapped[float] = mapped_column(Numeric(10, 2, asdecimal=True), default=0)

    college: Mapped["College"] = relationship("College", back_populates="fee_structures")

    @property
    def total_fee(self):
        return (self.tuition_fee + self.lab_fee + self.library_fee +
                self.sports_fee + self.development_fee)

class HostelRoom(BaseModel):
    __tablename__ = "hostel_rooms"

    college_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("colleges.id", ondelete="CASCADE"), nullable=False, index=True)
    room_number: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    room_type: Mapped[str] = mapped_column(String, nullable=False)  # single, double, triple
    capacity: Mapped[int] = mapped_column(Integer, nullable=False)
    monthly_rent: Mapped[float] = mapped_column(Numeric(10, 2, asdecimal=True), nullable=False)
    security_deposit: Mapped[float] = mapped_column(Numeric(10, 2, asdecimal=True), nullable=False)

    college: Mapped["College"] = relationship("College", back_populates="hostel_rooms")
    occupancies: Mapped[list["HostelOccupancy"]] = relationship("HostelOccupancy", back_populates="room")

class HostelOccupancy(BaseModel):
    __tablename__ = "hostel_occupancies"

    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    room_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("hostel_rooms.id"), nullable=False)
    check_in_date: Mapped[DateTime] = mapped_column(DateTime, nullable=False)
    check_out_date: Mapped[DateTime | None] = mapped_column(DateTime, nullable=True)
    security_deposit_paid: Mapped[float] = mapped_column(Numeric(10, 2, asdecimal=True), default=0)

    user: Mapped["User"] = relationship("User")
    room: Mapped["HostelRoom"] = relationship("HostelRoom", back_populates="occupancies")

class AuditLog(BaseModel):
    __tablename__ = "audit_logs"

    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    financial_record_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("financial_records.id"), nullable=True)
    action: Mapped[str] = mapped_column(String, nullable=False)
    old_values: Mapped[str | None] = mapped_column(Text, nullable=True)  # JSON string
    new_values: Mapped[str | None] = mapped_column(Text, nullable=True)  # JSON string
    ip_address: Mapped[str | None] = mapped_column(String, nullable=True)
    user_agent: Mapped[str | None] = mapped_column(String, nullable=True)

    user: Mapped["User"] = relationship("User")
    financial_record: Mapped["FinancialRecord"] = relationship("FinancialRecord", back_populates="audit_logs")