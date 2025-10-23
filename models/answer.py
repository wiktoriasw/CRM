from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.dialects.postgresql import ARRAY
from models.utils import Base, get_uuid4


class Answer(Base):
    __tablename__ = "answer"

    answer_uuid = Column(String, primary_key=True, default=get_uuid4)
    user_uuid = Column(String, ForeignKey("user.user_uuid"), nullable=False)
    answers = Column(ARRAY(String), nullable=False)
    survey_uuid = Column(String, ForeignKey("survey.survey_uuid"), nullable=False)
