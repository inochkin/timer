import streamlit as st
import pandas as pd
from database.db_init import db_tasks
from lib.static import FORMAT_DATATIME, get_priority_name, get_status_name
from lib.general_func import highlight_cells


def import_table_today_tasks(curr_date_by_user_timezone, count_completed_tasks_today):

    tasks_today = db_tasks.get_all_tasks_today_completed_and_all_not(curr_date_by_user_timezone)
    if tasks_today:
        task_list = [{"№": index,
                      "🕗 Created": task.datetime_create.strftime(FORMAT_DATATIME) if task.datetime_create else '',
                      "🕗 Start": task.datetime_start.strftime(FORMAT_DATATIME) if task.datetime_start else '',
                      "🕗 End": task.datetime_end.strftime(FORMAT_DATATIME) if task.datetime_end else '',
                      "Period": task.hours_minutes,
                      "📝Description": task.desc,
                      "Priority": get_priority_name(task.priority),
                      "Status": get_status_name(task.status)
                      } for index, task in enumerate(tasks_today, start=1)]

        df = pd.DataFrame(task_list)
        # Применяем стили
        styled_df = df.style.map(highlight_cells, subset=["Status"])
        st.dataframe(styled_df, hide_index=True)

        # ----- total
        st.text(f"Completed tasks: {count_completed_tasks_today}")

