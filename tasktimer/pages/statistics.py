import streamlit as st

st.set_page_config(layout="wide")  # Устанавливает широкий макет

from custom.not_main_page_styles import import_not_main_page_styles
from database.db_init import db_tasks
import plotly.express as px

import_not_main_page_styles()


st.title("Statistics")


last_7_days_data = db_tasks.statistic_graph_by_last_7_days()
hours_per_day_str = []

for day, total_minutes in last_7_days_data:
    hours = total_minutes // 60
    minutes = total_minutes % 60
    total_time = f"{hours:02}:{minutes:02}"
    print(f"Date: {day}, Total time: {total_time}")

    hours_per_day_str.append(total_time)  # !!!

days_of_week = [day for day, _ in last_7_days_data]
total_minutes_by_day = [total_minutes for _, total_minutes in last_7_days_data]


print('days_of_week ', days_of_week)
print('total_minutes_by_day ', total_minutes_by_day)


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
