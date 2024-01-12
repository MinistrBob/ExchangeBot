from aiogram import Bot, Dispatcher
from aiogram.types import CallbackQuery
from exchangelib import Account


async def delete_email(callback: CallbackQuery, account: Account):
    # print(callback.message)
    email_id = callback.data.split('_')[1]
    email = account.inbox.get(id=email_id)
    email.move_to_trash()
    # account.inbox.delete(email_id)
    await callback.answer()
