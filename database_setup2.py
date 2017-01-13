import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()


class Users(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    password = Column(String(100), nullable=False)
    email = Column(String(100))
    time_created = Column(DateTime(timezone=True), server_default=func.now())

class Posts(Base):
    __tablename__ = 'Posts'

    title = Column(String(250), nullable=False)
    PostText = Column(String, nullable=False)
    id = Column(Integer, primary_key=True)
    time_created = Column(DateTime(timezone=True), server_default=func.now())
    Owner_name = Column(String)
    Owner_id = Column(Integer,ForeignKey('user.id'))
    user = relationship(Users)

class Questions(Base):
    """docstring for ClassName"""
    __tablename__ = 'Questions'

    id = Column(Integer, primary_key=True)
    Questioner_Id = Column(Integer, ForeignKey('user.id'))
    Owner_name = Column(String)
    time_created = Column(DateTime(timezone=True), server_default=func.now())
    Text= Column(String, nullable=False)
    user_rel = relationship(Users)

class Comments(Base):
    __tablename__ = 'Comments'
    id = Column(Integer, primary_key=True)
    Comment = Column(String, nullable=False)
    Commenter_Id = Column(Integer, ForeignKey('user.id')) 
    time_created = Column(DateTime(timezone=True), server_default=func.now())
    Post_id = Column(Integer, ForeignKey('Posts.id'))
    Comment_rel = relationship(Users)
    post_rel = relationship(Posts)

class Comments_questions(Base):
    __tablename__ = "Comments_questions"
    id = Column(Integer, primary_key=True)
    Comment = Column(String)
    Commenter_Id = Column(Integer, ForeignKey('user.id')) 
    time_created = Column(DateTime(timezone=True), server_default=func.now())
    Question_id = Column(Integer, ForeignKey('Questions.id'))
    Comment_rel = relationship(Users)
    ques_rel = relationship(Questions)


        
engine = create_engine('sqlite:///Blog.db')


Base.metadata.create_all(engine)