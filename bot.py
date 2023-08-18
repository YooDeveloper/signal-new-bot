import requests
import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.types import InputFile

from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.fsm_storage.redis import RedisStorage2

from tgbot.config import load_config
from tgbot.filters.admin import AdminFilter
from tgbot.handlers.admin import register_admin
from tgbot.handlers.echo import register_echo
from tgbot.handlers.user import register_user
from tgbot.middlewares.environment import EnvironmentMiddleware

logger = logging.getLogger(__name__)

from air import *
from pil import *

def register_all_middlewares(dp, config):
    dp.setup_middleware(EnvironmentMiddleware(config=config))


def register_all_filters(dp):
    dp.filters_factory.bind(AdminFilter)


def register_all_handlers(dp):
    register_admin(dp)
    register_user(dp)

    register_echo(dp)


async def repeat(interval, func, *args, **kwargs):
    """Run func every interval seconds.

    If func has not finished before *interval*, will run again
    immediately when the previous iteration finished.

    *args and **kwargs are passed as the arguments to func.
    """
    while True:
        await asyncio.gather(
            func(*args, **kwargs),
            asyncio.sleep(interval),
        )

async def main():
    logging.basicConfig(
        level=logging.INFO,
        format=u'%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s',
    )
    logger.info("Starting bot")
    config = load_config(".env")

    storage = RedisStorage2() if config.tg_bot.use_redis else MemoryStorage()
    bot = Bot(token=config.tg_bot.token, parse_mode='HTML')
    dp = Dispatcher(bot, storage=storage)

    bot['config'] = config

    register_all_middlewares(dp, config)
    register_all_filters(dp)
    register_all_handlers(dp)
    
    async def f():
        try:
            await asyncio.sleep(1)
            print('run')
            response = requests.get('https://garantex.io/api/v2/depth?market=usdtrub')
            api_val = float(response.json()['asks'][0]['price'])
            print(api_val)
            for task in Task.all():
                res = ""
                chat_id = task.channel
                text = task.body
                for package in task.packages:
                    print(package.var_count)
                    if package.var_count == 1:
                        for logic in package.logics:
                            tst = api_val + round(api_val * logic.percent / 100, 2) + logic.margin
                            result = round(float(tst) / logic.val, 2)
                            res+=f"{logic.title}: {result}\n"
                            res = addText(str(result))
                            photo = InputFile(res)
                            if logic.last_val == result:
                                print('не изменилось')
                            else:
                                await bot.send_photo(chat_id, photo=photo, caption=logic.title)
                            lg = Logic.from_id(logic.id)
                            lg.last_val = result
                            lg.save()
                # res+=f"\n{task.body}"
                # if task.logics.count() > 0:
                # await bot.send_message(chat_id, str(res))

        except Exception as e: 
            print(e)

    t1 = asyncio.ensure_future(repeat(10, f))

    # start
    try:
        await dp.start_polling()
    finally:
        await dp.storage.close()
        await dp.storage.wait_closed()
        await bot.session.close()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.error("Bot stopped!")
