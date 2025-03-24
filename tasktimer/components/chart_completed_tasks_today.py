import streamlit as st
import pandas as pd
from database.db_init import db_tasks
from lib.static import FORMAT_DATATIME, get_priority_name, get_status_name
import altair as alt


def import_chart_completed_tasks_today(curr_date_by_user_timezone):
    tasks_completed_today = db_tasks.get_all_tasks_today_completed(curr_date_by_user_timezone)

    if tasks_completed_today:
        task_list = [{
            "Task": task.desc,
            "Start": task.datetime_start.strftime(FORMAT_DATATIME) if task.datetime_start else '',
            "End": task.datetime_end.strftime(FORMAT_DATATIME) if task.datetime_end else '',
            "Priority": get_priority_name(task.priority),
            "Status": get_status_name(task.status)
        } for task in tasks_completed_today]

        # Преобразование данных в DataFrame
        df = pd.DataFrame(task_list)
        df["Start"] = pd.to_datetime(df["Start"])
        df["End"] = pd.to_datetime(df["End"])
        df["Duration"] = (df["End"] - df["Start"]).dt.total_seconds() / 60  # Длительность в минутах

        # Создаем график
        chart = alt.Chart(df).mark_bar().encode(
            x="Start:T",
            x2="End:T",
            y=alt.Y("Task:N", title="Tasks"),
            color="Status:N"
        ).properties(title="Today's Completed Tasks")

        # Отображение графика
        st.altair_chart(chart, use_container_width=True)
