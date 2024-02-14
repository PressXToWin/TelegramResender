from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker

import settings

from .models import Base, User

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


def get_user_city(tg_id):
    session = Session()
    user = session.query(User).filter(User.tg_id == tg_id).first()
    return user.bot_token
