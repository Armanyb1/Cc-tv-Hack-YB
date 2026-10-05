# Arman CC Camera Scanner (BD Networks)

An advanced and high-performance network security tool designed specifically for scanning and analyzing IP cameras across Bangladesh networks.

## 🚀 Key Features

* **APNIC Integration:** Automatically fetches the latest official Bangladesh IPv4 ranges from the APNIC database.
* **Smart Camera Detection:** Identifies prominent camera models and web services including:
  * Dahua Technology Web Services
  * HIK Vision Surveillance Systems
* **Real-Time Live Save:** Captured camera details are written to output files instantly as they are found (`file.flush()`).
* **Multi-Threaded Performance:** Utilizes a robust 100-thread concurrent scanning mechanism for maximum speed.
* **Termux Optimized:** Fully compatible with Android via Termux, featuring graceful fallback color support.
* **Interactive Control:** Built-in safe stop and pause/resume capabilities during active scans.

---

## 📱 Installation & Setup

### For Termux (Android)
Update your package repositories:
```bash
pkg update && pkg upgrade -y
```

Install essential packages:
```bash
pkg install python git -y
```

Install required Python libraries:
```bash
pip install requests aiohttp pyfiglet colorama
```

### For Desktop (Windows / Linux / macOS)
Ensure Python is installed, then run:
```bash
pip install requests aiohttp pyfiglet colorama
```

---

## 🛠️ How to Use

Clone your repository and launch the tool:
```bash
git clone https://github.com/Armanyb/arman-cc-camera-tool
cd arman-cc-camera-tool
python camera_tool.py
```

### Menu Options
1. **Fetch/Update IP Ranges:** Downloads the fresh Bangladesh IP allocation list.
2. **Execute Camera Scan:** Scans the target IP ranges for active cameras.
3. **Automated Sequence:** Performs IP fetching followed immediately by the scanning process.
4. **Exit:** Safely terminates the program.

---

## 🎮 Scan Control Shortcuts

Manage your scanning process on the fly:
* **Ctrl+C:** ⛔ Instantly halts the scan and exits cleanly.
* **Ctrl+Z:** ⏸️ Pauses or resumes the active scan thread pool (Supported on Linux, macOS, and Termux).

---

## 📁 Output & Results

* `BDALLIP.txt`: Contains all fetched Bangladesh IP ranges in CIDR format.
* `CCTV Found.txt`: Live-updated log containing details of all successfully discovered cameras.

### Sample Detection Log:
```text
============================================================
Camera Type: Dahua Technology Web Service
IP Address: 192.168.1.50
Port: 80
URL: http://192.168.1.50
Detection Time: 2026-10-05 16:00:00
============================================================
```

---

## 🛡 Legal Disclaimer

This utility is built strictly for educational, research, and authorized penetration testing purposes. Always secure proper, explicit permission from network owners before conducting any scans. The author holds no responsibility for misuse.

---

**Developed with ❤️ by Arman Yb**  
*Telegram Support:* `@Armanyb`  
*GitHub Profile:* `[github.com/Armanyb](https://github.com/Armanyb)`
