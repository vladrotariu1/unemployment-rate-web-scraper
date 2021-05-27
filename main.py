from DB_controller import DataBaseController
from data_controller import *
import numpy as np
import pandas as pd
import sys
import time
import json


def populate_with_last_year_data():
    controller = DataBaseController()
    dates = get_last_n_monthly_updates(12)
    links = get_last_n_monthly_updates_links(12)
    link_index = 0

    for date in dates:
        df = get_monthly_data(links[link_index])[:-1]
        controller.insert_data(df, date[0], int(date[1]))
        link_index += 1

    return dates[0]


def populate_with_last_month_data():
    controller = DataBaseController()
    dates = get_last_n_monthly_updates(1)
    links = get_last_n_monthly_updates_links(1)

    df = get_monthly_data(links[0])[:-1]
    controller.insert_data(df, dates[0][0], int(dates[0][1]))

    return dates[0]


def get_app_props():
    with open("app-properties.json", "r") as jsonFile:
        data = json.load(jsonFile)
        jsonFile.close()

    return data


def new_update():
    data = get_app_props()
    last_update_data = get_last_n_monthly_updates(12)[0]

    if data['month'] == last_update_data[0] and data['year'] == last_update_data[1]:
        return False
    else:
        return True


def set_app_props(new_data):
    print(new_data)
    with open("app-properties.json", "r") as jsonFile:
        data = json.load(jsonFile)

    data["month"] = new_data[0]
    data["year"] = new_data[1]
    print(data)

    with open("app-properties.json", "w") as jsonFile:
        jsonFile.write(json.dumps(data))
        jsonFile.close()


def main():

    if len(sys.argv) > 1:
        if sys.argv[1] == 'populate':
            print('\n\nStarting to populate the database')
            populate_with_last_year_data()
            set_app_props(get_last_n_monthly_updates(1)[0])

    get_app_props()

    while True:
        print("Verifying incoming datasets")

        if new_update():
            print("New dataset found. Parsing data and inserting it into the database")
            populate_with_last_month_data()
            set_app_props(get_last_n_monthly_updates(1)[0])
        else:
            print("No new data..")
            time.sleep(3600)


if __name__ == '__main__':
    main()