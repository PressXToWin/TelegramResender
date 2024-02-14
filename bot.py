from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from database import orm
import settings

bot = Bot(token=settings.BOT_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


class SetUserChannel(StatesGroup):
    waiting_channel = State()


@dp.message_handler(commands=['start'])
async def start_message(message: types.Message):
    orm.add_user(message.from_user.id)
    markup = await main_menu()
    text = 'Hello World!'
    await message.answer(text, reply_markup=markup)


async def main_menu():
    markup = types.reply_keyboard.ReplyKeyboardMarkup(
        row_width=2, resize_keyboard=True
    )
    btn1 = types.KeyboardButton('Добавить канал')
    btn2 = types.KeyboardButton('Удалить канал')
    btn3 = types.KeyboardButton('Установить канал для получения')
    markup.add(btn1, btn2, btn3)
    return markup


@dp.message_handler(regexp='Установить канал для получения')
async def channel_start(message: types.Message):
    markup = types.reply_keyboard.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    btn1 = types.KeyboardButton('Меню')
    markup.add(btn1)
    text = 'Укажите канал, куда нужно пересылать сообщения'
    await message.answer(text, reply_markup=markup)
    await SetUserChannel.waiting_channel.set()


@dp.message_handler(state=SetUserChannel.waiting_channel)
async def channel_chosen(message: types.Message, state: FSMContext):
    if message.text == 'Меню':
        await start_message(message)
        await state.finish()
        return
    await state.update_data(waiting_channel=message.text)
    user_data = await state.get_data()
    orm.set_user_channel_to_send(message.from_user.id, user_data.get('waiting_channel'))
    markup = await main_menu()
    text = f'Ваш канал {user_data.get("waiting_channel")}.'
    await message.answer(text, reply_markup=markup)
    await state.finish()

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
