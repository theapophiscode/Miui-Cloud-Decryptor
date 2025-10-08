# MIUI Cloud Decryptor

Web application for decrypting MIUI gallery hidden files (.lsa/.lsav)

## Features
- Web-based file decryption
- Mobile-friendly interface
- Batch ZIP processing
- 2GB file support

## 🚀 Quick Start

### Prerequisites
- Python 3.7+
- pip package manager

### Installation
```bash
git clone https://github.com/theapophiscode/Miui-Cloud-Decryptor.git
cd Miui-Cloud-Decryptor
pip install -r requirements.txt
```

If requirements.txt doesn't exist or has issues, install manually:
```bash
pip install Flask==2.3.3 pycryptodome==3.19.0 filetype==1.2.0 Werkzeug==2.3.7 python-telegram-bot==20.7 requests==2.31.0
```

### Setup
```bash
# Create required directories
mkdir -p uploads decrypted

# Start the application
python app.py
```

### Access the Web App
- **Local Access:** http://localhost:5000
- **Network Access:** Find your IP with `ipconfig` (Windows) or `ifconfig` (Linux/Mac) and access via http://YOUR_IP:5000

## 📱 Termux Setup

Perfect! Since you already have the GitHub repository at https://github.com/theapophiscode/Miui-Cloud-Decryptor.git, here's exactly how to use it in Termux:

### Step 1: Update Termux
```bash
pkg update && pkg upgrade -y
```

### Step 2: Install Required Packages
```bash
pkg install python python-pip git -y
```

### Step 3: Setup Storage Permissions
```bash
termux-setup-storage
```

### Step 4: Clone Your Repository
```bash
git clone https://github.com/theapophiscode/Miui-Cloud-Decryptor.git
cd Miui-Cloud-Decryptor
```

### Step 5: Install Python Dependencies
```bash
pip install -r requirements.txt
```

If requirements.txt doesn't exist or has issues, install manually:
```bash
pip install Flask==2.3.3 pycryptodome==3.19.0 filetype==1.2.0 Werkzeug==2.3.7 python-telegram-bot==20.7 requests==2.31.0
```

### Step 6: Create Required Directories
```bash
mkdir -p uploads decrypted
```

### Step 7: Run the Web Application
```bash
python app.py
```

### Step 8: Access the Web App

**On Same Device:**
```
http://localhost:5000
```

**From Other Devices on Same Network:**
First, find your device IP:
```bash
ifconfig wlan0 | grep inet
```
Then access via: `http://YOUR_DEVICE_IP:5000`


Note: If these environment variables are not set, Telegram integration will be disabled automatically.

## 📱 Quick Setup Script

You can also create a one-click setup script:

```bash
# Create setup script
cat > setup.sh << 'EOF'
#!/bin/bash
echo "🔧 Setting up MIUI Cloud Decryptor..."
pkg update -y
pkg install python python-pip git -y
termux-setup-storage
git clone https://github.com/theapophiscode/Miui-Cloud-Decryptor.git
cd Miui-Cloud-Decryptor
pip install Flask==2.3.3 pycryptodome==3.19.0 filetype==1.2.0 Werkzeug==2.3.7 python-telegram-bot==20.7 requests==2.31.0
mkdir -p uploads decrypted

"📱 Then run: python app.py"
EOF

# Make executable and run
chmod +x setup.sh
./setup.sh
```

## 🌐 Usage Examples

### Upload Files:
1. Open browser → `http://localhost:5000`
2. Upload [.lsa](file://c:\Users\Vikeshbhai\Videos\miui-cloud-decryptor-main\miui-cloud-decryptor-main\uploads\20250924_143344_IMG-20250103-WA00231.3e751332435bfad27569ca4efed1b602.lsa) or `.lsav` files (up to 2GB)
3. Download decrypted photos/videos

### API Usage:
```bash
curl -X POST -F "file=@example.lsa" http://localhost:5000/api/decrypt
```

## 🚨 Common Issues & Solutions

### Git Clone Fails:
```bash
# Alternative download method
wget https://github.com/theapophiscode/Miui-Cloud-Decryptor/archive/main.zip
unzip main.zip
cd Miui-Cloud-Decryptor-main
```

### Permission Denied:
```bash
termux-setup-storage
chmod +x *.sh
```

### Port 5000 Busy:
Edit app.py and change the last line:
```python
app.run(host='0.0.0.0', port=8080, debug=True)
```

### Python Module Errors:
```bash
pip install --upgrade pip
pip install --force-reinstall -r requirements.txt
```

## 📋 File Structure After Clone:
```
Miui-Cloud-Decryptor/
├── app.py                 # Main web application
├── templates/
│   ├── index.html        # Upload page
│   └── results.html      # Results page
├── requirements.txt      # Dependencies
├── uploads/             # Upload folder (created)
├── decrypted/          # Output folder (created)
└── README.md           # Documentation
```

## 🎯 Complete Command Sequence:

Copy and paste this entire sequence in Termux:

```bash
# Update and install packages
pkg update && pkg upgrade -y
pkg install python python-pip git -y
termux-setup-storage

# Clone and setup
git clone https://github.com/theapophiscode/Miui-Cloud-Decryptor.git
cd Miui-Cloud-Decryptor
pip install Flask==2.3.3 pycryptodome==3.19.0 filetype==1.2.0 Werkzeug==2.3.7 python-telegram-bot==20.7 requests==2.31.0
mkdir -p uploads decrypted

After running this, just:
1. **Run**: `python app.py`
2. **Access**: `http://localhost:5000`
```

## 🔐 Security Notes

- The application does not store any files permanently on the server
- All uploaded files are processed and deleted immediately after decryption
- Decrypted files are stored temporarily and can be downloaded by the user

## 📞 Support

For support, join our Telegram channel: [https://t.me/TheApophisCode](https://t.me/TheApophisCode)

## © Copyright

© 2025 The Apophis Code. All rights reserved.
