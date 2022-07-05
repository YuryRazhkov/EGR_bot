import time

from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

from request_moduls.egr_request import request_to_registr
from request_moduls.tax_inspspection_request import request_to_tax_inspection
from request_moduls.just_bel_request import request_just_bel
from config import TOKEN
import logging


logger = logging.getLogger('botlog')

logger.debug('Start')
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

logger.debug('Start')








@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    await message.reply("Здравствуйте!\nВведите УНП (9 цифр)")


@dp.message_handler()
async def unp(msg: types.Message):
    regnum = msg.text
    user = f'{str(msg.from_user.id)} {msg.from_user.first_name} {msg.from_user.last_name}'
    logger.debug(f'user: {user}; request text: {regnum}')

    if regnum.isnumeric() and len(regnum) == 9:
        logger.debug('request text is correct')
        await bot.send_message(msg.from_user.id, 'Собираю информацию. Ожидайте')
        logger.debug('start function request_to_tax_inspection')
        await bot.send_message(msg.from_user.id, 'Запрашиваю ИМНС')
        await bot.send_message(msg.from_user.id, request_to_tax_inspection(regnum))
        time.sleep(0.5)
        logger.debug('start function request_to_registr')
        await bot.send_message(msg.from_user.id, 'Запрашиваю ЕГР. Подождите полминутки')
        await bot.send_message(msg.from_user.id, request_to_registr(regnum))
        time.sleep(0.5)
        logger.debug('start function request_just_bel')
        await bot.send_message(msg.from_user.id, 'Ищу объявления о ликвидации')
        await bot.send_message(msg.from_user.id, request_just_bel(regnum))
        logger.debug(f'user: {user}; end request')
    else:
        await bot.send_message(msg.from_user.id, 'Не корректное значение. Введите УНП (9 цифр)!')
        logger.debug('request text is NOT correct')
        logger.debug(f'user: {user}; end request')

if __name__ == '__main__':
    executor.start_polling(dp)
