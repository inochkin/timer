from datetime import datetime, timedelta
from sqlalchemy import Column, Integer, DateTime, String, desc
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


    def get_user_id(self):    # TODO need user user auth
        user_id = '9b1deb4d-3b7d-4bad-9bdd-2b0d7b3dcb6d'
        uuid_obj = uuid.UUID(user_id)  # Конвертация строки в объект UUID
        return uuid_obj


    @decor_session
    def save_new_task_done(self, hours_minutes, desc, priority, task_start_datetime,
                           task_end_datetime, session):

        uuid_obj = self.get_user_id()  # TODO need user user auth

        new_task = Tasks(user_id=uuid_obj,
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
    def get_all_tasks_today_completed_and_all_not(self, curr_date_by_user_timezone, session):

        uuid_obj = self.get_user_id()  # TODO need user user auth

        completed_tasks_today = and_(
            Tasks.user_id == uuid_obj,
            Tasks.status == STATUS[DONE],
            Tasks.datetime_end >= datetime.combine(curr_date_by_user_timezone, datetime.min.time())
        )
        not_completed_tasks_all = Tasks.status == STATUS[NOT_COMPLETED]

        return (
            session.query(Tasks)
            .filter(or_(completed_tasks_today, not_completed_tasks_all))
            .order_by(Tasks.id.desc())
            .all()
        )


    @decor_session
    def get_all_tasks_today_completed(self, curr_date_by_user_timezone, session):

        uuid_obj = self.get_user_id()  # TODO need user user auth

        return (
            session.query(Tasks)
            .filter(and_(
                Tasks.user_id == uuid_obj,
                Tasks.status == STATUS[DONE],
                Tasks.datetime_end >= datetime.combine(curr_date_by_user_timezone, datetime.min.time())
            ))
            .order_by(Tasks.id.desc())
            .all()
        )


    @decor_session
    def delete_last_task_not_run(self, session):

        uuid_obj = self.get_user_id()  # TODO need user user auth

        last_task_not_run = (session.query(Tasks).
                             filter(Tasks.status == STATUS[NOT_COMPLETED], Tasks.user_id == uuid_obj).
                             order_by(Tasks.id.desc()).first())
        if last_task_not_run:
            session.delete(last_task_not_run)
            session.commit()
            return True


    # @decor_session
    # def update_task_state_done(self, id_task, task_complete_datetime, session):
    #     task_complete_datetime_obj = datetime.strptime(task_complete_datetime, FORMAT_DATATIME)
    #     task = session.query(Tasks).filter(Tasks.id == id_task).first()
    #     if task:
    #         task.status = STATUS[DONE]
    #         task.datetime_end = task_complete_datetime_obj
    #         session.commit()


    @decor_session
    def count_completed_tasks_today(self, curr_date_by_user_timezone, session):

        uuid_obj = self.get_user_id()  # TODO need user user auth

        count = (
            session.query(func.count(Tasks.id))
            .filter(
                Tasks.user_id == uuid_obj,
                Tasks.status == STATUS[DONE],
                func.date(Tasks.datetime_end) == curr_date_by_user_timezone
            )
            .scalar()
        )
        return count



    @decor_session
    def statistic_graph_by_last_7_days(self, session):

        uuid_obj = self.get_user_id()  # TODO need user user auth

        seven_days_ago = datetime.now() - timedelta(days=7)
        # Запрос для выборки данных за последние 7 дней и группировки по дням
        return (
            session.query(
                func.date(Tasks.datetime_create).label('day'),
                func.sum(func.cast(func.substring(Tasks.hours_minutes, 1, 2), Integer) * 60 + func.cast(
                    func.substring(Tasks.hours_minutes, 4, 2), Integer)).label('total_minutes')
            )
            .filter(Tasks.datetime_create >= seven_days_ago,
                    Tasks.user_id == uuid_obj)
            .group_by(func.date(Tasks.datetime_create))
            .order_by(desc(func.date(Tasks.datetime_create)))
            .all()
        )


