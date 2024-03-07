from datetime import datetime

from sqlalchemy import (BigInteger, Column, DateTime, ForeignKey, Integer,
                        String, Text, create_engine)
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

import settings

Base = declarative_base()
engine = create_engine(settings.DATABASE_URL, echo=True, pool_size=0, max_overflow=0)


class User(Base):
    __tablename__ = 'Users'
    id = Column(Integer, primary_key=True)
    tg_id = Column(BigInteger, nullable=False)
    connection_date = Column(DateTime, nullable=False, default=datetime.now())
    channel_to_send = Column(BigInteger)
    keywords = relationship(
        'Keyword',
        backref='keywords',
        lazy=True,
        cascade='all, delete-orphan'
    )

    def __repr__(self):
        return self.tg_id


class Keyword(Base):
    __tablename__ = 'Keywords'
    id = Column(Integer, primary_key=True)
    owner = Column(Integer, ForeignKey('Users.id'), nullable=False)
    keyword = Column(String)
    date = Column(DateTime, nullable=False, default=datetime.now())

    def __repr__(self):
        return f'{self.user} - {self.keyword}'


class Channel(Base):
    __tablename__ = 'Channels'
    id = Column(Integer, primary_key=True)
    owner = Column(Integer, ForeignKey('Users.id'), nullable=False)
    channel = Column(String)
    date = Column(DateTime, nullable=False, default=datetime.now())

    def __repr__(self):
        return f'{self.user} - {self.channel}'


class Message(Base):
    __tablename__ = 'Messages'
    id = Column(Integer, primary_key=True)
    channel_id = Column(BigInteger, nullable=False)
    message_date = Column(DateTime, nullable=False, default=datetime.now())
    message_id = Column(BigInteger, nullable=False)
    message_text = Column(Text)


Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()
