# -*- coding:utf-8 -*-
from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# 创建对象的基类:
Base = declarative_base()
class News(Base):
    __tablename__ = 'news'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(20))
    access_token = Column(String(20))

engine = create_engine('mysql+pymysql://root:941126@localhost:3306/test')
DBSession = sessionmaker(bind=engine)
session = DBSession()
news = News(name='133', access_token='2343234')
session.add(news)
session.commit()
session.close()
