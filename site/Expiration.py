#!/usr/bin/env

#import libraries that are needed
import Mysql
import datetime

# save the current date and time

current_time = str(datetime.datetime.now())
date = current_time.split(" ")[0]

# read dates that run expiration.py from the database

run_days = Mysql.read_dates_from_database()
list_of_days = []
for each_day in run_days:
    day, = each_day
    list_of_days.append(day)

try:

    # check if the current date is in the list of days to run expiration.py
    if date in list_of_days:
        pass

    # if the current date is not in the list of days to run expiration.py
    else:
        List_Of_Users = Mysql.read_users_from_database()
        current_time = str(datetime.datetime.now())
        date = current_time.split(" ")[0]
        Mysql.write_date_to_database(date)
        for user in List_Of_Users:

            user_db, password_db, phone_number, email, days, token, verify, Device, Device_OS = user
            Mysql.update_user(token,int(days)-1)
        
        # log it on flask
        print(f"127.0.0.1 - - [{current_time}] \"Run Expiration.py HTTP/1.1\" 200 -")

except Exception as error:
        pass