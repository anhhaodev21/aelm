import requests
import time
import re
import os
from bs4 import BeautifulSoup

def print_info_banner():
    banner = (        
        "\033[1;39m┌──────────────────────── Anh Em Legendary Messenger ───────────────────────┐\n"
        "\033[1;33m ➜ \033[1;39mAdmin: Anh Hao - Erik\n"
        "\033[1;33m ➜ \033[1;39mTeam: Anh Em Legendary Messenger\n"
        "\033[1;33m ➜ \033[1;39mChuc Nang Messenger\n"
        "\033[1;33m ➜ \033[1;39m[4] Thả Sớ|\n"
        "\033[1;39m└─────────────────────────────────────────────────────┘\n"
    )
    print(banner)

class Messenger:
    def __init__(self, cookie):
        self.cookie = cookie
        self.user_id = self.get_user_id()
        self.fb_dtsg = None
        self.init_params()

    def get_user_id(self):
        try:
            return re.search(r"c_user=(\d+)", self.cookie).group(1)
        except:
            raise Exception("Cookie không hợp lệ")

    def init_params(self):
        headers = {'Cookie': self.cookie, 'User-Agent': 'Mozilla/5.0'}
        try:
            response = requests.get('https://m.facebook.com', headers=headers)
            match = re.search(r'name="fb_dtsg" value="(.*?)"', response.text)
            if match:
                self.fb_dtsg = match.group(1)
            else:
                raise Exception("Không tìm thấy fb_dtsg")
        except Exception as e:
            raise Exception(f"Lỗi khởi tạo: {str(e)}")

    def send_message(self, recipient_id, message):
        timestamp = int(time.time() * 1000)
        data = {
            'fb_dtsg': self.fb_dtsg,
            '__user': self.user_id,
            'body': message,
            'action_type': 'ma-type:user-generated-message',
            'timestamp': timestamp,
            'offline_threading_id': str(timestamp),
            'message_id': str(timestamp),
            'thread_fbid': recipient_id,
            'source': 'source:chat:web',
            'client': 'mercury'
        }
        headers = {
            'Cookie': self.cookie,
            'User-Agent': 'Mozilla/5.0',
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        try:
            r = requests.post('https://www.facebook.com/messaging/send/', data=data, headers=headers)
            return r.status_code == 200
        except:
            return False

def send_messages_to_group(group_id, cookie, delay):
    messenger = Messenger(cookie)

    try:
        with open('so.txt', 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except:
        print("Không thể đọc file 'so.txt'.")
        return

    for line in lines:
        message = line.strip()
        if message:
            success = messenger.send_message(group_id, message)
            print(f"Gửi sớ: {message} => {'Thành công' if success else 'Thất bại'}")
            time.sleep(delay)

if __name__ == "__main__":
    os.system('clear')
    print_info_banner()

    group_id = input("-> ID Box: ")
    cookie = input("-> Cookie Facebook: ")
    try:
        delay = float(input("-> Delay (giây): "))
    except:
        delay = 5

    send_messages_to_group(group_id, cookie, delay)
