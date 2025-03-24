from sqlalchemy import Column, String
from database.main_db import Base, decor_session
from sqlalchemy.dialects.postgresql import UUID
import uuid

class Settings(Base):
    __tablename__ = "settings"
    user_id = Column(UUID(as_uuid=True), primary_key=True, unique=True)
    timezone_user = Column(String)
    min_task_user = Column(String)

    @decor_session
    def save_user_timezone(self, timezone, session):

        # TODO need user user auth
        user_id = '9b1deb4d-3b7d-4bad-9bdd-2b0d7b3dcb6d'
        uuid_obj = uuid.UUID(user_id)  # Конвертация строки в объект UUID

        if timezone:
            user = session.query(Settings).filter(Settings.user_id == uuid_obj).first()
            if not user:
                add_setting = Settings(user_id=uuid_obj, timezone_user=timezone)
                session.add(add_setting)
            else:
                user.timezone_user = timezone

            session.commit()

    @decor_session
    def get_timezone_user(self, session):
        # TODO need user user auth
        user_id = '9b1deb4d-3b7d-4bad-9bdd-2b0d7b3dcb6d'
        uuid_obj = uuid.UUID(user_id)  # Конвертация строки в объект UUID
        user = session.query(Settings).filter(Settings.user_id == uuid_obj).first()
        if user:
            return user.timezone_user


    @decor_session
    def save_user_min_time(self, time_sec, session):

        # TODO need user user auth
        user_id = '9b1deb4d-3b7d-4bad-9bdd-2b0d7b3dcb6d'
        uuid_obj = uuid.UUID(user_id)  # Конвертация строки в объект UUID

        if time_sec:
            user = session.query(Settings).filter(Settings.user_id == uuid_obj).first()
            if not user:
                add_setting = Settings(user_id=uuid_obj, min_task_user=time_sec)
                session.add(add_setting)
            else:
                user.min_task_user = time_sec

            session.commit()

    @decor_session
    def get_min_time_user(self, session):
        # TODO need user user auth
        user_id = '9b1deb4d-3b7d-4bad-9bdd-2b0d7b3dcb6d'
        uuid_obj = uuid.UUID(user_id)  # Конвертация строки в объект UUID
        user = session.query(Settings).filter(Settings.user_id == uuid_obj).first()
        if user:
            return user.min_task_user

