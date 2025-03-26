from database.main_db import Base, engine

# ------- import all models (class tables)
from database.models.tasks import Tasks
from database.models.user import User


# create all table in db if not exists.
Base.metadata.create_all(engine)

# all table instances:
db_tasks = Tasks()
db_users = User()



