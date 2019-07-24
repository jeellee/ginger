# coding: utf-8
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base import Base


class Speak(Base):
    id = Column(Integer, primary_key=True)
    time = Column(Integer, unique=True, nullable=False)
    content = Column(String(500), default='')
    user = relationship('User')
    user_id = Column(Integer, ForeignKey('user.id'))
    topic = relationship('Topic')
    topic_id = Column(Integer, ForeignKey('topic.id'))
    topic_choice_blue_or_red = Column(Integer, default=1)


