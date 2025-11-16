import requests
import json
import time
import threading
import re
import os
from bs4 import BeautifulSoup

def print_info_banner():
    banner = (              
        "\033[1;39m┌──────────────────────── Anh Em Legendary Messenger ───────────────────────┐\n"
        "\033[1;33m ➜ \033[1;39mAdmin: Anh Hao - Erik\n"
        "\033[1;33m ➜ \033[1;39mTeam: Anh Em Legendary Messenger\n"
        "\033[1;33m ➜ \033[1;39mChuc Nang Messenger\n"
        "\033[1;33m ➜ \033[1;39m[1] Treo Ngôn\n"
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
        headers = {
            'Cookie': self.cookie,
            'User-Agent': 'Mozilla/5.0'
        }
        try:
            for url in ['https://www.facebook.com', 'https://mbasic.facebook.com', 'https://m.facebook.com']:
                response = requests.get(url, headers=headers)
                match = re.search(r'name="fb_dtsg" value="(.*?)"', response.text)
                if match:
                    self.fb_dtsg = match.group(1)
                    return
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
            response = requests.post('https://www.facebook.com/messaging/send/', data=data, headers=headers)
            return response.status_code == 200
        except:
            return False

def send_messages_loop(messengers, recipient_ids, message, delay):
    while True:
        for recipient_id in recipient_ids:
            for messenger in messengers:
                success = messenger.send_message(recipient_id, message)
                status = "THÀNH CÔNG" if success else "THẤT BẠI"
                print(f"[{status}] Gửi tin nhắn tới box: {recipient_id}")
                time.sleep(delay)

def main():
    os.system('clear')
    print_info_banner()

    recipient_ids = []
    print("Nhập ID box (Enter trống hoặc nhập 'done' để kết thúc):")
    while True:
        rid = input("> ").strip()
        if not rid or rid.lower() == 'done':
            break
        recipient_ids.append(rid)

    cookies = []
    print("Nhập cookie (Enter trống hoặc nhập 'done' để kết thúc):")
    while True:
        c = input("> ").strip()
        if not c or c.lower() == 'done':
            break
        cookies.append(c)

    messengers = []
    for i, cookie in enumerate(cookies, 1):
        try:
            m = Messenger(cookie)
            messengers.append(m)
            print(f"Cookie {i}: OK - User ID: {m.user_id}")
        except Exception as e:
            print(f"Cookie {i}: Lỗi - {e}")

    if not messengers:
        print("Không có cookie hợp lệ.")
        return

    try:
        delay = float(input("Nhập Delay Vào (giây): "))
    except:
        delay = 5

    message_file = input("Nhập tên file chứa tin nhắn: ")
    try:
        with open(message_file, 'r', encoding='utf-8') as f:
            message = f.read().strip()
    except:
        print("Không đọc được file.")
        return

    print("\n💤 Treo Ngôn Được Bật - Tool By AELM🔰💤")
    send_messages_loop(messengers, recipient_ids, message, delay)

if __name__ == "__main__":
    main()
