from datetime import datetime

from sqlalchemy import (BigInteger, Column, DateTime, ForeignKey, Integer,
                        String, create_engine)
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

import settings

Base = declarative_base()
engine = create_engine(settings.DATABASE_URL, echo=True)


class User(Base):
    __tablename__ = 'Users'
    id = Column(Integer, primary_key=True)
    tg_id = Column(BigInteger, nullable=False)
    connection_date = Column(DateTime, nullable=False, default=datetime.now())
    bot_token = Column(String)
    channel_to_send = Column(BigInteger, nullable=False)
    keywords = relationship(
        'Keyword',
        backref='keyword',
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


Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()
