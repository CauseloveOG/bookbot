from copy import deepcopy

from aiogram import F, Router
from aiogram.filters import Command, CommandStart
from aiogram.types import CallbackQuery, Message

from database.database import user_dict_template, users_db
from filters.filters import IsDigitCallbackData, IsDelBookmarksCallbackData
from keyboards.bookmarks_kb import (create_bookmarks_keyboard,
                                    create_edit_keyboard)
from keyboards.pagination_kb import create_pagination_keyboard
from lexicon.lexicon import LEXICON
from services.file_handling import book

router = Router()

# Хендлер команды /start
# Добавляет пользователя в базу данных, если его там нет
# Отправляет приветственное сообщение
@router.message(CommandStart())
async def process_start_command(message: Message):
    await message.answer(LEXICON[message.text])
    if message.from_user.id not in users_db:
        users_db[message.from_user.id] = deepcopy(user_dict_template)


# Хендлер команды /help
# Отправляет пользователю список доступных команд
@router.message(Command(commands='help'))
async def process_help_command(message: Message):
    await message.answer(LEXICON[message.text])


# Хендлер команды /beginning
# Отправляет пользователю первую страницу с кнопками
@router.message(Command(commands='beginning'))
async def process_beginning_command(message: Message):
    users_db[message.from_user.id]['page'] = 1
    text = book[1]
    await message.answer(
        text=text,
        reply_markup=create_pagination_keyboard(
            'backward',
            f'{users_db[message.from_user.id]['page']}/{len(book)}',
            'forward'
        )
    )


# Хендлер команды /continue
# Отправляет страницу, на которой пользователь остановился
@router.message(Command(commands='continue'))
async def process_continue_command(message: Message):
    text = book[users_db[message.from_user.id]['page']]
    await message.answer(
        text=text,
        reply_markup=create_pagination_keyboard(
            'backward',
            f'{users_db[message.from_user.id]['page']}/{len(book)}',
            'forward'
        )
    )


# Хендлер команды /bookmarks
# Отправляет список закладок или сообщение об их отсутствии
@router.message(Command(commands='bookmarks'))
async def process_bookmarks_command(message: Message):
    if users_db[message.from_user.id]['bookmarks']:
        await message.answer(
            text=LEXICON[message.text],
            reply_markup=create_bookmarks_keyboard(
                *users_db[message.from_user.id]['bookmarks']
            )
        )
    else:
        await message.answer(text=LEXICON['no_bookmarks'])


# Обработка нажатия инлайн кнопки Вперед
@router.callback_query(F.data == 'forward')
async def process_forward_press(callback: CallbackQuery):
    if users_db[callback.from_user.id]['page'] < len(book):
        users_db[callback.from_user.id]['page'] += 1
        text = book[users_db[callback.from_user.id]['page']]
        await callback.message.edit_text(
            text=text,
            reply_markup=create_pagination_keyboard(
                'backward',
                f'{users_db[callback.from_user.id]['page']}/{len(book)}',
                'forward'
            )
        )
    await callback.answer()


# Обработка нажатия инлайн кнопки Назад
@router.callback_query(F.data == 'backward')
async def process_backward_press(callback: CallbackQuery):
    if users_db[callback.from_user.id]['page'] > 1:
        users_db[callback.from_user.id]['page'] -= 1
        text = book[users_db[callback.from_user.id]['page']]
        await callback.message.edit_text(
            text=text,
            reply_markup=create_pagination_keyboard(
                'backward',
                f'{users_db[callback.from_user.id]['page']}/{len(book)}',
                'forward'
            )
        )
    await callback.answer()


# Обработка нажатия кнопки с текущей страницей
# добавление страницы в закладки
@router.callback_query(lambda x: '/' in x.data and x.data.replace('/', '').isdigit())
async def process_page_press(callback: CallbackQuery):
    users_db[callback.from_user.id]['bookmarks'].add(
        users_db[callback.from_user.id]['page']
    )
    await callback.answer('Страница добавлена в закладки')


# Обработка нажатия инлайн-кнопки с закладкой из списка закладок
@router.callback_query(IsDigitCallbackData())
async def process_bookmark_press(callback:CallbackQuery):
    text = book[int(callback.data)]
    users_db[callback.from_user.id]['page'] = int(callback.data)
    await callback.message.edit_text(
        text=text,
        reply_markup=create_pagination_keyboard(
            'backward',
            f'{users_db[callback.from_user.id]['page']}/{len(book)}',
            'forward'
        )
    )


# Обработка нажатия кнопки Редактировать под списком закладок
@router.callback_query(F.data == 'edit_bookmarks')
async def process_edit_press(callback: CallbackQuery):
    await callback.message.edit_text(
        text=LEXICON[callback.data],
        reply_markup=create_edit_keyboard(
            *users_db[callback.from_user.id]['bookmarks']
        )
    )


# Обработка нажатия кнопки Отменить во время работы с Закладками
@router.callback_query(F.data == 'cancel')
async def process_cancel_press(callback: CallbackQuery):
    await callback.message.edit_text(text=LEXICON['cancel_text'])


# Обработка нажатия кнопки с закладкой из списка к удалению
@router.callback_query(IsDelBookmarksCallbackData())
async def process_del_bookmarks_press(callback:CallbackQuery):
    users_db[callback.from_user.id]['bookmarks'].remove(
        int(callback.data[:-3])
    )
    if users_db[callback.from_user.id]['bookmarks']:
        await callback.message.edit_text(
            text=LEXICON['/bookmarks'],
            reply_markup=create_edit_keyboard(
                *users_db[callback.from_user.id]['bookmarks']
            )
        )
    else:
        await callback.message.edit_text(text=LEXICON['no_bookmarks'])