import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Student Performance Dashboard",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Student Performance Dashboard")
st.write("SWYNEX Internship - Task 3: Interactive Dashboard")

# Load dataset
df = pd.read_csv("cleaned_student.csv")

# Clean column names
df.columns = df.columns.str.strip()

# Convert numeric columns
df["Age"] = pd.to_numeric(df["Age"], errors="coerce")
df["Marks"] = pd.to_numeric(df["Marks"], errors="coerce")

# Sidebar filters
st.sidebar.header("Dashboard Filters")

departments = ["All"] + sorted(
    df["Department"].dropna().astype(str).unique().tolist()
)

selected_department = st.sidebar.selectbox(
    "Select Department",
    departments
)

filtered_df = df.copy()

if selected_department != "All":
    filtered_df = filtered_df[
        filtered_df["Department"] == selected_department
    ]

if filtered_df.empty:
    st.warning("No students found for this filter.")
    st.stop()

# KPI cards
col1, col2, col3 = st.columns(3)

col1.metric("Total Students", len(filtered_df))

average_marks = filtered_df["Marks"].mean()
col2.metric(
    "Average Marks",
    f"{average_marks:.2f}" if pd.notna(average_marks) else "N/A"
)

average_age = filtered_df["Age"].mean()
col3.metric(
    "Average Age",
    f"{average_age:.1f}" if pd.notna(average_age) else "N/A"
)

st.divider()

# Charts
left, right = st.columns(2)

with left:
    st.subheader("Marks Distribution")
    marks_data = filtered_df.dropna(subset=["Marks"])
    fig1 = px.histogram(
        marks_data,
        x="Marks",
        nbins=10,
        title="Distribution of Student Marks"
    )
    st.plotly_chart(fig1, use_container_width=True)

with right:
    st.subheader("Average Marks by Department")
    dept_marks = filtered_df.groupby(
        "Department", as_index=False
    )["Marks"].mean()

    fig2 = px.bar(
        dept_marks,
        x="Department",
        y="Marks",
        title="Department-wise Average Marks"
    )
    st.plotly_chart(fig2, use_container_width=True)

left2, right2 = st.columns(2)

with left2:
    st.subheader("Age Distribution")
    age_data = filtered_df.dropna(subset=["Age"])
    fig3 = px.histogram(
        age_data,
        x="Age",
        title="Student Age Distribution"
    )
    st.plotly_chart(fig3, use_container_width=True)

with right2:
    st.subheader("Age vs Marks")
    scatter_data = filtered_df.dropna(
        subset=["Age", "Marks"]
    )
    fig4 = px.scatter(
        scatter_data,
        x="Age",
        y="Marks",
        hover_name="Name",
        title="Relationship Between Age and Marks"
    )
    st.plotly_chart(fig4, use_container_width=True)

st.subheader("Student Data")
st.dataframe(filtered_df, use_container_width=True)

st.caption("SWYNEX Internship | Task 3")