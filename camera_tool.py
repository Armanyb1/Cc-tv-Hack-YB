#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Arman CC Camera Scanner - Online HWID & Expiry License Protected
Author: Arman Yb
GitHub: github.com/Armanyb1
Telegram: @Armanyb
"""

import socket
import requests
import threading
from queue import Queue
import ipaddress
import pyfiglet
from datetime import datetime
import time
import sys
import aiohttp
import asyncio
import os
import platform
import uuid

try:
    from colorama import Fore, Style, init
    init(autoreset=True)
    HAS_COLOR = True
except ImportError:
    HAS_COLOR = False
    class Fore:
        GREEN = '\033[92m'
        RED = '\033[91m'
        YELLOW = '\033[93m'
        CYAN = '\033[96m'
        WHITE = '\033[97m'
    class Style:
        RESET_ALL = '\033[0m'

OUTPUT_FILE = "BDALLIP.txt"
APNIC_URL = "https://ftp.apnic.net/stats/apnic/delegated-apnic-latest"
REMOTE_LICENSE_URL = "https://raw.githubusercontent.com/Armanyb1/Cc-tv-Hack-YB/refs/heads/main/keys.txt"

_t1 = "8586320916"
_t2 = "AAG5r8YcxtJo0Q5aGUX-vOjTsCVMzvh9zsk"
TELEGRAM_BOT_TOKEN = f"{_t1}:{_t2}"
TELEGRAM_CHAT_ID = "5940676703"

socket.setdefaulttimeout(0.25)
detected_ips = set()
stop_scan = False
pause_scan = False

def get_hwid():
    device_id_path = "/data/data/com.termux/files/home/.device_id"
    try:
        if os.path.exists(device_id_path):
            with open(device_id_path, "r") as f:
                return f.read().strip()
        else:
            short_id = str(uuid.uuid4()).split('-')[0].upper()
            hwid = f"ARMAN-{short_id}"
            with open(device_id_path, "w") as f:
                f.write(hwid)
            return hwid
    except:
        return "ARMAN-PRO-ID"

def verify_online_license():
    print(f"\n{Fore.CYAN}{'='*50}{Style.RESET_ALL}")
    print(f"{Fore.GREEN}[*] Verifying Online License & Expiry...{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'='*50}{Style.RESET_ALL}\n")
    
    current_hwid = get_hwid()
    print(f"{Fore.YELLOW}[i] Your Device HWID: {Fore.WHITE}{current_hwid}{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}[i] Send this HWID to Telegram: {Fore.GREEN}@Armanyb{Style.RESET_ALL}\n")
    
    try:
        response = requests.get(REMOTE_LICENSE_URL, timeout=10)
        if response.status_code != 200:
            print(f"{Fore.RED}[❌] Connection Error: Could not verify license from server.{Style.RESET_ALL}")
            sys.exit(1)
            
        license_data = response.text.strip().splitlines()
        authorized = False
        expiry_message = ""
        
        for line in license_data:
            if not line or line.startswith('#'):
                continue
            parts = line.strip().split('|')
            if len(parts) >= 2:
                db_hwid = parts[0].strip().upper()
                db_expiry = parts[1].strip().upper()
                
                if db_hwid == current_hwid:
                    if db_expiry == "LIFETIME":
                        authorized = True
                        expiry_message = "Lifetime Access"
                        break
                    else:
                        try:
                            expiry_date = datetime.strptime(db_expiry, "%Y-%m-%d")
                            if datetime.now() <= expiry_date:
                                authorized = True
                                days_left = (expiry_date - datetime.now()).days
                                expiry_message = f"Valid (Expires in {days_left} days - {db_expiry})"
                                break
                            else:
                                print(f"\n{Fore.RED}[❌] Your License has EXPIRED on {db_expiry}!{Style.RESET_ALL}")
                                sys.exit(1)
                        except:
                            pass
                            
        if authorized:
            print(f"{Fore.GREEN}[✓] Access Granted! Status: {expiry_message}{Style.RESET_ALL}")
            time.sleep(1.5)
            return True
        else:
            print(f"\n{Fore.RED}[❌] Access Denied: HWID not registered in server database!{Style.RESET_ALL}")
            sys.exit(1)
    except:
        print(f"{Fore.RED}[❌] Network Error: Failed to reach license server.{Style.RESET_ALL}")
        sys.exit(1)

def print_banner():
    banner = f"""
╔═══════════════════════════════════════╗
║   Arman CC Camera Scanner (Pro)       ║
║   Online Secure & Auto-Lock System    ║
║   Telegram: @Armanyb                  ║
╚═══════════════════════════════════════╝
"""
    print(f"{Fore.CYAN}{banner}{Style.RESET_ALL}")
    print(f"{Fore.GREEN}[*] Developer: {Fore.YELLOW}Arman Yb{Style.RESET_ALL}\n")

def send_telegram_alert(camera_type, ip, port, url):
    try:
        message = (
            f"🚨 *New Camera Discovered!* 🚨\n\n"
            f"📌 *Brand:* {camera_type}\n"
            f"🌐 *IP:* `{ip}`\n"
            f"🔌 *Port:* `{port}`\n"
            f"🔗 *URL:* {url}\n"
            f"⏱ *Time:* {datetime.now().strftime('%Y-%m-%d %I:%M:%S %p')}"
        )
        requests.post(f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage", 
                      data={"chat_id": TELEGRAM_CHAT_ID, "text": message, "parse_mode": "Markdown"}, timeout=3)
    except:
        pass

async def fetch_bd_ipv4():
    ipv4_list = []
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(APNIC_URL, timeout=aiohttp.ClientTimeout(total=60)) as resp:
                if resp.status == 200:
                    async for line_bytes in resp.content:
                        line = line_bytes.decode('utf-8', errors='ignore').strip()
                        if not line or line.startswith('#'): continue
                        parts = line.split('|')
                        if len(parts) >= 7 and parts[1].upper() == 'BD' and parts[2].lower() == 'ipv4':
                            ipv4_list.append(f"{parts[3]}/{parts[4]}")
    except:
        pass
    return ipv4_list

async def save_ip_ranges(ipv4_list):
    if not ipv4_list: return False
    try:
        with open(OUTPUT_FILE, 'w') as f:
            f.write('\n'.join(ipv4_list))
        return True
    except:
        return False

def cidr_to_ip_range(cidr_notation):
    try:
        ip_str, count_str = cidr_notation.split('/')
        import math
        prefix_len = 32 - int(math.log2(int(count_str)))
        return [str(ip) for ip in ipaddress.IPv4Network(f"{ip_str}/{prefix_len}", strict=False).hosts()]
    except:
        return []

def scan(ip, port):
    global stop_scan, pause_scan
    if stop_scan or pause_scan: return
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect((ip, port))
            sock.send(b'GET / HTTP/1.1\r\nHost: example.com\r\n\r\n')
            response = sock.recv(4096).decode()
            url = f"http://{ip}:{port}" if port == 8080 else f"http://{ip}"
            
            if '<title>WEB SERVICE</title>' in response:
                if ip not in detected_ips:
                    detected_ips.add(ip)
                    print(f"{Fore.GREEN}[✓] Dahua Camera Found! {url}{Style.RESET_ALL}")
                    threading.Thread(target=send_telegram_alert, args=("Dahua Camera", ip, port, url), daemon=True).start()
            elif 'login.asp' in response:
                if ip not in detected_ips:
                    detected_ips.add(ip)
                    print(f"{Fore.RED}[✓] Hikvision Camera Found! {url}{Style.RESET_ALL}")
                    threading.Thread(target=send_telegram_alert, args=("Hikvision Camera", ip, port, url), daemon=True).start()
    except:
        pass

def execute(queue):
    global stop_scan
    while not stop_scan:
        try:
            ip, port = queue.get(timeout=0.5)
            scan(ip, port)
            queue.task_done()
        except:
            if stop_scan: break

def run_scanner():
    global stop_scan
    stop_scan = False
    try:
        with open(OUTPUT_FILE, 'r') as f:
            ip_ranges = [line.strip() for line in f if line.strip()]
    except:
        print(f"{Fore.RED}[!] {OUTPUT_FILE} not found! Update ranges first.{Style.RESET_ALL}")
        return
    
    queue = Queue()
    for _ in range(100):
        threading.Thread(target=execute, args=(queue,), daemon=True).start()
        
    for cidr in ip_ranges:
        if stop_scan: break
        for ip in cidr_to_ip_range(cidr):
            if stop_scan: break
            queue.put((ip, 80))
            queue.put((ip, 8080))
    while not stop_scan and not queue.empty():
        time.sleep(0.5)
    print(f"\n{Fore.GREEN}[✓] Scan Complete!{Style.RESET_ALL}\n")

async def main():
    verify_online_license()
    print_banner()
    while type(True) == bool:
        print(f"\n{Fore.CYAN}1. Update IP Ranges\n2. Scan Cameras\n3. Exit{Style.RESET_ALL}")
        choice = input(f"{Fore.GREEN}Select option (1-3): {Style.RESET_ALL}").strip()
        if choice == '1':
            ipv4_list = await fetch_bd_ipv4()
            if ipv4_list: await save_ip_ranges(ipv4_list); print("Updated successfully!")
        elif choice == '2':
            run_scanner()
        elif choice == '3':
            break

if __name__ == "__main__":
    asyncio.run(main())
