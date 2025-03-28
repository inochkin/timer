from datetime import datetime, timezone
from typing import Union
from sqlalchemy import Column, String, Integer, DateTime
from database.main_db import Base, decor_session
from sqlalchemy.dialects.postgresql import UUID
import uuid
import bcrypt
import streamlit as st


class User(Base):
    __tablename__ = "user"
    # UUID = '9b1deb4d-3b7d-4bad-9bdd-2b0d7b3dcb6d'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    username = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    token_confirm = Column(String, unique=True)
    status = Column(Integer, unique=True, default=False)
    date_registration = Column(DateTime, default=datetime.now(timezone.utc))
    timezone_user = Column(String)
    min_task_user = Column(String)
    final_sound = Column(String)

    # --------------------------------------------------------------------

    @staticmethod
    def _get_user_id_object():
        user_id = st.session_state['user_id']
        if user_id:
            # Конвертация строки в объект UUID
            return uuid.UUID(user_id)

    @staticmethod
    def hash_password(password: str) -> str:
        password_code = password.encode('utf-8')
        hashed_password_bytes = bcrypt.hashpw(password_code, bcrypt.gensalt())
        # hashed_password_str = hashed_password_bytes.decode('utf-8')
        hashed_password_str = hashed_password_bytes.decode('utf-8')
        return hashed_password_str


    @staticmethod
    def verify_password(plain_password: str, hashed_password_str: str) -> bool:
        plain_password_bytes = plain_password.encode('utf-8')
        hashed_password_bytes = hashed_password_str.encode('utf-8')
        return bcrypt.checkpw(plain_password_bytes, hashed_password_bytes)


    def verify_token(self, plain_token: str, token_expected: str) -> bool:
        return True if plain_token == token_expected else False


    @decor_session
    def register_user(self, username: str, email: str, password: str, token: str, session):
        '''
        :param username:
        :param email:
        :param password:
        :param token:
        :param session: session is auto close by decorator decor_session.
        :return:
        '''
        hashed_password = self.hash_password(password)
        new_user = User(username=username, email=email, hashed_password=hashed_password,
                        token_confirm=token, status=False)
        session.add(new_user)
        session.commit()
        # print(f"- user {email} was added to db.")


    @decor_session
    def activate_user(self, email, session):
        '''
        :param email:
        :param session: session is auto close by decorator decor_session.
        :return:
        '''
        user = session.query(User).filter(User.email == email).first()
        user.status = True
        session.commit()
        # print(f"- user {email} is activated.")


    @decor_session
    def is_user_exist(self, email: str, session):
        '''
        :param email:
        :param session: session is auto close by decorator decor_session.
        :return:
        '''
        return session.query(User).filter(User.email == email).first()


    @decor_session
    def authenticate_user(self, email: str, password: str, session) -> Union[tuple[True, str, str], str]:
        '''
        Find a user in db and verify the password is correct.
        :param email: is login.
        :param password: password of an user.
        :param session: session is auto close by decorator decor_session.
        :return: True - if user is authenticated. Or return str with error.
        '''
        user = session.query(User).filter(User.email == email).first()
        hashed_password_str = user.hashed_password
        user_status = user.status

        if not user:
            return "- User not found!"

        # check status.
        if not user_status:
            return "- User is not activated! no confirmation by email."

        # if password is wrong.
        if not self.verify_password(password, hashed_password_str):
            return "- Incorrect user or password!"

        # print("- Login successful!")
        # print("--- user status -->", user_status)

        return True, user.id, user.username

    # --------------------------------------------------------------------

    @decor_session
    def save_user_timezone(self, timezone, session):
        user_id = self._get_user_id_object()
        if user_id:
            if timezone:
                user = session.query(User).filter(User.id == user_id).first()
                if user:
                    user.timezone_user = timezone
                    session.commit()


    @decor_session
    def get_timezone_user(self, session):
        user_id = self._get_user_id_object()
        if user_id:
            user = session.query(User).filter(User.id == user_id).first()
            if user:
                return user.timezone_user


    @decor_session
    def save_user_min_time(self, time_sec, session):
        user_id = self._get_user_id_object()
        if user_id:
            if time_sec:
                user = session.query(User).filter(User.id == user_id).first()
                if user:
                    user.min_task_user = time_sec
                    session.commit()


    @decor_session
    def save_final_sound(self, final_sound, session):
        user_id = self._get_user_id_object()
        if user_id:
            if final_sound:
                user = session.query(User).filter(User.id == user_id).first()
                if user:
                    user.final_sound = final_sound
                    session.commit()


    @decor_session
    def get_min_time_user(self, session):
        user_id = self._get_user_id_object()
        if user_id:
            user = session.query(User).filter(User.id == user_id).first()
            if user:
                return user.min_task_user

    @decor_session
    def get_final_sound_user(self, session):
        user_id = self._get_user_id_object()
        if user_id:
            user = session.query(User).filter(User.id == user_id).first()
            if user:
                return user.final_sound


    @decor_session
    def get_all_users(self, session):
        users = session.query(User).all()
        user_data = []
        for user in users:
            user_data.append({"id": str(user.id),
                              "name": user.username,
                              "email": user.email,
                              "hashed_password": user.hashed_password,
                              "token_confirm": user.token_confirm,
                              "status": user.status,
                              "date_registration": user.date_registration,
                              "timezone_user": user.timezone_user,
                              "min_task_user": user.min_task_user})
        return user_data

