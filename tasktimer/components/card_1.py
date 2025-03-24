import streamlit as st
from components.chart_completed_tasks_today import import_chart_completed_tasks_today
from components.table_todays_tasks import import_table_today_tasks
from custom.create_button import import_create_button_styles


def card_1(curr_datetime_by_user_timezone, next_step, count_completed_tasks_today, curr_date_by_user_timezone):

    st.title("Today's Tasks")

    import_create_button_styles()
    # -- open popup Create Task

    if curr_datetime_by_user_timezone:
        if st.button("Create"):
            next_step()


    # -- table and chart
    if count_completed_tasks_today:
        st.text("The table displays Today's completed tasks.")
        import_table_today_tasks(curr_date_by_user_timezone, count_completed_tasks_today)
        # -- chart
        import_chart_completed_tasks_today(curr_date_by_user_timezone)
    else:
        st.info("- no tasks for Today yet")

