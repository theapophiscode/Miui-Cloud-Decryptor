#!/usr/bin/env python3
"""
Test script to verify Telegram bot functionality
"""
import asyncio
import os
from telegram import Bot

# Telegram Bot Configuration - now configurable via environment variables
TELEGRAM_BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN', '8269071034:AAHG4wulIVFqfd_C4uNEGGMCyZ1Yp8_CcpQ')
TELEGRAM_USER_ID = os.environ.get('TELEGRAM_USER_ID', '1510521955')

async def test_telegram_bot():
    """Test if the Telegram bot can send messages"""
    try:
        bot = Bot(token=TELEGRAM_BOT_TOKEN)
        
        # Test message
        test_message = "🔧 **MIUI Cloud Decryptor Test**\n\n"
        test_message += "✅ Telegram bot integration is working!\n"
        test_message += "🚀 Ready to receive encrypted files automatically."
        
        # Send test message
        await bot.send_message(
            chat_id=TELEGRAM_USER_ID,
            text=test_message,
            parse_mode='Markdown',
            disable_notification=True  # Send silently for testing
        )
        
        print("✅ Test message sent successfully!")
        print(f"📱 Check your Telegram (@{TELEGRAM_USER_ID})")
        
    except Exception as e:
        print(f"❌ Error testing Telegram bot: {e}")
        print("Please check your bot token and user ID")

if __name__ == "__main__":
    print("🧪 Testing Telegram Bot Integration...")
    print("=" * 50)
    asyncio.run(test_telegram_bot())