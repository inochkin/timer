import streamlit as st
from datetime import datetime, timedelta
from sqlalchemy import Column, Integer, DateTime, String, desc

from components.check_user_is_auth import get_current_date_user
from database.main_db import Base, decor_session
from sqlalchemy.dialects.postgresql import UUID
import uuid
from lib.static import STATUS, NOT_COMPLETED, DONE
from sqlalchemy import and_, or_
from sqlalchemy import func


class Tasks(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    # UUID = '9b1deb4d-3b7d-4bad-9bdd-2b0d7b3dcb6d'
    user_id = Column(UUID(as_uuid=True), nullable=False)
    hours_minutes = Column(String)
    desc = Column(String(320))
    status = Column(Integer)    # Created = 0, in progress = 1, done = 2, pause = 3
    priority = Column(Integer)  # low = 0, middle = 1, high = 2
    datetime_create = Column(DateTime)
    datetime_start = Column(DateTime, nullable=True)
    datetime_end = Column(DateTime, nullable=True)


    @staticmethod
    def _get_user_id_object():
        user_id = st.session_state['user_id']
        # print('user_id >>>>', user_id)
        if user_id:
            # Конвертация строки в объект UUID
            return uuid.UUID(user_id)


    @decor_session
    def save_new_task_done(self, hours_minutes, desc, priority, task_start_datetime,
                           task_end_datetime, session):
        user_id = self._get_user_id_object()
        if user_id:
            new_task = Tasks(user_id=user_id,
                             hours_minutes=hours_minutes,
                             desc=desc,
                             status=STATUS[DONE],
                             priority=priority,
                             datetime_create=task_start_datetime,
                             datetime_start=task_start_datetime,
                             datetime_end=task_end_datetime)
            session.add(new_task)
            session.commit()
            return new_task.id


    @decor_session
    def get_all_tasks_today_completed_and_all_not(self, session):
        current_date_user = get_current_date_user()
        user_id = self._get_user_id_object()
        if user_id and current_date_user:
            completed_tasks_today = and_(
                Tasks.user_id == user_id,
                Tasks.status == STATUS[DONE],
                Tasks.datetime_end >= datetime.combine(current_date_user, datetime.min.time())
            )
            not_completed_tasks_all = Tasks.status == STATUS[NOT_COMPLETED]

            return (
                session.query(Tasks)
                .filter(or_(completed_tasks_today, not_completed_tasks_all))
                .order_by(Tasks.id.desc())
                .all()
            )


    @decor_session
    def get_all_tasks_today_completed(self, session):
        current_date_user = get_current_date_user()
        user_id = self._get_user_id_object()
        if user_id and current_date_user:
            return (
                session.query(Tasks)
                .filter(and_(
                    Tasks.user_id == user_id,
                    Tasks.status == STATUS[DONE],
                    Tasks.datetime_end >= datetime.combine(current_date_user, datetime.min.time())
                ))
                .order_by(Tasks.id.desc())
                .all()
            )


    # @decor_session
    # def delete_last_task_not_run(self, session):
    #     user_id = self._get_user_id_object()
    #     if user_id:
    #         last_task_not_run = (session.query(Tasks).
    #                              filter(Tasks.status == STATUS[NOT_COMPLETED], Tasks.user_id == user_id).
    #                              order_by(Tasks.id.desc()).first())
    #         if last_task_not_run:
    #             session.delete(last_task_not_run)
    #             session.commit()
    #             return True


    # @decor_session
    # def update_task_state_done(self, id_task, task_complete_datetime, session):
    #     task_complete_datetime_obj = datetime.strptime(task_complete_datetime, FORMAT_DATATIME)
    #     task = session.query(Tasks).filter(Tasks.id == id_task).first()
    #     if task:
    #         task.status = STATUS[DONE]
    #         task.datetime_end = task_complete_datetime_obj
    #         session.commit()


    @decor_session
    def count_completed_tasks_today(self, session):
        current_date_user = get_current_date_user()
        user_id = self._get_user_id_object()
        if user_id and current_date_user:
            return (
                session.query(func.count(Tasks.id))
                .filter(
                    Tasks.user_id == user_id,
                    Tasks.status == STATUS[DONE],
                    func.date(Tasks.datetime_end) == current_date_user.strftime("%Y-%m-%d")
                )
                .scalar()
            )

        return 0


    @decor_session
    def statistic_graph_by_last_7_days(self, session):
        current_date_user = get_current_date_user()
        user_id = self._get_user_id_object()
        if user_id and current_date_user:
            seven_days_ago = current_date_user - timedelta(days=7)
            # Запрос для выборки данных за последние 7 дней и группировки по дням
            return (
                session.query(
                    func.date(Tasks.datetime_create).label('day'),
                    func.sum(func.cast(func.substring(Tasks.hours_minutes, 1, 2), Integer) * 60 + func.cast(
                        func.substring(Tasks.hours_minutes, 4, 2), Integer)).label('total_minutes')
                )
                .filter(Tasks.datetime_create >= seven_days_ago,
                        Tasks.user_id == user_id)
                .group_by(func.date(Tasks.datetime_create))
                .order_by(desc(func.date(Tasks.datetime_create)))
                .all()
            )

