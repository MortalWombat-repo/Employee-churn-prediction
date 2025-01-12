#!/usr/bin/env python
# coding: utf-8

import requests


url = "http://localhost:9696/predict"

employee = {
    "department": "retail",
    "promoted": 0,
    "review": 0.514585,
    "projects": 4,
    "salary": "high",
    "tenure": 8.0,
    "satisfaction": 0.486957,
    "bonus": 1,
    "avg_hrs_month": 190.332987,
    "left": 0
}


response = requests.post(url, json=employee).json()
print(response)

if response["churn"] == True:
    print("employee churned")
    print(f"probability of churn {response["churn_probability"]}")
else:
    print("employee didn't churn")
    print(f"probability of churn {response["churn_probability"]}")