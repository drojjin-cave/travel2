from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, orm
from .db_session import SqlAlchemyBase

#from werkzeug.security import generate_password_hash, check_password_hash


class News(SqlAlchemyBase):
    __tablename__ = 'news'

    id = Column(Integer, primary_key=True, autoincrement=True)

    name = Column(String(100), nullable=True, index=True)
    content = Column(String(), nullable=True)
    date = Column(DateTime, default=datetime.now)

    is_private = Column(Boolean, default=True)

    user_id = Column(Integer, ForeignKey('users.id'))

    user = orm.relationship('User')

    def __repr__(self):
        return f"<news {self.id}>"


'''
class Profiles(SqlAlchemyBase):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    old = db.Column(db.Integer)
    city = db.Column(db.String(100))

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __repr__(self):
        return f"<profiles {self.id}>
''' #  TODO: для дальнейшего создания базы профилей пользователей
