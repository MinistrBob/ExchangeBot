from aiogram import Bot, Dispatcher
from aiogram.types import CallbackQuery
from exchangelib import Account
from telebot.utils.callback import EmailCallbackData


async def delete_email(callback: CallbackQuery, account: Account, callback_data: EmailCallbackData):
    # print(callback.message)
    email_id = callback_data.email_id
    email = account.inbox.get(id=email_id)
    email.move_to_trash()
    # account.inbox.delete(email_id)
    await callback.answer()
