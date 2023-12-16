import asyncio
import logging

from aiogram import Bot, Dispatcher, types
from exchangelib import Credentials, Account, DELEGATE, HTMLBody
from telebot.utils.commands import set_commands

from settings import app_settings as appset

# Settings
print("Starting to set up the application...")
if appset.DEBUG:
    print(f"app settings={appset}")

# Logging
print("Starting to configure the application logging...")
# Define the logging level
if appset.DEBUG:
    log_level = logging.DEBUG
else:
    log_level = logging.INFO
logging.basicConfig(level=log_level,
                    format='%(asctime)s|%(levelname)-5s|%(funcName)s| %(message)s',
                    datefmt='%d.%m.%Y %I:%M:%S')
log = logging.getLogger(__name__)

# Working
log.info("The application is running")


async def start_bot(bot: Bot):
    await set_commands(bot)
    await bot.send_message(appset.telegram_admin_id, 'Bot started!')


async def stop_bot(bot: Bot):
    await bot.send_message(appset.telegram_admin_id, 'Bot stopped!')


async def start_telegram_bot():
    log.info("Starting the Telegram bot...")
    log.debug(f"Starting the Telegram bot {appset.telegram_bot_token}")
    bot = Bot(token=appset.telegram_bot_token, parse_mode='HTML')
    dp = Dispatcher()
    dp.startup.register(start_bot)
    dp.shutdown.register(stop_bot)
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == '__main__':
    asyncio.run(start_telegram_bot())

    credentials = Credentials(username=appset.user_login, password=appset.user_password)
    config = Configuration(server=appset.smtp_server, credentials=credentials, auth_type=NTLM)
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
