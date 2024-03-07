from sqlalchemy import create_engine, select, desc
from sqlalchemy.orm import sessionmaker

import settings

from .models import Base, User, Channel, Keyword, Message

engine = create_engine(settings.DATABASE_URL, echo=True, pool_size=0, max_overflow=0)
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
    return session.query(User).filter(User.id == 1).first().channel_to_send
#    return session.query(User).filter(User.tg_id == tg_id).first().channel_to_send


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


def add_message(channel_id, message_id, message_date, text):
    session = Session()
    new_message = Message(
        message_date=message_date,
        message_id=message_id,
        channel_id=channel_id,
        message_text=text
    )
    session.add(new_message)
    session.commit()


def get_messages():
    session = Session()
    rows = session.query(Message).count()
    return rows


def get_last_message():
    session = Session()
    return session.query(Message).order_by(Message.id.desc()).first()
