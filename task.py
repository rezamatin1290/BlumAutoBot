def solve(acc_name, task: dict):
    access_token = accounts[acc_name]["access_token"]
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

def solve_task(acc_name):
    url_task = "https://earn-domain.blum.codes/api/v1/tasks"
    access_token = accounts[acc_name]["access_token"]
    headers = default_header.copy()
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
        solve(acc_name, task)
