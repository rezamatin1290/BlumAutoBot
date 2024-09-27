import requests
import time
import random
from urllib.parse import unquote
import threading
import json
import re
from autoplay import autoplay

# Headers
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

# Functions
def startFarm(Accname):
    print(f"[{Accname}] starting farm =>", end="")
    url = "https://game-domain.blum.codes/api/v1/farming/start"
    access_token = accounts[Accname]["access_token"]
    headers = defheader.copy()
    headers["authorization"] = access_token
    response = requests.post(url, headers=headers)
    print(" response: ", response)

def Claim_Farm(Accname):
    url = 'https://game-domain.blum.codes/api/v1/farming/claim'
    access_token = accounts[Accname]["access_token"]
    print(f"[{Accname}] => claim farming =>", end="")
    headers = defheader.copy()
    headers["authorization"] = access_token
    response = requests.post(url, headers=headers)
    print(" response: ", response)
    return response.json()

def solve(Accname, task: dict):
    access_token = accounts[Accname]["access_token"]
    headers = {
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'en-US,en;q=0.9',
        'authorization': f'{access_token}',
        'content-length': '0',
        'lang': 'en',
        'origin': 'https://telegram.blum.codes',
        'priority': 'u=1, i',
        'sec-ch-ua': '"Chromium";v="128", "Not;A=Brand";v="24", "Microsoft Edge";v="128", "Microsoft Edge WebView2";v="128"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36 Edg/128.0.0.0'
    }
    
    ignore_tasks = [
        "39391eb2-f031-4954-bd8a-e7aecbb1f192",  # wallet connect
        "d3716390-ce5b-4c26-b82e-e45ea7eba258",  # invite task
        "f382ec3f-089d-46de-b921-b92adfd3327a",  # invite task
        "220ee7b1-cca4-4af8-838a-2001cb42b813",  # invite task
        "5ecf9c15-d477-420b-badf-058537489524",  # invite task
        "c4e04f2e-bbf5-4e31-917b-8bfa7c4aa3aa",  # invite task
    ]
    task_id = task.get("id")
    if task_id in ignore_tasks:
        return
    task_title = task.get("title")
    task_status = task.get("status")

    start_task_url = f"https://earn-domain.blum.codes/api/v1/tasks/{task_id}/start"
    claim_task_url = f"https://earn-domain.blum.codes/api/v1/tasks/{task_id}/claim"
    _start = requests.post(start_task_url, headers=headers)

    time.sleep(5)
    _res = requests.post(claim_task_url, headers=headers)
    print(_res)

def find_not_finished_tasks(data):
    not_finished_tasks = []

    def traverse_tasks(tasks):
        for task in tasks:
            if task.get("status") != "FINISHED":
                not_finished_tasks.append(task)
            if "subTasks" in task:
                traverse_tasks(task["subTasks"])

    def traverse_sections(sections):
        for section in sections:
            if "tasks" in section:
                traverse_tasks(section["tasks"])
            if "subSections" in section:
                traverse_sections(section["subSections"])

    traverse_sections(data)
    return not_finished_tasks

def solve_task(Accname):
    url_task = "https://earn-domain.blum.codes/api/v1/tasks"
    access_token = accounts[Accname]["access_token"]
    headers = defheader.copy()
    headers["authorization"] = access_token
    res = requests.get(url_task, headers=headers)

    not_finished_tasks = find_not_finished_tasks(res.json())
    for task in not_finished_tasks:
        if any(keyword in task['title'].lower() for keyword in ["invite", "farm", "connect", "subTasks"]):
            continue
        if task['status'] == "READY_FOR_VERIFY":
            print(f"task <{task['title']}> need code to verify skipping, <{task['id']}>")
            continue
        print(f"start Task ID: {task['id']}, Title: {task['title']}, Status: {task['status']}")
        solve(Accname, task)

def getdailyreward(Accname):
    print(f"[{Accname}] getting Daily reward => ", end="")
    url = 'https://game-domain.blum.codes/api/v1/daily-reward?offset=-210'
    access_token = accounts[Accname]["access_token"]
    headers = defheader.copy()
    headers["authorization"] = access_token
    response_get = requests.get(url, headers=headers)
    response_js = response_get.json()
    if response_js.get('days'):
        print(f"[{Accname}] => daily reward: {response_js}")
        response = requests.post(url, headers=headers)
    else:
        print(f"[{Accname}] => daily reward not found: {response_js}")

def user_balance(Accname):
    url = "https://game-domain.blum.codes/api/v1/user/balance"
    access_token = accounts[Accname]["access_token"]
    headers = defheader.copy()
    headers["authorization"] = access_token
    response = requests.get(url, headers=headers)
    print(f"[{Accname}] => user balance: {response.json()}")
    return response.json()

def Login(Accname):
    print("Logging into Account", Accname)
    url = "https://user-domain.blum.codes/api/v1/auth/provider/PROVIDER_TELEGRAM_MINI_APP"
    global accounts
    auth_url = accounts[Accname]["auth_url"]
    if "https://telegram.blum.codes" in auth_url:
        auth_url = auth_url.replace("https://telegram.blum.codes/#tgWebAppData=", "")
    decode_data = unquote(string=unquote(string=auth_url.split('&tgWebAppVersion')[0]))
    json_data = {"query": decode_data}
    response = requests.post(url, json=json_data)
    response_json = response.json()
    ref_token = response_json.get("token").get("refresh")
    access_token = "Bearer " + response_json.get("token").get("access")
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
            if not accounts.get(acc_name).get("Login"):
                Login(acc_name)
                
            if user_d.get("message") == "Invalid jwt token":
                print("Invalid Token, refreshing token")
                Login(acc_name)
                user_d = user_balance(acc_name)

            user_d = user_balance(acc_name)
            if config.get("auto_complete_task"):
                solve_task(acc_name)


            time.sleep(random.uniform(6, 10))
            getdailyreward(acc_name)

            timestamp = user_d.get("timestamp", None)
            farmingtime = user_d.get("farming", None)
            end_time = farmingtime.get("endTime", None) if farmingtime else None

            if (user_d.get("farming", None) is None) or (timestamp and end_time and timestamp >= end_time):
                if user_d.get("message") == "Invalid jwt token":
                    print("Invalid Token, refreshing token")
                    Login(acc_name)
                Claim_Farm(acc_name)
                time.sleep(random.uniform(60, 3 * 60))
                startFarm(acc_name)
                time.sleep(random.uniform(60, 2 * 60))
                getdailyreward(acc_name)
                time.sleep(random.uniform(10 * 60, 15 * 60))
                user_d = user_balance(acc_name)
                timestamp = user_d.get("timestamp", None)
            elif end_time and timestamp < end_time:
                time_to_farm = (end_time // 1000) - (timestamp // 1000)
                hour = time_to_farm // 3600
                minute = (time_to_farm - (hour * 3600)) // 60
                second = time_to_farm - (hour * 3600) - (minute * 60)
                card_number = user_d.get("playPasses")
                if card_number > 0 and config.get("auto_play_game"):
                    iter = min(card_number, random.uniform(max(1, card_number - 3), min(10, card_number)))
                    autoplay(accounts, acc_name, iter, config.get("game_point").get("low"), config.get("game_point").get("high"))
                print(f"account: {acc_name}, Balance: {user_d.get('availableBalance')}, Card Number: {user_d.get('playPasses')}, End time of farming in {hour} hour, {minute} minute, {second} seconds")
                Delay = random.uniform(time_to_farm + 1, time_to_farm + (6 * 60))
                print(f"adding random time to sleep {Delay} seconds")
                time.sleep(Delay)
                Login(acc_name)
            else:
                print(f"[{acc_name}] => unknown condition!")
                print(f"[{acc_name}] user reported balance json: ", user_d)
        except Exception as e:
            print(f"error => {e}")
            user_d = user_balance(acc_name)
            continue

def start_threads():
    threads = []
    for acc in accounts.keys():
        process = threading.Thread(target=main, args=(acc,))
        threads.append(process)
        process.start()
        time.sleep(10)
    for p in threads:
        p.join()

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
            "Login": False,
        }
    main(name)
