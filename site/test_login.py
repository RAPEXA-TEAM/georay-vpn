import requests

base_url = "http://127.0.0.1:5550/"
user = "mmd" 
TokenID = "a1a"
password = 'mmd1' 

def ok(base_url,user,TokenID,password):
    print("[+] Test basic login Server start.")
    route = "/login"
    aa = {"user" : user , 'pass':password , "token" : TokenID}
    print(f"[+] Test basic login Server")
    r = requests.post(url = base_url+route, json=aa)
    print(f"[+] response : {r.text}")
    print("[+] Test basic login Server done.")

if __name__ == "__main__":
    ok(base_url,user,TokenID,password)
