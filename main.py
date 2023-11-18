import asyncio
import sqlite3
from multiprocessing import Process  # Import Process from multiprocessing

from aiogram import Bot, Dispatcher, types
from exchangelib import DELEGATE, Credentials, Account

import custom_logger
from settings import app_settings

# Settings
print("Starting to set up the application...")
appset = app_settings
if appset.DEBUG:
    print(f"app settings={appset}")

# Logging
print("Starting to configure the application logging...")
log = custom_logger.get_logger(appset)

# Working
log.info("The application is running")



# Replace these with your actual Microsoft Exchange Server credentials
EXCHANGE_EMAIL = 'your_exchange_email@example.com'
EXCHANGE_PASSWORD = 'your_exchange_password'
EXCHANGE_SERVER = 'your_exchange_server_url'

# Initialize the SQLite database for storing Exchange credentials
conn = sqlite3.connect('exchange_credentials.db')
cursor = conn.cursor()
cursor.execute('CREATE TABLE IF NOT EXISTS credentials (user_id INT, email TEXT)')
conn.commit()

# Initialize the Telegram bot with your token
TELEGRAM_BOT_TOKEN = 'your_telegram_bot_token'
bot = Bot(token=TELEGRAM_BOT_TOKEN)
dp = Dispatcher(bot)


# Define the ExchangeMail procedure
async def ExchangeMail():,
    # Connect to the Exchange server
    credentials = Credentials(EXCHANGE_EMAIL, EXCHANGE_PASSWORD)
    account = Account(EXCHANGE_EMAIL, credentials=credentials, autodiscover=True, access_type=DELEGATE)

    # Start monitoring for new emails
    folder = account.inbox  # You can change this to the folder you want to monitor
    async for item in folder.filter(is_read=False):
        # Forward the new email to Telegram chat with chat_id=7777
        await bot.send_message(chat_id=7777, text=f"New email received:\n{item.subject}\n{item.text_body}")


# Define the /start command handler
@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    user_id = message.from_user.id

    # Check if the user's credentials are already saved
    cursor.execute('SELECT email FROM credentials WHERE user_id = ?', (user_id,))
    existing_email = cursor.fetchone()

    if existing_email:
        await message.answer(f'Your Exchange Server email is already saved: {existing_email[0]}')
    else:
        await message.answer('Please enter your Exchange Server email:')

        # Register a handler to collect the email from the user
        @dp.message_handler(lambda message: message.from_user.id == user_id)
        async def save_exchange_email(message: types.Message):
            email_input = message.text.strip()
            cursor.execute('INSERT INTO credentials (user_id, email) VALUES (?, ?)', (user_id, email_input))
            conn.commit()
            await message.answer(f'Your Exchange Server email ({email_input}) has been saved.')

        # Remove the temporary handler after the email is collected
        dp.remove_handler(save_exchange_email)


if __name__ == '__main__':
    exchange_process = Process(target=lambda: asyncio.run(ExchangeMail()))
    exchange_process.start()

    from aiogram import executor

    executor.start_polling(dp, skip_updates=True)
