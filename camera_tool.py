from datetime import datetime
import platform
import socket
import subprocess
import sys
import threading
import time
import urllib.parse
import urllib.request

DB_FILE = "arman_live_cameras.txt"

# === TELEGRAM CONFIGURATION (তোর বটের টোকেন ও চ্যাট আইডি এখানে থাকবে) ===
TELEGRAM_BOT_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"
TELEGRAM_CHAT_ID = "YOUR_TELEGRAM_CHAT_ID"

# Common Port to Brand/App Mapping (Silent Recognition)
PORT_MAPPING = {
    80: ("Generic Web Cam / Router", "HTTP"),
    554: ("RTSP Stream Camera", "RTSP"),
    8000: ("Hikvision DVR/NVP", "Hik-Connect"),
    37777: ("Dahua DVR/Camera", "gDMSS/iDMSS"),
    8899: ("V380 / Generic IP Cam", "V380 Pro"),
}


# ==================== LICENSE & HWID SYSTEM ====================
def get_device_hwid():
  """Generates a unique hardware ID for the client's device"""
  try:
    # Combining platform details to create a unique device fingerprint
    system_info = (
        platform.node()
        + platform.machine()
        + platform.processor()
        + platform.system()
    )
    # Creating a stable hash/string representation
    import hashlib

    hwid = hashlib.md5(system_info.encode("utf-8")).hexdigest().upper()
    return hwid
  except:
    return "ARMAN-CLIENT-DEVICE-2026"


def verify_client_license():
  """Fetches keys.txt from GitHub and verifies client license and expiry date"""
  user_hwid = get_device_hwid()
  try:
    # তোর গিটহাবের র-লিংক (Raw Link) থেকে keys.txt চেক করবে
    url = (
        "https://raw.githubusercontent.com/Armanyb1/Cc-tv-Hack-YB/main/keys.txt"
    )
    response = urllib.request.urlopen(url, timeout=5)
    lines = response.read().decode("utf-8").splitlines()

    is_authorized = False

    for line in lines:
      line = line.strip()
      if not line or line.startswith("#"):
        continue

      parts = line.split()
      if len(parts) >= 2:
        file_hwid, expiry_value = parts[0], parts[1]

        if file_hwid == user_hwid:
          # যদি লাইফটাইম হয়
          if expiry_value.lower() == "lifetime":
            is_authorized = True
            break
          else:
            # ডেট চেক করার লজিক (YYYY-MM-DD ফরম্যাট)
            try:
              expiry_date = datetime.strptime(expiry_value, "%Y-%m-%d")
              current_date = datetime.now()

              if current_date <= expiry_date:
                is_authorized = True
                break
              else:
                print(
                    "\n\033[91m[-] আপনার লাইসেন্সের মেয়াদ শেষ হয়ে গেছে! টুলটি"
                    " লক করা হয়েছে।\033[0m"
                )
                print(
                    "[-] নতুন করে লাইসেন্স নিতে যোগাযোগ করুন: https://t.me/Armanyb"
                )
                sys.exit()
            except ValueError:
              print("\n\033[91m[-] লাইসেন্স ডেট ফরম্যাটে সমস্যা রয়েছে!\033[0m")
              sys.exit()

    if not is_authorized:
      print("\n\033[91m" + "=" * 65)
      print(" [!] ACCESS DENIED: আপনার ডিভাইসটি রেজিস্টার্ড নয় বা লাইসেন্স নেই!")
      print(f" [!] আপনার ডিভাইস HWID: {user_hwid}")
      print(" [!] এই HWID টি এডমিনকে (Telegram: https://t.me/Armanyb) পাঠিয়ে দিন।")
      print("=" * 65 + "\033[0m")
      sys.exit()

  except Exception as e:
    print(
        "\n\033[93m[!] সতর্কতা: লাইসেন্স সার্ভার কানেকশনে সমস্যা হয়েছে বা ইন্টারনেট"
        f" নেই! ({e})\033[0m"
    )
    print("[!] ইন্টারনেট কানেকশন চেক করে আবার চেষ্টা করুন।")
    sys.exit()


# ==============================================================


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
  """Sends silent alert to your Telegram Bot"""
  if (
      TELEGRAM_BOT_TOKEN == "YOUR_TELEGRAM_BOT_TOKEN"
      or TELEGRAM_CHAT_ID == "YOUR_TELEGRAM_CHAT_ID"
  ):
    return
  try:
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    data = urllib.parse.urlencode(
        {"chat_id": TELEGRAM_CHAT_ID, "text": message}
    ).encode("utf-8")
    req = urllib.request.Request(url, data=data, method="POST")
    urllib.request.urlopen(req, timeout=3)
  except:
    pass


def save_to_db(ip, port, brand, proto, rtsp_link):
  timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
  entry = f"[IP]: {ip}:{port} | [Device]: {brand} | [Proto]: {proto} | [RTSP]: {rtsp_link} | [Time]: {timestamp}\n"
  with open(DB_FILE, "a") as f:
    f.write(entry)


def silent_check(ip, port):
  """Silently checks the port and sends Telegram notification on success"""
  try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(1.5)  # Low timeout for silent & fast check
    result = s.connect_ex((ip, port))
    s.close()

    if result == 0:
      brand, proto = PORT_MAPPING.get(port, ("Unknown IP Device", "TCP"))

      # Generate RTSP Link if port is 554 or supports streaming
      if port == 554:
        rtsp_link = f"rtsp://{ip}:{port}/live/ch0"
      elif port == 8000:
        rtsp_link = f"rtsp://{ip}:{port}/h264/ch1/main/av_stream"
      else:
        rtsp_link = f"http://{ip}:{port}"

      print(f"\n[+] Active & Silent Match Found: {ip}:{port} ({brand})")
      print(f"    [🔗 Stream URL]: {rtsp_link}")

      save_to_db(ip, port, brand, proto, rtsp_link)

      # Send alert to Telegram
      tg_msg = f"🚨 Arman Recon Alert!\n\n[IP]: {ip}:{port}\n[Device]: {brand}\n[Link]: {rtsp_link}"
      send_telegram_alert(tg_msg)
  except:
    pass


def scan_subnet(subnet_prefix):
  print(
      f"\n[i] Starting Silent Recon on Subnet: {subnet_prefix}.1 to"
      f" {subnet_prefix}.254"
  )
  send_telegram_alert(f"🔍 Scan Started on Subnet: {subnet_prefix}.x")

  threads = []
  ports_to_check = [80, 554, 8000, 37777, 8899]

  for i in range(1, 255):
    ip = f"{subnet_prefix}.{i}"
    for port in ports_to_check:
      t = threading.Thread(target=silent_check, args=(ip, port))
      threads.append(t)
      t.start()

    if len(threads) >= 50:
      for t in threads:
        t.join()
      threads = []

  for t in threads:
    t.join()
  print("\n[✓] Silent Recon Completed Successfully!")
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
  # টুল রান হওয়ার সাথে সাথেই লাইসেন্স চেক করবে
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
