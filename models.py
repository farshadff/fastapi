from sqlalchemy import Column, Integer, String, Text, DateTime
from database import Base
import datetime

class ServiceResult(Base):
    __tablename__ = "service_results"

    id = Column(Integer, primary_key=True, index=True)
    user = Column(String(50), index=True)
    type = Column(String(50))
    result = Column(Text)
    date = Column(DateTime, default=datetime.datetime.utcnow)
    date_fa = Column(String(50))
