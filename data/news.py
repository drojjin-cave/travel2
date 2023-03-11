from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, orm, BLOB
from .db_session import SqlAlchemyBase

'''
import locale
locale.setlocale(
    category=locale.LC_ALL,
    locale="Russian"
)
'''


class News(SqlAlchemyBase):
    __tablename__ = 'news'

    id = Column(Integer, primary_key=True, autoincrement=True)

    title = Column(String(100), nullable=True, index=True)
    content = Column(String(), nullable=True)
    date = Column(DateTime, default=datetime.now)
    img = Column(String(), default=None)
    user_id = Column(Integer, ForeignKey('users.id'))

    user = orm.relationship('User')

    my_format_data = "%d %B %Y"
    time_format = '%H:%M'
