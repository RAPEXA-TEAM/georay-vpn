import Mysql

try:

    print("\n[+] Wellcome to Georay-vpn mysql client...")
    print("[+] List of users : ")

    List_Of_Users = Mysql.read_users_from_database()
    counter = 1

    for user in List_Of_Users:

        user_db, password_db, phone_number, email, days, token = user
        print(f"[{counter}]",user_db, password_db, phone_number, email, days, token)
        counter += 1

    print("\n"+("."*60)+"\n")
    token = input("[+] Enter token for update : ")
    days = int(input("[+] Enter days for update : "))

    if Mysql.update_user(token.strip(),days):
        print(f"[+] Update user {token} expiration date to {days} \n")

    else : 
        print("[-] Error : connection with mysql server refused... \n")

except Exception as error:
        print(f"[-] Error : {error}\n")