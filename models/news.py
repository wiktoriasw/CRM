from sqlalchemy import Column, DateTime, ForeignKey, String
from sqlalchemy.orm import relationship
from models.utils import Base, get_uuid4


class News(Base):
    __tablename__ = "news"
    news_uuid = Column(String, primary_key=True, default=get_uuid4)
    user_uuid = Column(String, ForeignKey("user.user_uuid"), nullable=False)
    trip_uuid = Column(String, ForeignKey("trip.trip_uuid"), nullable=False)
    content = Column(String, nullable=False)
    title = Column(String, nullable=False)
    publication_date = Column(DateTime, nullable=False)

    user = relationship("User", back_populates="news")
    trip = relationship("Trip", back_populates="news")
