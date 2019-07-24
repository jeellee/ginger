# coding: utf-8
from sqlalchemy import orm
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base import Base, db

# 一个事件一个话题 一个表


class Topic(Base):
    """
    id = 
    user_id = 话题创建人
    name =
    bg = 话题展示页背景
    focus_users = 关注的人
    start_time = 开始时间
    end_time = 结束时间
    brief =话题简介
    content =话题内容
    red_topic =红方主题
    blue_topic =蓝方主题
    event_id = 该话题所属事件
    """
    id = Column(Integer, primary_key=True)
    user = relationship('User')
    user_id = Column(Integer, ForeignKey('user.id'))
    name = Column(String(24), nullable=False)
    # pic  图片信息   存在服务器上，链接 static/fbb_cyy.png
    bg = Column(String(200), nullable=False)
    focus_users = Column(String(24), default='')
    start_time = Column(Integer, default=0)
    end_time = Column(Integer, default=0)
    red_topic = Column(String(24))
    blue_topic = Column(String(24))
    event = relationship('Event')
    event_id = Column(Integer, ForeignKey('event.id'))
    # 话题站队表的表id， 按一定方式生成的id
    # vote_tab = relationship('VoteTab')
    # table_id = Column(Integer, ForeignKey('vote_tab.id'))

    @orm.reconstructor
    def __init__(self):
        self.fields = ['id', 'user_id', 'name', 'bg', 'focus_users',
                       'start_time', 'end_time', 'red_topic', 'blue_topic',
                       'event_id']

    @staticmethod
    def create_topic(user_id, name, start_time, end_time, red_topic,
                     blue_topic, bg, event_id):
        # 1-查询VoteTab表，创建一条数据，并取到id
        # 2-设置VoteTab表 id到topic表
        #
        with db.auto_commit():
            topic = Topic()
            topic.user_id = user_id
            topic.name = name
            topic.start_time = start_time
            topic.end_time = end_time
            topic.red_topic = red_topic
            topic.blue_topic = blue_topic
            topic.event_id = event_id
            topic.bg = bg
            db.session.add(topic)


class Vote(Base):
    """
    站队投票数据表，每一个事件对应一个表
    id = 自增
    table_id = 投票表表id
    vote_time = 投票时间戳
    vote_who = 投票给红方还是蓝方： 0或1
    vote_user = 投票的用户id  （方便统计用户数据）
    topic = 话题表id（外键）
    """
    id = Column(Integer, primary_key=True)
    vote_time = Column(Integer, default=0)
    vote_who = Column(Integer, default=0)
    user = relationship('User')
    vote_user = Column(Integer, ForeignKey('user.id'))
    topic = relationship('Topic')
    topic_id = Column(Integer, ForeignKey('topic.id'))

    @orm.reconstructor
    def __init__(self):
        self.fields = ['vote_time', 'vote_who', 'vote_user', 'topic_id']

    @classmethod
    def create_vote(cls, vote_user, vote_who, vote_topic):
        from datetime import datetime
        with db.auto_commit():
            vote = cls()
            vote.vote_time = "%s" % int(datetime.now().timestamp())
            vote.vote_user = vote_user
            vote.vote_who = vote_who
            vote.topic_id = vote_topic
            db.session.add(vote)


class VoteTab(Base):
    """
    存储 站队投票表 的表
    id = 
    table = 投票表表名
    create_time = 创建时间
    """
    id = Column(Integer, primary_key=True)
    table = Column(String(24), nullable=False)  # VoteData001,VoteData002

    @staticmethod
    def create_vote_tab():
        from datetime import datetime
        # 1-查询VoteTab表，创建一条数据，并取到id
        # 2-设置VoteTab表 id到topic表
        #
        with db.auto_commit():
            vote_tab = VoteTab()
            vote_tab.table = "vote_%s" % int(datetime.now().timestamp())
            db.session.add(vote_tab)
