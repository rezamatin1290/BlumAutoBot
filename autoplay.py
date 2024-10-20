import requests
import time
import random
from urllib.parse import unquote
import urllib3
import json

urllib3.disable_warnings()

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

def make_requests_async(authorization_token, points, iteration):
    proxy = None
    max_retries = 4
    attempt = 0

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

    while attempt < max_retries:
        try:
            time.sleep(random.uniform(1, 3))

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

            # dogs_eligible = requests.post('https://game-domain.blum.codes/api/v2/game/eligibility/dogs_drop', headers=headers, proxies=proxy, verify=False) 
            
            # if dogs_eligible is not None:
            #     eligible = dogs_eligible.json().get('eligible', False)
            # else:
            #     eligible = None

            time.sleep(random.uniform(32, 40))
            
            claim_payload = create_payload(game_id, points, 0, headers)
            claim_payload = {"payload": claim_payload}
            # if eligible:
            #     dogs = random.randint(50, 80) 
            # else:
            #     claim_payload = create_payload(game_id, points, 0, headers)
    
            response = requests.post('https://game-domain.blum.codes/api/v2/game/claim', headers=headers, json=claim_payload)
            if response.status_code != 200:
                print(f"Error from /game/claim (Iteration {iteration}): {response.text}")
                attempt += 1
                continue

            return f"Response==> {response.text}"

        except requests.RequestException as ex:
            attempt += 1
            print(f"Attempt {attempt} failed: {ex}")
            if attempt < max_retries:
                time.sleep(random.uniform(6, 10))
            else:
                return 5

    if attempt >= max_retries:
        return 5

def autoplay(accounts, accname, iter, point_min, point_max):
    print("Development By Reza")

    sum_points = 0
    print(f"[{accname}] => account started for get blum point")

    while iter > 0:
        token = accounts[accname].get("access_token")

        point = random.randint(point_min, point_max)
        print(f"iter {iter} => point: {point}")
        sum_points += point

        retry = make_requests_async(token, point, iter)
        if retry == 5:
            return
        time.sleep(random.uniform(4, 10))
        iter -= 1

    print(f"all points tap => {sum_points}")

# Uncomment the following lines to run the autoplay function directly
# if __name__ == "__main__":
#     bearer_token = "your Bearer token"
#     p = random.randint(minpoint, maxpoint)
#     make_requests_async(bearer_token, p, 1)