import Mysql
import datetime

current_time = str(datetime.datetime.now())
date = current_time.split(" ")[0]


run_days = Mysql.read_dates_from_database()
list_of_days = []
for each_day in run_days:
    day, = each_day
    list_of_days.append(day)

try:

    if date in list_of_days:
        pass

    else:
        List_Of_Users = Mysql.read_users_from_database()
        current_time = str(datetime.datetime.now())
        date = current_time.split(" ")[0]
        Mysql.write_date_to_database(date)
        for user in List_Of_Users:

            user_db, password_db, phone_number, email, days, token = user
            Mysql.update_user(token,int(days)-1)

except Exception as error:
        pass