from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Integer, String, DateTime, func
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import mapped_column, Mapped
import os
import atexit
from datetime import datetime
from dotenv import load_dotenv


load_dotenv()

POSTGRES_USER = os.environ.get('POSTGRES_USER')
POSTGRES_PASSWORD = os.environ.get('POSTGRES_PASSWORD')
POSTGRES_DB = os.environ.get('POSTGRES_DB')
POSTGRES_HOST = os.environ.get('POSTGRES_HOST')
POSTGRES_PORT = os.environ.get('POSTGRES_PORT')

PG_DSN = (f'postgresql://'
          f'{POSTGRES_USER}:{POSTGRES_PASSWORD}'
          f'@{POSTGRES_HOST}:{POSTGRES_PORT}'
          f'/{POSTGRES_DB}')

engine = create_engine(PG_DSN)
Session = sessionmaker(bind=engine)


class Base(DeclarativeBase):

    @property
    def to_dict(self):
        return {'id': self.id}

class User(Base):

    __tablename__ = 'app_user'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String, nullable=False)
    registration_time: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    advertisements = relationship("Advertisement", backref="owner")

    @property
    def is_dict(self):
        return {
            'username': self.username,
            'registration_time': self.registration_time
        }

class Advertisement(Base):

    __tablename__ = 'app_advertisement'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=True)
    add_time: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    owner_id: Mapped[int] = mapped_column(Integer, ForeignKey('app_user.id'))

    @property
    def is_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'owner_id': self.owner_id,
            'add_time': self.add_time
        }

atexit.register(engine.dispose)
