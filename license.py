from datetime import datetime
import platform
import sys
import urllib.request


def get_device_hwid():
  try:
    system_info = (
        platform.node()
        + platform.machine()
        + platform.processor()
        + platform.system()
    )
    import hashlib

    return hashlib.md5(system_info.encode("utf-8")).hexdigest().upper()
  except:
    return "ARMAN-CLIENT-DEVICE-2026"


def verify_client_license():
  user_hwid = get_device_hwid()
  try:
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
          if expiry_value.lower() == "lifetime":
            is_authorized = True
            break
          else:
            try:
              expiry_date = datetime.strptime(expiry_value, "%Y-%m-%d")
              if datetime.now() <= expiry_date:
                is_authorized = True
                break
              else:
                print(
                    "\n[-] আপনার লাইসেন্সের মেয়াদ শেষ হয়ে গেছে! টুল লক করা"
                    " হয়েছে।"
                )
                sys.exit()
            except:
              sys.exit()

    if not is_authorized:
      print(f"\n[!] ACCESS DENIED! আপনার HWID: {user_hwid}")
      sys.exit()
  except:
    print("\n[!] লাইসেন্স সার্ভার কানেকশনে সমস্যা!")
    sys.exit()
