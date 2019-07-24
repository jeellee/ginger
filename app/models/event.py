# coding: utf-8
from sqlalchemy import Column, Integer, String, SmallInteger, orm
from app.models.base import Base


class Event(Base):
    """
    id    事件id
    name  事件name
    type   事件分类（事实热点，明星娱乐。。。）
    hot    事件热度
    time   事件创建时间
    topics  事件话题列表（topic_id1, topic_id2）
    """
    id = Column(Integer, primary_key=True)
    name = Column(String(24), nullable=False)
    type = Column(SmallInteger, nullable=False)
    hot = Column(Integer, default=0)
    create_time = Column(Integer, default=0)
    content = Column(String(500))

    @orm.reconstructor
    def __init__(self):
        self.fields = ['id', 'name', 'hot', 'create_time', 'content']
