from aiogram import Bot, Dispatcher
from aiogram.methods import DeleteMessage
from aiogram.types import CallbackQuery
from exchangelib import Account
from telebot.utils.callbackdata import EmailCallbackData
import logging
import db
import traceback
from settings import app_settings as appset

log = logging.getLogger("main")


async def delete_email(callback: CallbackQuery, account: Account, callback_data: EmailCallbackData, bot: Bot):
    # print(callback.message)
    log.info("Delete message")
    try:
        id_ = callback_data.email_id.split('=')[-1]
        result = db.execute_select(f"SELECT * FROM email where id='{id_}'")
        log.info(f"Try delete message={result}")
        # (1, 'AAMkADBkMWZkNjg2...', '178', '2024-05-10 12:25:37', '2024-05-10 12:25:37')
        if result:  # Если письма нет в БД
            email_id = result[0][1]
            email = account.inbox.get(id=email_id)
            # log.debug(f"email={email}; type(email)={type(email)}")
            email.move_to_trash()
            # account.inbox.delete(email_id)
            await callback.answer()
            await bot(DeleteMessage(chat_id=callback.message.chat.id, message_id=result[0][2]))
            # await callback.message.answer(f"Письмо с id={id_} и email_id={email_id} удалено.")
            log.info(f"Message deleted")
        else:
            message = f"Не нахожу письмо с id={id_} в базе данных."
            log.error(message)
            await callback.message.answer(message)
    except Exception as e:
        message = f'ERROR:{e}\n{traceback.format_exc()}'
        log.error(message)
        await bot.send_message(appset.telegram_chat_id, message)
