import sqlalchemy as sa

from storage.db_config import Base


class User(Base):
    __tablename__ = 'users'

    username = sa.Column(sa.String(50), unique=True, primary_key=True)
    created = sa.Column(sa.DateTime, default=sa.func.now())
    password = sa.Column(sa.String(100))
