import requests
import time
import random
from urllib.parse import unquote
import threading
import logging
from config import *
import threading

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")





token_header = {
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'en-US,en;q=0.9',
        'cache-control': 'no-cache',
        'content-type': 'application/json',
        'origin': 'https://telegram.blum.codes',
        'pragma': 'no-cache',
        'priority': 'u=1, i',
        'sec-ch-ua': '"Chromium";v="128", "Not;A=Brand";v="24", "Microsoft Edge";v="128", "Microsoft Edge WebView2";v="128"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36 Edg/128.0.0.0'
    }

defheader = {
            "accept": "application/json, text/plain, */*",
            "accept-language": "en-US,en;q=0.9",
            "origin": "https://telegram.blum.codes",
            "authorization": "",
            "priority": "u=1, i",
            "sec-ch-ua": '"Chromium";v="128", "Not;A=Brand";v="24", "Microsoft Edge";v="128", "Microsoft Edge WebView2";v="128"',
            "sec-ch-ua-platform": "Windows",
            "sec-ch-ua-mobile": "?0",
            "user-agent": "Mozilla/5.0 (Linux; Android 15; SM-A102U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.6613.127 Mobile Safari/537.36",
            "sec-fetch-site": "same-site",
            "sec-fetch-mode": "cors",
            "sec-fetch-dest": "empty"
            }




def startFarm(Accname):
    print(f"[{Accname}]starting farm =>", end = "")
    url = "https://game-domain.blum.codes/api/v1/farming/start"
    access_token = accounts[Accname]["access_token"] 

    headers = defheader
    headers["authorization"] = access_token


    response = requests.post(url, headers = headers)
    print(" reponse: ", response)
 


def Claim_Farm(Accname):
    url = 'https://game-domain.blum.codes/api/v1/farming/claim'
    access_token = accounts[Accname]["access_token"] 
    print (f"[{Accname}]=>claim farming=>", end="")

    headers = defheader
    headers["authorization"] = access_token

    response = requests.post(url, headers = headers)

    print(" response : ", response)

    return response.json()



def getdailyreward(Accname):
    print(f"[{Accname}] getting Daily reward=> ",end="")
    url = 'https://game-domain.blum.codes/api/v1/daily-reward?offset=-210'

    access_token = accounts[Accname]["access_token"] 
    headers = defheader
    headers["authorization"] = access_token
    response_get = requests.get(url, headers=headers)
    response_js = response_get.json()
    if response_js.get('days'):
        print (f"[{Accname}] => daily reward  : {response_js}")


        response = requests.post(url, headers = headers)
    else:
        print (f"[{Accname}] => daily reward not found  : {response_js}")
         





def user_balance(Accname):

    url = "https://game-domain.blum.codes/api/v1/user/balance"

    access_token = accounts[Accname]["access_token"] 

    headers = defheader
    headers["authorization"] = access_token

    response = requests.get(url, headers = headers)

    print (f"[{Accname}] => user balance  : {response.json()}")

    return response.json()




def Login(Accname):
    #tg_web_data
    print("Loging to Account" , Accname)


    url = "https://user-domain.blum.codes/api/v1/auth/provider/PROVIDER_TELEGRAM_MINI_APP"
    global accounts
    auth_url = accounts[Accname]["auth_url"]
    decode_data = unquote(string=unquote(string=auth_url.split('tgWebAppData=')[1].split('&tgWebAppVersion')[0]))

    json_data = {"query" : decode_data}
    response = requests.post(url, json=json_data)
    response_json = response.json()

    ref_token = response_json.get("token").get("refresh")
    access_token = "Bearer " + (response_json).get("token").get("access")
    accounts[Accname]["access_token"] = access_token
    accounts[Accname]["refresh_token"] = ref_token
    accounts[Accname]["Login"] = True

    return ref_token, access_token



def refreshToken(Accname):
    global accounts

    ref_token = accounts[Accname]["refresh_token"]
    refresh_payload = {"refresh": ref_token}

    response = requests.post("https://user-domain.blum.codes/api/v1/auth/refresh", json=refresh_payload)

    if response.ok:
        data = response.json()
        new_access_token = data.get("access")
        new_refresh_token = data.get("refresh")

        if new_access_token:
            accounts[Accname]["refresh_token"] = new_refresh_token
            accounts[Accname]["access_token"] = new_access_token

            print("Token refreshed successfully")


        else:
            print("New access token not found in the response")


    else:
        print("Failed to refresh the token")




def main(acc_name):
        while True:

            try:
                if not accounts.get(acc_name).get("Login"):
                    token = Login(acc_name)

                user_d = user_balance(acc_name)

                if user_d.get("message") == "Invalid jwt token":
                    print("Invalid Token refresh token")


                    Login(acc_name)
                    user_d = user_balance(acc_name)

                
                    
                time.sleep(23)
                getdailyreward(acc_name)
                
                timestamp = user_d.get("timestamp", None)
                
                farmingtime = user_d.get("farming", None)

                if farmingtime:
                    end_time = farmingtime.get("endTime", None)
                else:
                    end_time = None

                if (user_d.get("farming", None) is None) or ((timestamp) and (end_time) and (timestamp >= end_time)):
                    if user_d.get("message") == "Invalid jwt token":
                        print("Invalid Token refresh token")


                        Login(acc_name)
                    
                    claim = Claim_Farm(acc_name)
                    time.sleep(random.randint(60, 3*60))

                    startFarm(acc_name)
                    time.sleep(random.randint(60, 2*60))
                    
                    getdailyreward(acc_name)
                    time.sleep(random.randint(10 * 60, 15 * 60))
                    user_d = user_balance(acc_name)
                    timestamp = user_d.get("timestamp", None)


    
                elif (end_time) and (timestamp < end_time):
                    time_to_farm = ((end_time//1000) - (timestamp//1000))
                    hour = time_to_farm // 3600
                    minute = (time_to_farm - (hour * 3600)) // 60
                    second = (time_to_farm) - (hour * 3600) - (minute * 60)
                    print(f"account :{acc_name} , Balance : {user_d.get('availableBalance')}, Card Number : {user_d.get('playPasses')}, End time of farming in {hour} hour, {minute} minute, {second} seconds")
                    time_to_farm = ((end_time//1000) - (timestamp//1000))
                    Delay = random.randint(time_to_farm + 1, time_to_farm + (6 * 60))
                    print(f"adding random time to sleep {Delay} seconds")
                    time.sleep(Delay)
                    Login(acc_name)
                
                else:
                    print(f"[{acc_name}] => unknow condition!")
    
                    print(f"[{acc_name}]user reported balance json: ", user_d)



            except Exception as e:
                    
                    print(f"error =>{e}")
                    

                    user_d = user_balance(acc_name)
                    continue

def start_threads():


    threads = []
    for acc in accounts.keys():
        process = threading.Thread(target=main, args=(acc,))
        threads.append(process)
        process.start()
        time.sleep(random.randint(60, 2*60))

    for p in threads:
        p.join()

if __name__ == "__main__":
    print("Development By Reza")
    start_threads()