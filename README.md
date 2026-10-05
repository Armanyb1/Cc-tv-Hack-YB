# 📸 Arman Professional Smart Recon & RTSP Tool
An advanced, 100% silent, and high-performance network security and camera recognition tool designed for network analysis and RTSP stream generation. Developed by **Arman Yb**.

---

### 🚀 Key Features
- **100% Silent & Safe Recon:** Uses low-timeout socket connections to minimize logs and avoid heavy alerts.
- **Smart Brand Recognition:** Automatically maps open ports (80, 554, 8000, 37777, 8899) to prominent camera brands and apps including Hikvision, Dahua, V380, and generic RTSP streams.
- **Auto RTSP Link Generation:** Instantly creates playable stream links for discovered cameras.
- **Real-Time Telegram Alerts:** Built-in alert system using standard Python libraries (zero heavy external dependencies) to notify you instantly on Telegram.
- **Database Logging:** Automatically saves all active camera findings and timestamps to `arman_live_cameras.txt`.
- **Termux Optimized:** Fully compatible with Android via Termux with smooth color banner support.

---

### 📱 Installation & Setup (ইনস্টলেশন ও চালুর নিয়ম)

**For Termux (Android):**
টার্মাক্স ওপেন করে নিচের কমান্ডগুলো এক এক করে পেস্ট করো:

```
pkg update && pkg upgrade -y
```
```
pkg install python git -y
```
```
git clone [https://github.com/Armanyb1/Cc-tv-Hack-YB.git](https://github.com/Armanyb1/Cc-tv-Hack-YB.git)
```
```
cd Cc-tv-Hack-YB
```
```
python camera_tool.py
```

----

### 💳 Pricing & License (মূল্য ও লাইসেন্স প্যাকেজ)
এই টুলটি ব্যবহার করার জন্য পেইড লাইসেন্স নিতে হবে। আমাদের সাশ্রয়ী প্যাকেজগুলো দেখে নিন:
- **৭ দিন:** ১০০ টাকা
- **১ মাস (Monthly):** ৩৮০ টাকা
- **আজীবন (Lifetime):** ৭০০ টাকা
- **বিকাশ/নগদ নম্বর:** `01880374287`

**যেভাবে লাইসেন্স নিবে:**
পেমেন্ট করার পর টার্মাক্সে টুল রান করলে স্ক্রিনে বা টেলিগ্রামে যে তথ্য দেখাবে, সেটি স্ক্রিনশটসহ সরাসরি আমাদের টেলিগ্রামে পাঠিয়ে দিন। সাথে সাথে লাইসেন্স অ্যাক্টিভ করে দেওয়া হবে!

---

### 🛠️ How to Use & Menu Options
1. **Scan Local Wi-Fi (LAN) + Silent Port Mapping:** Scans your local router/network safely.
2. **Scan Custom Public / ISP Subnet Range:** Scans custom specified subnet ranges.
3. **Auto Bangladesh ISP Subnets (Silent Recon):** Preset BD ISP subnet pools for rapid analysis.
4. **View Saved Cameras Database:** Displays all saved entries from `arman_live_cameras.txt`.
5. **Exit:** Safely terminates the program.

**How to Check Live Streams:**
- Copy any generated `rtsp://...` link from the terminal, Telegram alert, or database.
- Open **VLC Media Player**, go to **"Open Network Stream"**, paste the link, and hit play!

---

### 📁 Output & Results
- `arman_live_cameras.txt`: Contains local logs of discovered devices, ports, protocols, and RTSP stream links.
- **Telegram Notifications:** Sends instant alerts directly to your configured Telegram bot.

---

### 🛡 Legal Disclaimer
This utility is built strictly for educational, research, and authorized network security testing purposes. Always secure proper, explicit permission from network owners before conducting any scans. The author holds no responsibility for misuse.

---

### 📞 Contact & Support (যোগাযোগ)
- **Telegram Support:** https://t.me/Armanyb
- **GitHub Profile:** [github.com/Armanyb1](https://github.com/Armanyb1)
