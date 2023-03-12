# #!/usr/bin/env

# #import libraries that are needed
# import Mysql
# import datetime

# # save the current date and time

# current_time = str(datetime.datetime.now())
# date = current_time.split(" ")[0]

# try:

#     # check if the current date is in the list of days to run expiration.py
    
#     date_db = Mysql.read_one_date_or_404_from_database(date)

#     if date_db != None:

#         pass

#     # if the current date is not in the list of days to run expiration.py
#     else:

#         List_Of_Users = Mysql.read_users_from_database()
#         Mysql.write_date_to_database(date)
#         for user in List_Of_Users:

#             user_db, password_db, phone_number, email, days, token, verify, Device, Device_OS = user
#             Mysql.update_user(token,int(days)-1)
        
#         # log it on flask
#         print(f"127.0.0.1 - - [{current_time}] \"Run Expiration.py HTTP/1.1\" 200 -")

# except Exception as error:
#         pass