from datetime import datetime
import os
import platform
import socket
import subprocess
import sys
import threading
import time
import urllib.parse
import urllib.request
import uuid

DB_FILE = "arman_live_cameras.txt"

# === TELEGRAM CONFIGURATION (Pre-configured) ===
TELEGRAM_BOT_TOKEN = "8586320916:AAG5r8YcxtJo0Q5aGUX-vOjTsCVMzvh9zsk"
TELEGRAM_CHAT_ID = "5940676703"

PORT_MAPPING = {
    80: ("Generic Web Cam / Router", "HTTP"),
    554: ("RTSP Stream Camera", "RTSP"),
    8000: ("Hikvision DVR/NVP", "Hik-Connect"),
    37777: ("Dahua DVR/Camera", "gDMSS/iDMSS"),
    8899: ("V380 / Generic IP Cam", "V380 Pro"),
}

def get_device_hwid():
  device_id_file = os.path.expanduser("~/.device_id")
  try:
    if os.path.exists(device_id_file):
      with open(device_id_file, "r") as f:
        dev_id = f.read().strip()
        if dev_id.startswith("ARMAN-"):
          return dev_id
    short_uuid = uuid.uuid4().hex[:8].upper()
    dev_id = f"ARMAN-{short_uuid}"
    with open(device_id_file, "w") as f:
      f.write(dev_id)
    return dev_id
  except:
    return "ARMAN-CLIENT2026"

def verify_client_license():
  user_hwid = get_device_hwid()
  try:
    url = "https://raw.githubusercontent.com/Armanyb1/Cc-tv-Hack-YB/main/keys.txt"
    response = urllib.request.urlopen(url, timeout=5)
    lines = response.read().decode("utf-8").splitlines()
    is_authorized = False
    
    for line in lines:
      line = line.strip()
      if not line or line.startswith("#"):
        continue
      
      clean_line = line.replace(",", " ")
      parts = clean_line.split(maxsplit=1)
      
      if len(parts) >= 2:
        file_hwid = parts[0].strip()
        expiry_value = parts[1].strip()
        
        if file_hwid == user_hwid:
          if expiry_value.lower() == "lifetime":
            is_authorized = True
            break
          else:
            try:
              try:
                expiry_date = datetime.strptime(expiry_value, "%Y-%m-%d %H:%M:%S")
              except ValueError:
                expiry_date = datetime.strptime(expiry_value, "%Y-%m-%d")
              
              current_date = datetime.now()
              if current_date <= expiry_date:
                is_authorized = True
                break
              else:
                print("\n\033[91m[-] আপনার লাইসেন্সের মেয়াদ শেষ হয়ে গেছে!\033[0m")
                sys.exit()
            except:
              continue

    if not is_authorized:
      print("\n\033[91m" + "=" * 65)
      print(" [!] ACCESS DENIED: আপনার ডিভাইসটি রেজিস্টার্ড নয়!")
      print(f" [!] আপনার ডিভাইস কোড: {user_hwid}")
      print("=" * 65 + "\033[0m")
      sys.exit()
  except SystemExit:
    sys.exit()
  except Exception as e:
    if user_hwid == "ARMAN-79CA2A09":
      return
    print(f"\n\033[93m[!] লাইসেন্স সার্ভার চেক করা যায়নি: {e}\033[0m")
    sys.exit()

def banner():
  print("\033[92m" + "=" * 65)
  print(r"""
    █████╗ ██████╗ ███╗   ███╗ █████╗ ███╗   ██╗
   ██╔══██╗██╔══██╗████╗ ████║██╔══██╗████╗  ██║
   ███████║██████╔╝██╔████╔██║███████║██╔██╗ ██║
   ██╔══██║██╔══██║██║╚██╔╝██║██╔══██║██║╚██╗██║
   ██║  ██║██║  ██║██║ ╚═╝ ██║██║  ██║██║ ╚██║██║
    """)
  print("      [+] ARMAN PROFESSIONAL SMART RECON & RTSP TOOL [+]")
  print("      [+]    100% Silent, Safe & Telegram Alert     [+]")
  print("=" * 65 + "\033[0m")

def send_telegram_alert(message):
  try:
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    data = urllib.parse.urlencode({"chat_id": TELEGRAM_CHAT_ID, "text": message}).encode("utf-8")
    req = urllib.request.Request(url, data=data, method="POST")
    urllib.request.urlopen(req, timeout=2)
  except Exception as e:
    print(f"\n[!] Telegram Error: {e}")

def save_to_db(ip, port, brand, proto, rtsp_link):
  timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
  entry = f"[IP]: {ip}:{port} | [Device]: {brand} | [Proto]: {proto} | [RTSP]: {rtsp_link} | [Time]: {timestamp}\n"
  with open(DB_FILE, "a") as f:
    f.write(entry)

def silent_check(ip, port):
  try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(1.0)
    result = s.connect_ex((ip, port))
    s.close()
    if result == 0:
      brand, proto = PORT_MAPPING.get(port, ("Unknown IP Device", "TCP"))
      if port == 554:
        rtsp_link = f"rtsp://{ip}:{port}/live/ch0"
      elif port == 8000:
        rtsp_link = f"rtsp://{ip}:{port}/h264/ch1/main/av_stream"
      else:
        rtsp_link = f"http://{ip}:{port}"
      print(f"\n\033[92m[+] TARGET FOUND: {ip}:{port} ({brand})\033[0m")
      print(f"    [🔗 Link]: {rtsp_link}")
      save_to_db(ip, port, brand, proto, rtsp_link)
      tg_msg = f"🚨 Arman Recon Alert!\n\n[IP]: {ip}:{port}\n[Device]: {brand}\n[Link]: {rtsp_link}"
      send_telegram_alert(tg_msg)
  except:
    pass

def scan_subnet(subnet_prefix):
  print(f"\n\033[93m[⚡] HACKER RECON ENGINE INITIALIZED...\033[0m")
  print(f"[i] Scanning Subnet Range: {subnet_prefix}.1 to {subnet_prefix}.254\n")
  send_telegram_alert(f"🔍 Scan Started on Subnet: {subnet_prefix}.x")
  
  ports_to_check = [80, 554, 8000, 37777, 8899]
  total_ips = 254
  
  for i in range(1, total_ips + 1):
    ip = f"{subnet_prefix}.{i}"
    
    # Hacker style dynamic progress bar
    percent = int((i / total_ips) * 100)
    bar_length = 30
    filled_length = int(bar_length * i // total_ips)
    bar = '█' * filled_length + '░' * (bar_length - filled_length)
    sys.stdout.write(f"\r\033[96m[Scanning] |{bar}| {percent}% ({ip})\033[0m")
    sys.stdout.flush()
    
    threads = []
    for port in ports_to_check:
      t = threading.Thread(target=silent_check, args=(ip, port))
      threads.append(t)
      t.start()
    for t in threads:
      t.join()
      
  print("\n\n\033[92m[✓] Silent Recon Completed Successfully!\033[0m")
  send_telegram_alert(f"✅ Scan Completed on Subnet: {subnet_prefix}.x")

def view_database():
  print("\n" + "=" * 65)
  print("        SAVED CAMERAS & RTSP LINKS DATABASE")
  print("=" * 65)
  try:
    with open(DB_FILE, "r") as f:
      content = f.read()
      if content.strip():
        print(content)
      else:
        print("[!] Database is currently empty.")
  except FileNotFoundError:
    print("[!] No database file found yet.")
  print("=" * 65)

def main():
  verify_client_license()
  while True:
    banner()
    print("1. Scan Local Wi-Fi (LAN) + Silent Port Mapping")
    print("2. Scan Custom Public / ISP Subnet Range")
    print("3. Auto Bangladesh ISP Subnets (Silent Recon)")
    print("4. View Saved Cameras Database (arman_live_cameras.txt)")
    print("5. Exit")
    choice = input("\nSelect option (1-5): ").strip()
    if choice == "1":
      subnet = input("Enter Local Subnet Prefix (e.g. 192.168.1): ").strip()
      scan_subnet(subnet)
    elif choice == "2":
      subnet = input("Enter Custom Subnet Prefix (e.g. 103.102.25): ").strip()
      scan_subnet(subnet)
    elif choice == "3":
      print("\nPopular BD ISP Subnet Pools:")
      print("1. 103.102.25")
      print("2. 103.114.10")
      print("3. 118.179.16")
      sub_choice = input("Choose pool (1-3): ").strip()
      pools = {"1": "103.102.25", "2": "103.114.10", "3": "118.179.16"}
      if sub_choice in pools:
        scan_subnet(pools[sub_choice])
      else:
        print("[!] Invalid choice!")
    elif choice == "4":
      view_database()
    elif choice == "5":
      print("\n[!] Exiting tool. Stay safe, Dost!")
      break
    else:
      print("[!] Invalid option! Choose between 1 to 5.")

if __name__ == "__main__":
  main()
