from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker

import settings

from .models import Base, User, Channel, Keyword

engine = create_engine(settings.DATABASE_URL, echo=True)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)


def add_user(tg_id):
    session = Session()
    user = session.query(User).filter(User.tg_id == tg_id).first()
    if user is None:
        new_user = User(tg_id=tg_id)
        session.add(new_user)
        session.commit()


def set_user_bot_token(tg_id, token):
    session = Session()
    user = session.query(User).filter(User.tg_id == tg_id).first()
    user.bot_token = token
    session.commit()


def get_user_bot_token(tg_id):
    session = Session()
    user = session.query(User).filter(User.tg_id == tg_id).first()
    return user.bot_token


def set_user_channel_to_send(tg_id, channel):
    session = Session()
    user = session.query(User).filter(User.tg_id == tg_id).first()
    user.channel_to_send = channel
    session.commit()


def get_user_channel_to_send(tg_id):
    session = Session()
    user = session.query(User).filter(User.tg_id == tg_id).first()
    return user.channel_to_send


def add_channel(tg_id, channel):
    session = Session()
    user = session.query(User).filter(User.tg_id == tg_id).first()
    new_channel = Channel(
        channel=channel,
        owner=user.id
    )
    session.add(new_channel)
    session.commit()


def get_channels(tg_id):
    session = Session()
    user = session.query(User).filter(User.tg_id == tg_id).first()
    channels = user.channels
    return channels


def delete_user_channels(channel_id):
    session = Session()
    channel = session.get(Channel, channel_id)
    session.delete(channel)
    session.commit()


def add_keyword(tg_id, keyword):
    session = Session()
    user = session.query(User).filter(User.tg_id == tg_id).first()
    new_keyword = Keyword(
        keyword=keyword,
        owner=user.id
    )
    session.add(new_keyword)
    session.commit()


def get_keywords(tg_id):
    session = Session()
    user = session.query(User).filter(User.tg_id == tg_id).first()
    keywords = user.keywords
    return keywords


def delete_user_keywords(keyword_id):
    session = Session()
    keyword = session.get(Keyword, keyword_id)
    session.delete(keyword)
    session.commit()
