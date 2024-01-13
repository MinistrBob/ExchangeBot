from aiogram.filters.callback_data import CallbackData


class EmailCallbackData(CallbackData, prefix="email"):
    email_id: str
    action: str
