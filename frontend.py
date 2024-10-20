"""
a program that users the blum card

account link, number of card for used
show number of card, start


show: 
    number of cards


"""
import threading
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

def create_payload(game_id, points, dogs, headers):
    url = 'https://raw.githubusercontent.com/zuydd/database/main/blum.json'
    data = requests.get(url=url)
    payload_server = data.json().get('payloadServer', [])
    filtered_data = [item for item in payload_server if item['status'] == 1]
    random_id = random.choice([item['id'] for item in filtered_data])
    resp = requests.post(f'https://{random_id}.vercel.app/api/blum', json={'game_id': game_id,
                                                                                    'points': points,
                                                                                    'dogs': dogs
                                                                                    })
    if resp is not None:
        data = resp.json()
        if "payload" in data:
            return data["payload"]
        return None

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

            response = requests.post('https://game-domain.blum.codes/api/v2/game/play', headers=headers)
            if response.status_code == 401:
                print("Token expired. Please enter a valid authorization token.")
                return 5  # Close play card
            elif response.status_code != 200:
                print(f"Iteration {iteration} failed: {response.text}")
                attempt += 1
                time.sleep(13)
                continue

            data = response.json()
            game_id = data.get("gameId")
            print(f"Iteration {iteration}: Wait for 32 seconds...")
            show_msg.insert(END, f"Iteration {iteration}: Wait for 32 seconds...")
            show_msg.see(END)
            show_msg.update()

            time.sleep(random.uniform(32, 40))

            claim_payload = create_payload(game_id, points, 0, headers)
            claim_payload = {"payload": claim_payload}

            response = requests.post('https://game-domain.blum.codes/api/v2/game/claim', headers=headers, json=claim_payload)
            if response.status_code != 200:
                print(f"Error from /game/claim (Iteration {iteration}): {response.text}")
                show_msg.insert(END,f"Error from /game/claim (Iteration {iteration}): {response.text}")
                show_msg.see(END)
                show_msg.update()
                return f"Iteration {iteration} failed."
            return f"Response==> {response.text}"

        except requests.RequestException as ex:
            attempt += 1
            print(f"Attempt {attempt} failed: {ex}")
            show_msg.insert(END,f"Attempt {attempt} failed: {ex}")
            show_msg.see(END)
            show_msg.update()

            if attempt < max_retries:
                time.sleep(retry_delay)
            else:
                show_msg.insert(END,f"Iteration {iteration} failed after {attempt} attempts.")
                return f"Iteration {iteration} failed after {attempt} attempts."




def autoplay(accounts, accname, iter, point_min, point_max):
    print("Development By Reza")

    pr = None

    sum_points = 0
    print(f"[{accname}] => account started for get blum point")
    show_msg.insert(END, f"[{accname}] => شروع و جمع اوری امتیاز ")
    show_msg.update()

    
    while iter > 0:
        token = (accounts[accname]).get("access_token")

        point = random.randint(point_min, point_max)
        print(f"iter {iter} => point: {point}")
        show_msg.insert(END, f"iter {iter} => point: {point}")
        show_msg.see(END)
        show_msg.update()

        sum_points = sum_points + point

        make_requests_async(token, point, iter)
        time.sleep(random.randint(4, 10))
        iter -= 1
    print(f"all points tap => {sum_points}")
    show_msg.insert(END,f"[{accname}] => همه ی امتیاز های به دست امده{sum_points} ")
    show_msg.insert(END,f"[{accname}] => برنامه به اتمام رسید )); یه بوس بده:) ")

    show_msg.see(END)
    show_msg.update()



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

    account_l = account_link.get()

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

    user_status = user_balance(name)
    if user_balance(name).get("message") == "Invalid jwt token":
        show_msg.insert(END,f"[{name}] => توکن نامعتبر در حال تازه سازی")
        Login(name)

    play_passes = (user_balance(name)).get("playPasses")
    print(f"[{name}] => تعداد کارت موجود: {play_passes}")
    show_msg.insert(END,f"[{name}] => تعداد کارت موجود: {play_passes}")




def start_play():
    show_msg.delete(0, END)
    show_msg.update()


    account_l = account_link.get()
    number_card1 = (number_card.get())
    try:
        name, decode_data = ret_name(account_l)
        number_card1 = int(number_card1)

    except:
        if number_card1 == "" or not number_card1.isdigit():
            show_msg.insert(END,f"لطفا تعداد کارت را به صورت عدد وارد کنید")
            show_msg.see(END)
            show_msg.update()

        else:
            show_msg.insert(END,f"tel : @spy_1290 :  لطفا لینک درست وارد کنید برای راهنمایی بیشتر به ایدی ")
            show_msg.update()

        return 
    
    accounts = read_accounts()

    if not check_if_exist(name):
        accounts[name] = {"auth_url": decode_data}
        save_accounts(accounts)
    else:
        print("exist in database")

    if not (accounts[name]).get("Login"):
        Login(name)
    
    if user_balance(name).get("message") == "Invalid jwt token":
        show_msg.insert(END,f"[{name}] => توکن نامعتبر در حال تازه سازی")
        show_msg.update()
        show_msg.see(END)       
        show_msg.update() 
        Login(name)
    play_passes = (user_balance(name)).get("playPasses")
    if  number_card1 > play_passes:
        show_msg.insert(END, "تعداد کارت وارد شده از تعداد کارت موجود بیشتر است")
        show_msg.update()
        number_card1 = play_passes
    show_msg.insert(END,f"started to play")


    show_msg.insert(END,f"در حال بازی با تعداد کارت {number_card1}")
    show_msg.update()
    show_msg.insert(END,"منتظر بمانید...")
    show_msg.see(END)
    show_msg.update() 
    
    threading.Thread(target=autoplay, args=(accounts, name, number_card1, 220, 240)).start()





window = Tk()
window.title("Blum Auto Clicker : Development by Reza")
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


