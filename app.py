import streamlit as st
from datetime import datetime
import pytz

# Fetch all time zones from pytz
all_time_zones = pytz.all_timezones

# Add a select box for time zone selection
selected_time_zone = st.selectbox('Select your time zone', all_time_zones, index=all_time_zones.index('America/Los_Angeles'))

# Set timezone to user's selection
user_tz = pytz.timezone(selected_time_zone)

# Initialize session state variables if they don't exist
if 'tasks' not in st.session_state:
    st.session_state.tasks = []

if 'start_time' not in st.session_state:
    st.session_state.start_time = datetime.now(user_tz)

# Calculate end time as midnight of the current day in user selected timezone
end_time = datetime.now(user_tz).replace(hour=23, minute=59, second=59, microsecond=999999)

def add_task(task_description, time_taken):
    st.session_state.tasks.append({"task": task_description, "time_taken": time_taken, "completed": False})

def complete_task(index):
    st.session_state.tasks[index]["completed"] = True

def delete_task(index):
    del st.session_state.tasks[index]

def reopen_task(index):
    st.session_state.tasks[index]["completed"] = False

# UI for adding tasks
st.title("You think you have time?")
task_description = st.text_input("Task Description")
time_taken = st.number_input("How long do you think it will take? (hours)", min_value=0.0, format="%.1f")
add_task_button = st.button("Add Task", on_click=add_task, args=(task_description, time_taken))

# Display tasks
for index, task in enumerate(st.session_state.tasks):
    col1, col2, col3, col4 = st.columns([3,1,1,1])
    with col1:
        st.write(f"{task['task']}")
    with col2:
        st.write(f"{task['time_taken']} hrs")
    with col3:
        if not task['completed']:
            st.button("Complete", key=f"complete_{index}", on_click=complete_task, args=(index,))
        else:
            st.button("Reopen", key=f"reopen_{index}", on_click=reopen_task, args=(index,))
    with col4:
        st.button("Delete", key=f"delete_{index}", on_click=delete_task, args=(index,))

# Calculate time to midnight from start_time in PST
time_to_midnight = (end_time - st.session_state.start_time).total_seconds() / 3600

# Calculate remaining time considering incomplete tasks
total_time_for_incomplete_tasks = sum(task["time_taken"] for task in st.session_state.tasks if not task["completed"])
remaining_time = max(0, time_to_midnight - total_time_for_incomplete_tasks)

# Display remaining time
st.write(f"## Time Left in the Day: {remaining_time:.1f} hours")
