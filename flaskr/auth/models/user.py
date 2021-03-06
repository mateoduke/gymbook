from flask import request
from flaskr import db
from sqlalchemy import  Column, String, Integer, DateTime, Boolean
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from werkzeug.security import check_password_hash

class User(db.Model):
    """User model for user related details"""
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    username = Column(String(80), unique=True, nullable=False)
    first_name = Column(String(80), nullable = False)
    last_name = Column(String(80), nullable = False)
    password = Column(String(80), nullable = False)
    registered_on = Column(DateTime(timezone=True), server_default=func.now())
    admin = Column(Boolean, nullable = False, default = False)

    token = relationship("Token", uselist=False, back_populates='user')

    def __repr__(self):
        return f'<User {self.username}>'


    def save(self):
        """Save method for user model, responsible for handling creating and updating model instance"""
        if self.id is None:
            db.session.add(self)
        return db.session.commit()


    @staticmethod
    def check_user_password(user, entered_password):
        """Validates that the password entered is for the given user

        :param user: User model instance
        :type user: User
        :param entered_password: password for given user
        :type entered_password: str
        :return: True if the password is correct false otherwise
        :rtype: bool
        """
        if not user or not entered_password:
            return False
        if not check_password_hash(user.password, entered_password):
            return False
        return True
