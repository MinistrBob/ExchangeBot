from aiogram.utils.keyboard import InlineKeyboardBuilder


def get_mail_keyboard(email_id):
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.button(text=f"DELETE", callback_data=f"id_{email_id}")
    keyboard_builder.adjust(1)
    return keyboard_builder.as_markup()
