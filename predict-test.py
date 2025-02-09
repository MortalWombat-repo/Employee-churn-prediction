#!/usr/bin/env python
# coding: utf-8

import requests
from colorama import Fore, Back, Style
import pandas as pd
import streamlit as st
import sys
import warnings

# Check if running in Streamlit mode
is_streamlit = "streamlit" in sys.modules

# Suppress Streamlit warnings if running in terminal mode
if not is_streamlit:
    warnings.filterwarnings("ignore", category=UserWarning, module="streamlit")

url = "http://localhost:9696/predict"

# employee churn status
employee_status = None

# Inital default values
employee = {
    "department": "operations",
    "promoted": 0,
    "review": 0.577569,
    "projects": 3,
    "salary": "low",
    "tenure": 5.0,
    "satisfaction": 0.626759,
    "bonus": 0,
    "avg_hrs_month": 180.866070
}

# """Streamlit"""
# st.image('img/image.png')
st.title("Employee churn prediction")
st.sidebar.title("Employee parameters")
st.sidebar.header("Use arrow buttons on sliders for maximum precision")
# Add a horizontal line (line break)
# st.sidebar.markdown("**____________________________________**")


st.sidebar.markdown("Departments")
# Selectbox
department = st.sidebar.selectbox(
    "What department does the employee belong to?",
    (
        "sales",
        "retail",
        "operations",
        "engineering",
        "marketing",
        "support",
        "admin",
        "finance",
        "logistics",
        "IT",
    ),
    index=1, # zero indexed
    placeholder="Select the department...",
    key="department",
)


st.sidebar.markdown("Promoted status")
# Pill selection
options = ["Yes", "No"]
promoted = st.sidebar.pills(
    "Was the employee promoted in the last 24 months?", options, default="No", key="promoted"
)


st.sidebar.markdown("Review grade employee got")
# Slider with plus/minus buttons
review = st.sidebar.slider(
    label="Select a value between 0.01 and 1.0",  # Label for the slider
    min_value=0.01,  # Minimum allowed value
    max_value=1.0,  # Maximum allowed value
    value=0.514585,  # Default value
    step=0.01,  # Step size for increments
    key="review",
)


st.sidebar.markdown("How many projects employee is in")
# Slider with plus/minus buttons
projects = st.sidebar.slider(
    label="Select a value 1 and 5",  # Label for the slider
    min_value=1,  # Minimum allowed value
    max_value=5,  # Maximum allowed value
    value=4,  # Default value
    step=1,  # Step size for increments
    key="projects",
)


st.sidebar.markdown("Tier of the employees salary")
# Selectbox
salary = st.sidebar.selectbox(
    "Select the tier of the employees salary?",
    (
        "low",
        "medium",
        "high",
    ),
    index=2,
    placeholder="Select the salary tier...",
    key="salary",
)


st.sidebar.markdown("Number of years employee has been at the company")
# Slider with plus/minus buttons
tenure = st.sidebar.slider(
    label="Select a value between 1 and 12",  # Label for the slider
    min_value=1.0,  # Minimum allowed value
    max_value=12.0,  # Maximum allowed value
    value=8.0,  # Default value
    step=0.1,  # Step size for increments
    key="tenure",
)


st.sidebar.markdown("Rating of employees satisfaction from surveys")
# Slider with plus/minus buttons
satisfaction = st.sidebar.slider(
    label="Select a value between 0.0 and 1.0",  # Label for the slider
    min_value=0.0,  # Minimum allowed value
    max_value=1.0,  # Maximum allowed value
    value=0.486957,  # Default value
    step=0.1,  # Step size for increments
    key="satisfaction",
)


st.sidebar.markdown("Bonus status")
# Pill selection
options = ["Yes", "No"]
bonus = st.sidebar.pills(
    "Has the employee received a bonus in the last 24 months?", options, default="Yes", key="bonus"
)


st.sidebar.markdown("Avg hours of work per month by the employee")
# Slider with plus/minus buttons
avg_hrs_month = st.sidebar.slider(
    label="Select a value between 171.0 and 201.0",  # Label for the slider
    min_value=171.0,  # Minimum allowed value
    max_value=201.0,  # Maximum allowed value
    value=190.332987,  # Default value
    step=0.1,  # Step size for increments
    key="avg_hrs_month",
)

# initialize the dictionary with the values
employee["department"] = department
# Convert "Yes"/"No" to 1/0
employee["promoted"] = 1 if promoted == "Yes" else 0
employee["review"] = review
employee["projects"] = projects
employee["salary"] = salary
employee["tenure"] = tenure
employee["satisfaction"] = satisfaction
# Convert "Yes"/"No" to 1/0
employee["bonus"] = 1 if bonus == "Yes" else 0
employee["avg_hrs_month"] = avg_hrs_month

#
#response = requests.post(url, json=employee).json()
#print(response)
#
#if response["churn"]:
#    print("employee churned")
#    print(f"probability of churn {response['churn_probability']}")
#else:
#    print("employee didn't churn")
#    print(f"probability of churn {response['churn_probability']}")


# """Main menu"""

# a trick for centering but it impacts the overall aesthetic as the title cant be centered without wrapping
#left_co, cent_co,last_co = st.columns(3)
#with cent_co:

st.image("img/employees.png") #caption=""

#st.write("**Parameters chosen:**")
st.header(":gear: Parameters chosen: ")

# Convert dictionary to DataFrame
df = pd.DataFrame(employee.items(), columns=["Feature", "Value"])

# Reset index does not work unfortunately, keeping this for future reference
#df = df.reset_index(drop=True)

# Convert all values to strings, it only displays the value, there is no difference to the user
df["Value"] = df["Value"].astype(str)

# Display as a dataframe (interactive and sortable) and hide the index
st.dataframe(df, use_container_width=True, hide_index=True)

# ""Streamlit Logic"""
if st.button("Predict Employee status"):
    response = requests.post(url, json=employee).json()
    employee_churn_status = response["churn"]
    employee_churn_status_probability = response['churn_probability']

    match employee_churn_status:
        case False:
            employee_churn_status = "Not churn"
            st.write("")
            st.markdown(f"### The employee is suspected to :green[**{employee_churn_status}**] :smile:", unsafe_allow_html=True)
            st.markdown(f"### With the probability of {employee_churn_status_probability:.3f}")
            st.markdown("#### No action needed.")
            st.image("img/employees_not_churned.png")
        case True:
            employee_churn_status = "Churn"
            st.write("")
            st.markdown(f"### The employee is suspected to :red[**{employee_churn_status}**] :pensive:", unsafe_allow_html=True)
            st.markdown(f"### With the probability of {employee_churn_status_probability:.3f}")
            st.markdown("#### Further action needed.")
            st.image("img/employees_churned.png")


# """Terminal logic"""
response = requests.post(url, json=employee).json()

employee_churn_status = response["churn"]
employee_churn_status_probability = response['churn_probability']

match employee_churn_status:
    case False:
        employee_churn_status = "Not churn"
        print(f"The employee is suspected to {Back.GREEN}{employee_churn_status}{Style.RESET_ALL} 😊")
        print(f"With the probability of {employee_churn_status_probability:.3f}")
        print("No action needed.")
    case True:
        employee_churn_status = "Churn"
        print(f"The employee is suspected to {Back.RED}{employee_churn_status}{Style.RESET_ALL} 😔")
        print(f"With the probability of {employee_churn_status_probability:.3f}")
        print("Further action needed.")