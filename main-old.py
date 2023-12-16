import asyncio
import sqlite3
import os
import time
import multiprocessing

from aiogram import Bot, Dispatcher, types
from exchangelib import Credentials, Account, DELEGATE, HTMLBody

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

# Replace these with your actual values
DATABASE_PATH = 'path/to/your/database.db'
EXCHANGE_EMAIL = 'your_exchange_email@example.com'
EXCHANGE_PASSWORD = 'your_exchange_password'
TELEGRAM_BOT_TOKEN = 'your_telegram_bot_token'
TELEGRAM_CHAT_ID = 7777


def exchange_mail(user):
    # Если у пользователя в БД указана почта,
    # то она отличается от username+app_settings.email_domain и используется она.
    if user[3]:
        exchange_email = user[3]
    else:
        exchange_email = f"{user[1]}@{app_settings.email_domain}"

    credentials = Credentials(username=f"{user[1]}\{app_settings.domain}", password=user[2])
    config = Configuration(server=app_settings.smtp_server, credentials=credentials, auth_type=NTLM)
    account = Account(exchange_email, config=config, autodiscover=False, access_type=DELEGATE)

    folder = account.inbox

    while True:  # Infinite loop
        for item in folder.filter(is_read=False):  # You may need to adjust the filter criteria
            # Forward the email to Telegram
            forward_to_telegram(item.subject, item.body, TELEGRAM_CHAT_ID)
            item.is_read = True  # Mark the email as read
            item.save()
        # Sleep for a short interval to avoid continuous checking
        time.sleep(60)  # Sleep for 60 seconds, adjust as needed


def forward_to_telegram(subject, body, chat_id):
    bot = Bot(token=TELEGRAM_BOT_TOKEN)
    text = f"New Email:\n\nSubject: {subject}\n\nBody: {body}"

    bot.send_message(chat_id=chat_id, text=text)


def start_telegram_bot():
    bot = Bot(token=TELEGRAM_BOT_TOKEN)
    dp = Dispatcher(bot)

    @dp.message_handler(commands=['start'])
    async def on_start(message: types.Message):
        await message.answer("Hi!")

    bot.polling()


def main():
    # Access the SQLite database
    conn = sqlite3.connect(app_settings.database_path)
    cursor = conn.cursor()

    # Replace 'Users' with your actual table name
    # (1, 'ivanov', 'Pa$$w0rd', None)
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()

    # Start a separate process for each user
    processes = []
    for user in users:
        process = multiprocessing.Process(target=exchange_mail, args=(user,))
        processes.append(process)
        process.start()

    # Start the Telegram bot in the main process
    start_telegram_bot()

    # Wait for all processes to finish
    for process in processes:
        process.join()


if __name__ == '__main__':
    main()

