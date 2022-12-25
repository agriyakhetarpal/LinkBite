from sqlalchemy import Boolean, Column, Integer, String, DateTime
from database import Base

class URL(Base):
    __tablename__ = "Table of URLs"

    id = Column(Integer, primary_key=True)
    key = Column(String, unique=True, index=True)
    # for analytics
    secret_key = Column(String, unique=True, index=True)
    target_url = Column(String, index=True)
    is_active = Column(Boolean, default=True)
    clicks = Column(Integer, default=0)
    tags = Column(String, default=None)
    # allow manual expiry date
    active_till = Column(DateTime)