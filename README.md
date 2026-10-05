# 📸 Arman CC Camera Scanner (BD Networks)
An advanced and high-performance network security tool designed specifically for scanning and analyzing IP cameras across Bangladesh networks. Developed by **Arman Yb**.

---

### 🚀 Key Features
- **APNIC Integration:** Automatically fetches the latest official Bangladesh IPv4 ranges from the APNIC database.
- **Smart Camera Detection:** Identifies prominent camera models and web services including Dahua Technology and HIK Vision Surveillance Systems.
- **Online HWID Protection:** Fully secured with a remote online license verification system.
- **Multi-Threaded Performance:** Utilizes a robust 100-thread concurrent scanning mechanism for maximum speed.
- **Termux Optimized:** Fully compatible with Android via Termux, featuring graceful fallback color support.

---

### 📱 Installation & Setup (ইনস্টলেশন ও চালুর নিয়ম)

**For Termux (Android):**
টার্মাক্স ওপেন করে নিচের কমান্ডগুলো এক এক করে পেস্ট করো:

    pkg update && pkg upgrade -y
    pkg install python git -y
    git clone https://github.com/Armanyb1/Cc-tv-Hack-YB.git
    cd Cc-tv-Hack-YB
    pip install requests aiohttp pyfiglet colorama
    python camera_tool.py

---

### 💳 Pricing & License (মূল্য ও লাইসেন্স প্যাকেজ)
এই টুলটি ব্যবহার করার জন্য পেইড লাইসেন্স নিতে হবে। আমাদের সাশ্রয়ী প্যাকেজগুলো দেখে নিন:
- **৭ দিন:** ১০০ টাকা
- **১ মাস (Monthly):** ৩৮০ টাকা
- **আজীবন (Lifetime):** ৭০০ টাকা
- **বিকাশ/নগদ নম্বর:** `01880374287`

**যেভাবে লাইসেন্স নিবে:**
পেমেন্ট করার পর টার্মাক্সে টুল রান করলে স্ক্রিনে যে **Unique Device Code (HWID)** দেখাবে, সেটি স্ক্রিনশটসহ সরাসরি আমাদের টেলিগ্রামে পাঠিয়ে দিন। সাথে সাথে লাইসেন্স অ্যাক্টিভ করে দেওয়া হবে!

---

### 🛠️ How to Use & Menu Options
1. **Fetch/Update IP Ranges:** Downloads the fresh Bangladesh IP allocation list.
2. **Execute Camera Scan:** Scans the target IP ranges for active cameras.
3. **Exit:** Safely terminates the program.

**Scan Control Shortcuts:**
- `Ctrl+C`: ⛔ Instantly halts the scan and exits cleanly.
- `Ctrl+Z`: ⏸️ Pauses or resumes the active scan thread pool.

---

### 📁 Output & Results
- `BDALLIP.txt`: Contains all fetched Bangladesh IP ranges in CIDR format.
- Telegram Alerts: Discovered cameras are instantly sent to your Telegram bot with IP, Port, and URL.

---

### 🛡 Legal Disclaimer
This utility is built strictly for educational, research, and authorized penetration testing purposes. Always secure proper, explicit permission from network owners before conducting any scans. The author holds no responsibility for misuse.

---

### 📞 Contact & Support (যোগাযোগ)
- **Telegram Support:** https://t.me/Armanyb
- **GitHub Profile:** [github.com/Armanyb1](https://github.com/Armanyb1)
