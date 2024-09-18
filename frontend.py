"""
a program that users the blum card

account link, number of card for used
show number of card, start


show: 
    number of cards


"""

from tkinter import *
import requests
import time
import random
from urllib.parse import unquote
import threading
import asyncio
import json
import logging
import urllib3
import re

urllib3.disable_warnings()



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


def Login(Accname):
    #tg_web_data
    print("Loging to Account" , Accname)
    accounts = read_accounts()

    url = "https://user-domain.blum.codes/api/v1/auth/provider/PROVIDER_TELEGRAM_MINI_APP"
    
    auth_url = accounts[Accname]["auth_url"]
    decode_data = unquote(string=unquote(string=auth_url.split('tgWebAppData=')[1].split('&tgWebAppVersion')[0]))

    json_data = {"query" : decode_data}
    response = requests.post(url, json=json_data)
    response_json = response.json()
    print(response_json)
    ref_token = response_json.get("token").get("refresh")
    access_token = "Bearer " + (response_json).get("token").get("access")
    accounts[Accname]["access_token"] = access_token
    accounts[Accname]["refresh_token"] = ref_token
    accounts[Accname]["Login"] = True
    save_accounts(accounts)
    
    return ref_token, access_token



def make_requests_async(authorization_token, points, iteration):
    proxy = None
    max_retries = 4
    retry_delay = 2  # seconds
    attempt = 0
    while attempt < max_retries:
        try:
            time.sleep(0.5)
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0",
                "Accept": "application/json, text/plain, */*",
                "accept-language": "en-US,en;q=0.9",
                "authorization": authorization_token,
                "origin": "https://telegram.blum.codes",
                "priority": "u=1, i",
                "sec-ch-ua": "\"Microsoft Edge\";v=\"125\", \"Chromium\";v=\"125\", \"Not.A/Brand\";v=\"24\", \"Microsoft Edge WebView2\";v=\"125\"",
                "sec-fetch-dest": "empty",
                "sec-fetch-mode": "cors",
                "sec-fetch-site": "same-site"
            }

            response = requests.post('https://game-domain.blum.codes/api/v1/game/play', headers=headers, proxies=proxy, verify=False)
            if response.status_code == 401:
                print("Token expired. Please enter a valid authorization token.")
                return f"Iteration {iteration} failed."
            elif response.status_code != 200:
                print(f"Iteration {iteration} failed: {response.text}")
                time.sleep(13)
                continue

            data = response.json()
            game_id = data.get("gameId")
            print(f"Iteration {iteration}: Wait for 32 seconds...")
            time.sleep(32)

            claim_payload = {
                "gameId": game_id,
                "points": points
            }

            response = requests.post('https://game-domain.blum.codes/api/v1/game/claim', headers=headers, json=claim_payload, proxies=proxy, verify=False)
            if response.status_code != 200:
                print(f"Error from /game/claim (Iteration {iteration}): {response.text}")
                return f"Iteration {iteration} failed."
            return f"Response==> {response.text}"

        except requests.RequestException as ex:
            attempt += 1
            print(f"Attempt {attempt} failed: {ex}")
            if attempt < max_retries:
                time.sleep(retry_delay)
            else:
                return f"Iteration {iteration} failed after {attempt} attempts."




def autoplay(accounts, accname, iter, point_min, point_max):
    print("Development By Reza")

    pr = None

    sum_points = 0
    print(f"[{accname}] => account started for get blum point")
    
    while iter > 0:
        token = (accounts[accname]).get("access_token")

        point = random.randint(point_min, point_max)
        print(f"iter {iter} => point: {point}")
        sum_points = sum_points + point

        make_requests_async(token, point, iter)
        time.sleep(random.randint(4, 10))
        iter -= 1
    print(f"all points tap => {sum_points}")

# if __name__ == "__main__":
#         autoplay()


def user_balance(Accname):

    url = "https://game-domain.blum.codes/api/v1/user/balance"
    accounts = read_accounts()
    access_token = accounts[Accname]["access_token"] 

    headers = defheader
    headers["authorization"] = access_token

    response = requests.get(url, headers = headers)

    print (f"[{Accname}] => user balance  : {response.json()}")

    return response.json()





def check_if_exist(name):
    with open("front.json", "r") as f:
        accounts = json.load(f)
    if not name in accounts:
        return False
    else:
        return True

def save_accounts(data):
    with open("front.json", "w") as f:
        json.dump(data, f)
  

def read_accounts():
    with open("front.json", "r") as f:
        accounts = json.load(f)
    return accounts

def ret_name(account_l):
        decode_data = unquote(string=unquote(string=account_l.split('&tgWebAppVersion')[0]))
        match = re.search(r'"id":(\d+)', decode_data)
        name = re.search(r'"first_name":"(.*?)"', decode_data)
        if match:
            user_id = match.group(1)
            print(user_id)
            name = name.group(1)

        name = user_id + " " + name
        return name, decode_data

def show_number_card():

    # show_msg.delete(0, END)
    account_l = account_link.get()
    # number_card1 = number_card.get()

    # account_l = "https://telegram.blum.codes/#tgWebAppData=query_id%3DAAFhVOIvAwAAAGFU4i8U1nvv%26user%3D%257B%2522id%2522%253A7245812833%252C%2522first_name%2522%253A%2522dogs%25204%2520tablet%2522%252C%2522last_name%2522%253A%2522%2522%252C%2522username%2522%253A%2522Matiuperry%2522%252C%2522language_code%2522%253A%2522en%2522%252C%2522allows_write_to_pm%2522%253Atrue%257D%26auth_date%3D1726201899%26hash%3De3d89048cea31c6fc2f70137c0256d51786e7e27008c21607ff89c24f98b0464&tgWebAppVersion=7.8&tgWebAppPlatform=android&tgWebAppThemeParams=%7B%22bg_color%22%3A%22%231e1e1e%22%2C%22section_bg_color%22%3A%22%23191819%22%2C%22secondary_bg_color%22%3A%22%23000000%22%2C%22text_color%22%3A%22%23ffffff%22%2C%22hint_color%22%3A%22%237d7d7d%22%2C%22link_color%22%3A%22%23bc84dd%22%2C%22button_color%22%3A%22%23c282e6%22%2C%22button_text_color%22%3A%22%23ffffff%22%2C%22header_bg_color%22%3A%22%23262425%22%2C%22accent_text_color%22%3A%22%23c992eb%22%2C%22section_header_text_color%22%3A%22%23d498f1%22%2C%22subtitle_text_color%22%3A%22%237f7e7f%22%2C%22destructive_text_color%22%3A%22%23ee686f%22%2C%22section_separator_color%22%3A%22%23000000%22%7D"
    try:
        name, decode_data = ret_name(account_l)
    except:
        show_msg.insert(END,f"tel : @spy_1290 :  لطفا لینک درست وارد کنید برای راهنمایی بیشتر به ایدی ")
        return 
    
    accounts = read_accounts()

    if not check_if_exist(name):
        accounts[name] = {"auth_url": decode_data}
        save_accounts(accounts)
    else:
        print("exist in database")

    if not (accounts[name]).get("Login"):
        Login(name)

    play_passes = (user_balance(name)).get("playPasses")
    print(f"[{name}] => تعداد کارت موجود: {play_passes}")
    show_msg.insert(END,f"[{name}] => تعداد کارت موجود: {play_passes}")




def start_play():
    show_msg.delete(0, END)

    account_l = account_link.get()
    number_card1 = (number_card.get())
    try:
        name, decode_data = ret_name(account_l)
        number_card1 = int(number_card1)

    except:
        if number_card1 == "" or not number_card1.isdigit():
            show_msg.insert(END,f"لطفا تعداد کارت را به صورت عدد وارد کنید")
        else:
            show_msg.insert(END,f"tel : @spy_1290 :  لطفا لینک درست وارد کنید برای راهنمایی بیشتر به ایدی ")
        return 
    
    accounts = read_accounts()

    if not check_if_exist(name):
        accounts[name] = {"auth_url": decode_data}
        save_accounts(accounts)
    else:
        print("exist in database")

    if not (accounts[name]).get("Login"):
        Login(name)
    
    show_msg.insert(END,f"started to play")

    autoplay(accounts, name, number_card1, 220, 240)




window = Tk()

l1 = Label(window, text="Account Link: ")
l1.grid(row=0, column=0, padx=10, pady=2, sticky="w")

l2 = Label(window, text="number cards:")
l2.grid(row=0, column=2 ,padx=10, pady=10, sticky="w")

account_link = StringVar()
e1 = Entry(window, textvariable=account_link)
e1.grid(row=0, column=1, padx=3, pady=10)

number_card = StringVar()
e2 = Entry(window, textvariable=number_card)
e2.grid(row=0, column=3, padx=10, pady=10)

show_msg = Listbox(window, height=6, width=60)
show_msg.grid(row=2, column=0, rowspan=6, columnspan=2)

sb = Scrollbar(window)
sb.grid(row=2, column=2, rowspan=6)

show_msg.configure(yscrollcommand=sb.set)
sb.configure(command=show_msg.yview)



show_ncard = Button(window, text="show number of card", width=22, command=show_number_card)
show_ncard.grid(row = 2 , column=3, padx=10, pady=10,)


button_start = Button(window, text="Start", width=20, command=start_play)
button_start.grid(row = 3 , column=3, padx=10, pady=7)

window.mainloop()


