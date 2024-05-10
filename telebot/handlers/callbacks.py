from aiogram import Bot, Dispatcher
from aiogram.types import CallbackQuery
from exchangelib import Account
from telebot.utils.callbackdata import EmailCallbackData
import logging
import db
import traceback

log = logging.getLogger("main")


async def delete_email(callback: CallbackQuery, account: Account, callback_data: EmailCallbackData):
    # print(callback.message)
    try:
        id_ = callback_data.email_id.split('=')[-1]
        result = db.execute_select(f"SELECT * FROM email where id='{id_}'")
        if result:  # Если письма нет в БД
            email_id = result[0]
            log.debug(f"email_id={email_id}")
            email = account.inbox.get(id=email_id)
            log.debug(f"email={email}; type(email)={type(email)}")
            email.move_to_trash()
            # account.inbox.delete(email_id)
            await callback.answer()
        else:
            await callback.message.answer(f"Не нахожу письмо с id={id_} в базе данных.")
    except Exception as e:
        await bot.send_message(appset.telegram_chat_id, f'ERROR:{e}\n{traceback.format_exc()}')
