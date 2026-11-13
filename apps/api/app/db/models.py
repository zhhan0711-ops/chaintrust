from sqlalchemy import DateTime, String, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from datetime import datetime

class Base(DeclarativeBase): pass
class AnalysisRecord(Base):
    __tablename__ = "analysis_records"
    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    input_type: Mapped[str] = mapped_column(String(32))
    source_hash: Mapped[str] = mapped_column(String(66), index=True)
    report_hash: Mapped[str] = mapped_column(String(66), index=True)
    report_json: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
