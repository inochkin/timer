import streamlit as st
st.set_page_config(layout="wide")

from components.chart_completed_tasks_today import import_chart_completed_tasks_today
from components.table_todays_tasks import import_table_today_tasks
from custom.main_styles import import_main_styles
from custom.sidebar import custom_sidebar
from database.db_init import db_tasks
import plotly.express as px

import_main_styles()
custom_sidebar()


st.title("Statistics")

count_completed_tasks_today = db_tasks.count_completed_tasks_today()

# -- table and chart
if count_completed_tasks_today:
    st.text("The table displays Today's completed tasks.")
    import_table_today_tasks(count_completed_tasks_today)
    # -- chart
    import_chart_completed_tasks_today()
else:
    st.info("- no tasks for Today.")


# ------------------------------ last_7_days_data
last_7_days_data = db_tasks.statistic_graph_by_last_7_days()
hours_per_day_str = []

if last_7_days_data:
    for day, total_minutes in last_7_days_data:
        hours = total_minutes // 60
        minutes = total_minutes % 60
        total_time = f"{hours:02}:{minutes:02}"
        hours_per_day_str.append(total_time)

    days_of_week = [day for day, _ in last_7_days_data]
    total_minutes_by_day = [total_minutes for _, total_minutes in last_7_days_data]


    # print('days_of_week ', days_of_week)
    # print('total_minutes_by_day ', total_minutes_by_day)

    # Создаем DataFrame
    import pandas as pd
    df = pd.DataFrame({
        'Day': days_of_week,
        'Hours': total_minutes_by_day
    })

    # Создаем график с помощью plotly
    fig = px.bar(df, x='Day', y='Hours', title='Last 7 days period: count of spent time')

    # force change Order.
    fig.update_layout(xaxis_type="category")

    # Форматируем ось X (убираем часы, оставляем только день и месяц)
    fig.update_xaxes(
        dtick="D1",
        tickformat="%Y-%m-%d",  # Можно также "%d %b" (23 Mar)
    )

    # Обновляем ось Y, чтобы она отображала время в формате 'hh:mm'
    fig.update_yaxes(
        tickmode='array',
        tickvals=total_minutes_by_day,
        ticktext=hours_per_day_str
    )

    # Отображаем график в Streamlit
    st.plotly_chart(fig)

else:
    st.info('No data yet.')

