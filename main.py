import asyncio
import logging
from datetime import time

from aiogram.utils.formatting import Text, Bold
from aiogram import Bot, Dispatcher, F
from exchangelib import Credentials, Account, DELEGATE, Configuration, NTLM
from telebot.utils.commands import set_commands
from telebot.handlers.callbacks import delete_email
from telebot.keyboards.inline_keyboards import get_mail_keyboard
from settings import app_settings as appset
from telebot.utils.callbackdata import EmailCallbackData

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
    # await set_commands(bot)
    await bot.send_message(appset.telegram_chat_id, 'Bot started!')


async def stop_bot(bot: Bot):
    await bot.send_message(appset.telegram_chat_id, 'Bot stopped!')


async def start_telegram_bot(dp, bot):
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


async def check_exchange_emails(account, bot):
    folder = account.inbox

    while True:  # Infinite loop
        log.debug("Checking for new emails...")
        for item in folder.filter(is_read=False):  # You may need to adjust the filter criteria
            log.info(f"=======================================================================")
            log.info(f"ID: {item.id}")
            log.info(f"NEW EMAIL: Subject: {item.subject}")
            log.debug(f"DEBUG:\n{item.subject}\n{item.text_body}")
            # Forward the email to Telegram
            # В некоторых письмах наряду с email отправителя передаётся его имя.
            if item.sender.email_address == item.sender.name:
                from_text = f"{item.sender.email_address}\n"
            else:
                from_text = f"{item.sender.email_address} [{item.sender.name}]\n"
            content = Text(
                Bold("From:\n"),
                from_text,
                Bold("Subject:\n"),
                f"{item.subject}\n",
                f"{'-'*40}\n\n",
                f"{item.text_body}"
            )
            log.debug(f"DEBUG: {content}")
            await bot.send_message(chat_id=appset.telegram_chat_id,
                                   **content.as_kwargs(), reply_markup=get_mail_keyboard(item.id))
            item.is_read = True  # Mark the email as read
            item.save()
        # Sleep for a short interval to avoid continuous checking
        await asyncio.sleep(60)  # Sleep for 60 seconds, adjust as needed


async def main():
    log.info("Starting the Telegram bot...")
    log.debug(f"Starting the Telegram bot {appset.telegram_bot_token}")

    log.info("Connecting to Exchange...")
    credentials = Credentials(username=appset.user_login, password=appset.user_password)
    config = Configuration(server=appset.smtp_server, credentials=credentials, auth_type=NTLM)
    account = Account(appset.user_email, config=config, autodiscover=False, access_type=DELEGATE)

    bot = Bot(token=appset.telegram_bot_token, parse_mode=None)
    dp = Dispatcher()
    dp.startup.register(start_bot)
    dp.shutdown.register(stop_bot)
    dp.callback_query.register(delete_email, EmailCallbackData.filter(F.action == 'delete'))
    dp['account'] = account

    log.info("Create async tasks...")
    # asyncio.run(start_telegram_bot())
    telegram_bot_task = asyncio.create_task(start_telegram_bot(dp, bot))
    exchange_task = asyncio.create_task(check_exchange_emails(account, bot))

    log.info("Run async tasks...")
    await asyncio.gather(telegram_bot_task, exchange_task)

    log.info("Closing the application...")


if __name__ == '__main__':
    asyncio.run(main())
