import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import date

# Set page title
st.set_page_config(page_title="Fitness Progress Tracker", layout="wide")

# Initialize session state
if "data" not in st.session_state:
    try:
        # Load saved data if it exists
        st.session_state["data"] = pd.read_csv("workout_log.csv")
        st.session_state["data"]["Date"] = pd.to_datetime(st.session_state["data"]["Date"])
    except FileNotFoundError:
        # Create an empty DataFrame if no saved data is found
        st.session_state["data"] = pd.DataFrame(columns=["Date", "Exercise", "Reps/Time", "Weight", "Notes"])

# Sidebar: Add new workout entry
st.sidebar.title("Log Workout")

# Suggest exercises based on past data
exercise_suggestions = st.session_state["data"]["Exercise"].unique().tolist()
exercise = st.sidebar.text_input("Exercise Name", "").capitalize()
if exercise_suggestions:
    exercise = st.sidebar.selectbox("Choose or Enter Exercise Name", exercise_suggestions, index=0)

reps_time = st.sidebar.text_input("Reps/Time (e.g., 10 reps or 30 min)", "")
weight = st.sidebar.text_input("Weight (kg)", "")
notes = st.sidebar.text_area("Notes", "")
submit = st.sidebar.button("Add Entry")

# Add workout to the DataFrame
if submit:
    if exercise and reps_time:
        new_entry = {
            "Date": date.today(),
            "Exercise": exercise,
            "Reps/Time": reps_time,
            "Weight": weight,
            "Notes": notes,
        }
        st.session_state["data"] = pd.concat([st.session_state["data"], pd.DataFrame([new_entry])], ignore_index=True)
        # Save updated data to a CSV
        st.session_state["data"].to_csv("workout_log.csv", index=False)
        st.sidebar.success("Workout added and saved!")
    else:
        st.sidebar.error("Please fill in at least the exercise name and reps/time.")

# Main section: Display the workout log
st.title("🏋️ Fitness Progress Tracker")
st.write("Log your workouts and visualize your progress over time.")

if not st.session_state["data"].empty:
    # Display workout log
    st.subheader("Workout Log")
    st.dataframe(st.session_state["data"])

    # Save and download the log
    st.download_button(
        label="Download Workout Log",
        data=st.session_state["data"].to_csv(index=False),
        file_name="workout_log.csv",
        mime="text/csv",
    )

    # Automated calculations
    st.subheader("Workout Summary")
    total_weight = st.session_state["data"]["Weight"].apply(pd.to_numeric, errors="coerce").sum()
    total_sessions = len(st.session_state["data"])
    st.write(f"**Total Weight Lifted (kg):** {total_weight}")
    st.write(f"**Total Sessions Logged:** {total_sessions}")

    # Plot progress
    st.subheader("Progress Visualization")
    exercise_to_plot = st.selectbox("Select an Exercise to Visualize:", st.session_state["data"]["Exercise"].unique())
    exercise_data = st.session_state["data"][st.session_state["data"]["Exercise"] == exercise_to_plot]

    if not exercise_data.empty:
        # Line chart of weight over time
        exercise_data["Date"] = pd.to_datetime(exercise_data["Date"])
        exercise_data["Weight"] = pd.to_numeric(exercise_data["Weight"], errors="coerce")

        # Line plot for weight
        plt.figure(figsize=(10, 5))
        plt.plot(exercise_data["Date"], exercise_data["Weight"], marker="o", label="Weight")
        plt.title(f"{exercise_to_plot} - Weight Progress")
        plt.xlabel("Date")
        plt.ylabel("Weight (kg)")
        plt.grid(True)
        plt.legend()
        st.pyplot(plt.gcf())
else:
    st.info("No workouts logged yet! Use the sidebar to start logging.")

# Upload progress photos
st.subheader("Progress Photos")
uploaded_file = st.file_uploader("Upload a progress photo", type=["png", "jpg", "jpeg"])

if uploaded_file:
    st.image(uploaded_file, caption=f"Uploaded on {date.today()}", use_column_width=True)
    st.success("Photo uploaded successfully!")
