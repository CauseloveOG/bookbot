from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from lexicon.lexicon import LEXICON


# Функция генерации клавиатуры для страницы книги
def create_pagination_keyboard(*buttons: str) -> InlineKeyboardMarkup:
    # Инициализация билдера
    kb_builder = InlineKeyboardBuilder()
    # Добавление в билдер ряд с кнопками
    kb_builder.row(*[InlineKeyboardButton(
        text=LEXICON[button] if button in LEXICON else button,
        callback_data=button) for button in buttons]
    )
    # Возврат объекта инлайн клавиатуры
    return kb_builder.as_markup()