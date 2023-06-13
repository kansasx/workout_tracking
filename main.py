import requests
import os
from datetime import datetime as dt


sheety_end_point = os.environ.get("SHEETYENDPOINT")
token = os.environ.get("TOKEN")

sheety_headers = {
        "Authorization": token,
        "Content-Type": "application/json"
    }


def get_data_from_text() -> list:
    """
    the function receives plain information and
     returns a json data using the nutritionix exercise API
    :return:
    """
    nutrition_key = os.environ.get("NUTRIKEY")
    nutri_id = os.environ.get("NUTRIID")

    url = "https://trackapi.nutritionix.com/v2/natural/exercise"
    activity = input("what activity did you engaged in today\n")

    headers = {
        "x-app-id": nutri_id,
        "x-app-key": nutrition_key}

    body = {
        "query": activity
    }

    data = requests.post(url=url, headers=headers, json=body).json()
    print(data)
    activities = data["exercises"]
    return activities


def get_sheet_data():
    """
    retrieves all records from a google sheet
    :return:
    """
    response = requests.get(sheety_end_point, headers=sheety_headers)
    response.raise_for_status()
    data = response.json()
    print(data)


def create_records(actions: list):
    """
    populates a google sheet with a recoord
    :param actions:
    :return:
    """
    date = dt.today().strftime('%d/%m/%Y')
    time_ = dt.today().strftime('%H:%M:%S')
    for activity in actions:
        exercise = activity["name"]
        time = activity["duration_min"]
        calories_burnt = activity["nf_calories"]

        request_body = {
            "workout": {"date": date,
                        "time": time_,
                        "exercise": exercise,
                        "duration": time,
                        "calories": calories_burnt,
                        }
        }
        response = requests.post(sheety_end_point, json=request_body, headers=sheety_headers)
        response.raise_for_status()
        print(response.text)

# uncomment the functions to get started
# nutri_response = get_data_from_text()
# get_sheet_data()
# create_records(nutri_response)