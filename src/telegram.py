import asyncio

from aiogram import Bot, Dispatcher, filters, types

from settings import Settings
from users.service import UserService

bot = Bot(Settings.TELEGRAM_BOT_TOKEN)
dp = Dispatcher()


@dp.message(filters.CommandStart(deep_link=True))
async def handler(message: types.Message, command: filters.CommandObject):
    payload = message.text.split(' ')[1]

    async with UserService() as service:
        user = message.from_user
        await service.link_telegram(user.id, user.full_name, user.username, payload)

        await message.answer("Ваш аккаунт успешно привязан!")


@dp.message()
async def handle_any(message: types.Message):
    await message.answer(
        'Привет!'
    )


async def start_bot():
    await dp.start_polling(bot)


async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
