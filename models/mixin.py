from sqlalchemy import Column, DateTime, ForeignKey, String
from sqlalchemy.sql import func


class TimestampMixin:
    deleted_at = Column(DateTime(timezone=True), nullable=False)
    created_at = Column(DateTime(timezone=True), nullable=True, default=func.now())
    updated_at = Column(
        DateTime(timezone=True), nullable=True, default=func.now(), onupdate=func.now()
    )


class AuditUserMixin:
    deleted_by = Column(String, ForeignKey("user.user_uuid"), nullable=True)
    updated_by = Column(String, ForeignKey("user.user_uuid"), nullable=True)
