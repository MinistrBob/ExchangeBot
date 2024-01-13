from aiogram.utils.keyboard import InlineKeyboardBuilder
from telebot.utils.callbackdata import EmailCallbackData


def get_mail_keyboard(email_id):
    print(f"EMAIL_ID={email_id}")
    keyboard_builder = InlineKeyboardBuilder()
    # keyboard_builder.button(text=f"DELETE", callback_data=f"id_{email_id}")
    keyboard_builder.button(text=f"DELETE", callback_data=EmailCallbackData(action="delete", email_id=email_id).pack())
    keyboard_builder.adjust(1)
    return keyboard_builder.as_markup()
