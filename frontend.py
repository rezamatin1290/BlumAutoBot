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


def Login(Accname):
    #tg_web_data
    print("Loging to Account" , Accname)

    proxy = None
    url = "https://user-domain.blum.codes/api/v1/auth/provider/PROVIDER_TELEGRAM_MINI_APP"
    global accounts
    auth_url = accounts[Accname]["auth_url"]
    decode_data = unquote(string=unquote(string=auth_url.split('tgWebAppData=')[1].split('&tgWebAppVersion')[0]))

    json_data = {"query" : decode_data}
    response = requests.post(url, json=json_data, proxies=proxy, verify=False)
    response_json = response.json()

    ref_token = response_json.get("token").get("refresh")
    access_token = "Bearer " + (response_json).get("token").get("access")
    accounts[Accname]["access_token"] = access_token
    accounts[Accname]["refresh_token"] = ref_token
    accounts[Accname]["Login"] = True

    
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



def show_number_card():
    with open("front.json", "r") as f:
        accounts = json.load(f)
    show_msg.delete(0, END)

    account_l = account_link.get()
    number_card1 = number_card.get()


    # x = x.strip()
    decode_data = unquote(string=unquote(string=account_l.split('&tgWebAppVersion')[0]))
    match = re.search(r'"id":(\d+)', decode_data)
    name = re.search(r'"first_name":"(.*?)"', decode_data)
    if match:
        user_id = match.group(1)
        print(user_id)
        name = name.group(1)
    name = user_id + " " + name

    if not name in accounts:
        print("{name} doesnt exist in database")
        accounts[name] = {"auth_url": decode_data}
        with open("front.json", "w") as f:
            print(accounts)
            json.dump(accounts,f)
    else:
        print("exist in database")

    show_msg.insert(END, f"name accunt is => {name}")


def start_play():
    pass

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

show_msg = Listbox(window, height=6, width=50)
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


