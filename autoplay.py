import requests
import time
import random
from urllib.parse import unquote
import urllib3

# Disable SSL warnings
urllib3.disable_warnings()

def login(accname):
    """
    Logs into the account using the provided account name.
    """
    print("Logging into Account", accname)

    proxy = None
    url = "https://user-domain.blum.codes/api/v1/auth/provider/PROVIDER_TELEGRAM_MINI_APP"
    global accounts
    auth_url = accounts[accname]["auth_url"]
    decode_data = unquote(string=unquote(string=auth_url.split('tgWebAppData=')[1].split('&tgWebAppVersion')[0]))

    json_data = {"query": decode_data}
    response = requests.post(url, json=json_data, proxies=proxy, verify=False)
    response_json = response.json()

    ref_token = response_json.get("token").get("refresh")
    access_token = "Bearer " + response_json.get("token").get("access")
    accounts[accname]["access_token"] = access_token
    accounts[accname]["refresh_token"] = ref_token
    accounts[accname]["Login"] = True

    return ref_token, access_token

def make_requests_async(authorization_token, points, iteration):
    """
    Makes asynchronous requests to play and claim points in the game.
    """
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

            response = requests.post('https://game-domain.blum.codes/api/v1/game/play', headers=headers, proxies=proxy, verify=False)
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
            time.sleep(32)

            claim_payload = {
                "gameId": game_id,
                "points": points
            }

            response = requests.post('https://game-domain.blum.codes/api/v1/game/claim', headers=headers, json=claim_payload, proxies=proxy, verify=False)
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
    """
    Automates the process of playing the game and claiming points.
    """
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
#     autoplay()
