from aiogram import Router
from aiogram.types import Message

router = Router()

# Хендлер реагирует на любые сообщения не предусмотренные логикой
@router.message()
async def send_echo(message: Message):
    await message.answer(f'Это эхо! {message.text}')