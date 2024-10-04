import requests
import time
import random
from urllib.parse import unquote
import threading
import json
import re
from autoplay import autoplay


default_header = {

default_header = {
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

def send_request(acc_name, url, method, headers, data = None):
    access_token = (accounts.get(acc_name)).get("access_token")
    headers.update({
        'authorization': access_token
    })

    method = method.upper()
    if method == "POST":
        if data:
            response = requests.post(url, headers=headers, data=data)
        else:
            response = requests.post(url, headers=headers)
    elif method == "GET":
        response = requests.get(url, headers=headers)
    return response

def startFarm(acc_name):
    print(f"[{acc_name}] starting farm =>", end="")

def send_request(acc_name, url, method, headers, data = None):
    access_token = (accounts.get(acc_name)).get("access_token")
    headers.update({
        'authorization': access_token
    })

    method = method.upper()
    if method == "POST":
        if data:
            response = requests.post(url, headers=headers, data=data)
        else:
            response = requests.post(url, headers=headers)
    elif method == "GET":
        response = requests.get(url, headers=headers)
    return response

def startFarm(acc_name):
    print(f"[{acc_name}] starting farm =>", end="")

    url = "https://game-domain.blum.codes/api/v1/farming/start"
    response = send_request(acc_name, url, "POST", default_header.copy) 

    response = send_request(acc_name, url, "POST", default_header.copy) 

    print(" response: ", response)

def claim_farm(acc_name):
    print(f"[{acc_name}] => Claim Farm =>", end="")
def claim_farm(acc_name):
    print(f"[{acc_name}] => Claim Farm =>", end="")
    url = 'https://game-domain.blum.codes/api/v1/farming/claim'

    response = send_request(acc_name, url, "POST", default_header.copy)
    print("response: ", response)

    response = send_request(acc_name, url, "POST", default_header.copy)
    print("response: ", response)
    return response.json()

def get_daily_reward(acc_name):
    print(f"[{acc_name}] getting Daily reward => ", end="")
    url = 'https://game-domain.blum.codes/api/v1/daily-reward?offset=-210'

    response_get = send_request(acc_name, url, "GET", default_header)

    response_get = send_request(acc_name, url, "GET", default_header)
    response_js = response_get.json()
    if response_js.get('days'):
        print(f"[{acc_name}] => daily reward: {response_js}")
        response =send_request(acc_name, url, "GET", default_header)
        print(f"[{acc_name}] => daily reward: {response_js}")
        response =send_request(acc_name, url, "GET", default_header)
    else:
        print(f"[{acc_name}] => daily reward not found: {response_js}")
        print(f"[{acc_name}] => daily reward not found: {response_js}")

def user_balance(acc_name):
def user_balance(acc_name):
    url = "https://game-domain.blum.codes/api/v1/user/balance"
    response = send_request(acc_name, url, "GET", default_header)

    print(f"[{acc_name}] => user balance: {response.json()}")
    response = send_request(acc_name, url, "GET", default_header)

    print(f"[{acc_name}] => user balance: {response.json()}")
    return response.json()

def login(acc_name):
    print("Logging into Account", acc_name)
def login(acc_name):
    print("Logging into Account", acc_name)
    url = "https://user-domain.blum.codes/api/v1/auth/provider/PROVIDER_TELEGRAM_MINI_APP"
    global accounts
    auth_url = (accounts.get(acc_name)).get("auth_url")
    
    auth_url = (accounts.get(acc_name)).get("auth_url")
    
    if "https://telegram.blum.codes" in auth_url:
        auth_url = auth_url.replace("https://telegram.blum.codes/#tgWebAppData=", "")
    decode_data = unquote(string=unquote(string=auth_url.split('&tgWebAppVersion')[0]))


    json_data = {"query": decode_data}
    response = requests.post(url, json=json_data)
    response_json = response.json()


    ref_token = response_json.get("token").get("refresh")
    access_token = "Bearer " + response_json.get("token").get("access")
    
    accounts[acc_name].update({
        "access_token": access_token,
        "refresh_token": ref_token,
        "login": True
    })
    
    accounts[acc_name].update({
        "access_token": access_token,
        "refresh_token": ref_token,
        "login": True
    })
    return ref_token, access_token

def refreshToken(acc_name):
def refreshToken(acc_name):
    global accounts
    ref_token = accounts[acc_name]["refresh_token"]

    refresh_payload = {
        "refresh": ref_token
    }

    response = requests.post(
        "https://user-domain.blum.codes/api/v1/auth/refresh",
        json=refresh_payload
    )
    
    ref_token = accounts[acc_name]["refresh_token"]

    refresh_payload = {
        "refresh": ref_token
    }

    response = requests.post(
        "https://user-domain.blum.codes/api/v1/auth/refresh",
        json=refresh_payload
    )
    
    if response.ok:
        data = response.json()
        new_access_token = data.get("access")
        new_refresh_token = data.get("refresh")


        if new_access_token:
            accounts[acc_name].update({
                "refresh_token": new_refresh_token,
                "access_token": new_access_token
            })
            accounts[acc_name].update({
                "refresh_token": new_refresh_token,
                "access_token": new_access_token
            })
            print("Token refreshed successfully")
        else:
            print("New access token not found in the response")
    else:
        print("Failed to refresh the token")

def read_from_file():
    with open("url.txt", "r") as f:
        return f.readlines()

def main(acc_name):
    while True:
        try:
            with open("config.json", 'r') as file:
                config = json.load(file)
        except Exception as e:
            print("Failed to read config.json or file does not exist.")
            exit(1)

        try:
            if not accounts.get(acc_name).get("login"):
                login(acc_name)
            user_data = user_balance(acc_name)
            
            if user_data.get("message") == "Invalid jwt token":
            if not accounts.get(acc_name).get("login"):
                login(acc_name)
            user_data = user_balance(acc_name)
            
            if user_data.get("message") == "Invalid jwt token":
                print("Invalid Token, refreshing token")
                login(acc_name)
                user_data = user_balance(acc_name)
                login(acc_name)
                user_data = user_balance(acc_name)

            time.sleep(random.uniform(6, 10))
            get_daily_reward(acc_name)
            get_daily_reward(acc_name)

            timestamp = user_data.get("timestamp", None)
            farmingtime = user_data.get("farming", None)
            timestamp = user_data.get("timestamp", None)
            farmingtime = user_data.get("farming", None)
            end_time = farmingtime.get("endTime", None) if farmingtime else None

            if (user_data.get("farming", None) is None) or (timestamp and end_time and timestamp >= end_time):
                claim_farm(acc_name)
            if (user_data.get("farming", None) is None) or (timestamp and end_time and timestamp >= end_time):
                claim_farm(acc_name)
                time.sleep(random.uniform(60, 3 * 60))
                startFarm(acc_name)
                time.sleep(random.uniform(60, 2 * 60))
                get_daily_reward(acc_name)
                get_daily_reward(acc_name)
                time.sleep(random.uniform(10 * 60, 15 * 60))

                user_data = user_balance(acc_name)
                timestamp = user_data.get("timestamp", None)


                user_data = user_balance(acc_name)
                timestamp = user_data.get("timestamp", None)

            elif end_time and timestamp < end_time:
                time_to_farm = (end_time // 1000) - (timestamp // 1000)
                hour = time_to_farm // 3600
                minute = (time_to_farm - (hour * 3600)) // 60
                second = time_to_farm - (hour * 3600) - (minute * 60)

                card_number = user_data.get("playPasses")

                card_number = user_data.get("playPasses")
                if card_number > 0 and config.get("auto_play_game"):
                    if card_number <= 3:
                        iter = card_number
                    elif card_number > 3:
                        iter = random.randint(card_number - 3, card_number)
                        if iter > 10:
                            iter = random.randint(7, 10)

                    autoplay(
                        accounts, acc_name, iter,
                        config.get("game_point").get("low"),
                        config.get("game_point").get("high")
                    )

                print(
                      f"account: {acc_name}, Balance: {user_data.get('availableBalance')},"
                      f" Card Number: {user_data.get('playPasses')}", 
                      f"End time of farming in {hour} hour, {minute} minute, {second} seconds"
                )
                delay = random.uniform(time_to_farm + 1, time_to_farm + (6 * 60))
                print(f"adding random time to sleep {delay} seconds")
                time.sleep(delay)
                login(acc_name)
                    if card_number <= 3:
                        iter = card_number
                    elif card_number > 3:
                        iter = random.randint(card_number - 3, card_number)
                        if iter > 10:
                            iter = random.randint(7, 10)

                    autoplay(
                        accounts, acc_name, iter,
                        config.get("game_point").get("low"),
                        config.get("game_point").get("high")
                    )

                print(
                      f"account: {acc_name}, Balance: {user_data.get('availableBalance')},"
                      f" Card Number: {user_data.get('playPasses')}", 
                      f"End time of farming in {hour} hour, {minute} minute, {second} seconds"
                )
                delay = random.uniform(time_to_farm + 1, time_to_farm + (6 * 60))
                print(f"adding random time to sleep {delay} seconds")
                time.sleep(delay)
                login(acc_name)
            else:
                print(f"[{acc_name}] => unknown condition!")
                print(f"[{acc_name}] user reported balance json: ", user_data)
                print(f"[{acc_name}] user reported balance json: ", user_data)
        except Exception as e:
            print(f"error => {e}")
            user_data = user_balance(acc_name)
            user_data = user_balance(acc_name)
            continue

def start_threads():
    threads = []
    for acc in accounts.keys():
        process = threading.Thread(target=main, args=(acc,))
        threads.append(process)
        process.start()
        time.sleep(random.uniform(10, 20))

    for thread in threads:
        thread.join()
        time.sleep(random.uniform(10, 20))

    for thread in threads:
        thread.join()

if __name__ == "__main__":
    print("Development By Reza")
    accounts = {}
    links = read_from_file()


    if not links or links[0].strip() == "":
        print("please insert your link in url.txt")
        exit()


    for x in links:
        x = x.strip()
        decode_data = unquote(string=unquote(string=x.split('&tgWebAppVersion')[0]))
        match = re.search(r'"id":(\d+)', decode_data)
        name = re.search(r'"first_name":"(.*?)"', decode_data)


        if match:
            user_id = match.group(1)
            name = name.group(1) if name else user_id
            name = f"{user_id} {name}"
            accounts[name] = {
                "auth_url": decode_data,
                "access_token": "",
                "refresh_token": "refresh_token",
                "login": False,
            }
            name = f"{user_id} {name}"
            accounts[name] = {
                "auth_url": decode_data,
                "access_token": "",
                "refresh_token": "refresh_token",
                "login": False,
            }
    start_threads()
