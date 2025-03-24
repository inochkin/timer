
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

db_url = "sqlite:///database.db"

engine = create_engine(db_url)

'''
# возможные параметры sessionmaker:
autocommit=False: Вам нужно явно вызывать commit(), чтобы сохранить изменения в базе данных.
autoflush=False: Сессия не будет автоматически отправлять изменения в базу перед 
                 выполнением запросов — это нужно делать вручную через flush() или commit().
'''
Session = sessionmaker(bind=engine)  # Создаем сессию для работы с базой данных
Base = declarative_base()   # Определяем базовый класс


def decor_session(func):
    '''
    decorator for session create and pass it to method and close session.
    '''
    def wrapper(*args, **kwargs):
        session: Session = Session()  # Создаем сессию
        try:
            response = func(*args, session=session, **kwargs)  # Передаем сессию в метод
            return response
        finally:
            session.close()  # Закрываем сессию после выполнения функции
    return wrapper



