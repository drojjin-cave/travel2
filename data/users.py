from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, orm, BLOB
from .db_session import SqlAlchemyBase
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


class User(SqlAlchemyBase, UserMixin):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=True)
    email = Column(String(50), unique=True,
                   index=True, nullable=True)
    password = Column(String(500), nullable=True)
    role = Column(String(), default='user')
    date = Column(DateTime, default=datetime.now)
    avatar = Column(BLOB, default=None)

    news = orm.relationship("News", back_populates='user')

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def get_id(self):
        return self.id



    def __repr__(self):
        return f"<user> {self.id} {self.name} {self.email}"
