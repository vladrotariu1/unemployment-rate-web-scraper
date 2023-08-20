import mysql.connector
from data_controller import get_counties_list


class DataBaseController:

    def __init__(self):
        self.mydb = mysql.connector.connect(
                host="localhost",
                user="user",
                password="password",
                database="unemployment_statistics"
            )

        self.cursor = self.mydb.cursor()

    def insert_counties(self):
        sql_statement = "INSERT INTO counties (county) VALUES (%s)"

        counties = get_counties_list()
        for county in counties:
            self.cursor.execute(sql_statement, (county,))

        self.mydb.commit()

    def insert_data(self, df, month, year):
        sql_statement = "INSERT INTO " \
                        "total_unemployment (" \
                        "month," \
                        "year," \
                        "county," \
                        "total," \
                        "women," \
                        "men," \
                        "under_25," \
                        "25_to_29," \
                        "30_to_39," \
                        "40_to_49," \
                        "50_to_55," \
                        "greater_55) " \
                        f"VALUES ('{month}', {year}, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

        print(sql_statement)
        for index, row in df.iterrows():
            self.cursor.execute(sql_statement, (
                index + 1,
                int(row[df.columns[1]].replace(' ', '').replace(',', '')),
                int(row[df.columns[2]].replace(' ', '').replace(',', '')),
                int(row[df.columns[3]].replace(' ', '').replace(',', '')),
                row[df.columns[4]],
                row[df.columns[5]],
                row[df.columns[6]],
                row[df.columns[7]],
                row[df.columns[8]],
                row[df.columns[9]]
            ))
            #print(int(row[df.columns[1]].replace(' ', '').replace(',', '')))

        self.mydb.commit()

