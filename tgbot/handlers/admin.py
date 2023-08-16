from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from asyncio import sleep
from aiogram.types import (
    InputFile, 
    CallbackQuery, 
    Message, 
    InlineKeyboardMarkup, 
    InlineKeyboardButton
)

from db.models import *



class EditBody(StatesGroup):
    input = State()

class AddTask(StatesGroup):
    input = State()

class AddLogic(StatesGroup):
    input = State()

class EditLogic(StatesGroup):
    input = State()

def confirm_btns(target_id):
    markup = InlineKeyboardMarkup(row_width=2)
    markup.row(
        InlineKeyboardButton(text=f"Да", callback_data=f"delete_task:{target_id}:yes"),
        InlineKeyboardButton(text=f"Отмена", callback_data=f"show_task:{target_id}"),
    )

    return markup

def confirm_log_btns(target_id):
    markup = InlineKeyboardMarkup(row_width=2)
    markup.row(
        InlineKeyboardButton(text=f"Да", callback_data=f"delete_logic:{target_id}:yes"),
        InlineKeyboardButton(text=f"Отмена", callback_data=f"show_logic:{target_id}"),
    )

    return markup

def admin_keyboard():
    markup = InlineKeyboardMarkup(row_width=2)
    for task in Task.all():
        markup.row(
            InlineKeyboardButton(text=f"{task.channel}", callback_data=f"show_task:{task.id}"),
        )
    markup.row(
        InlineKeyboardButton(text=f"Добавить канал", callback_data=f"add_task"),
    )

    return markup

def task_keyboard(task_id):
    markup = InlineKeyboardMarkup(row_width=2)
    task = Task.find(task_id)
    for logic in task.logics:
        markup.row(
            InlineKeyboardButton(text=f"{logic.title}", callback_data=f"show_logic:{logic.id}"),
        )
    markup.row(
        InlineKeyboardButton(text=f"Добавить формулу", callback_data=f"add_logic:{task_id}"),
        InlineKeyboardButton(text=f"Изменить текст", callback_data=f"edbo:{task_id}"),
    )
    markup.row(
        InlineKeyboardButton(text=f"Удалить канал", callback_data=f"delete_task:{task_id}:confirm"),
        InlineKeyboardButton(text=f"Назад", callback_data=f"admin"),
    )
    return markup

def logic_keyboard(logic_id):
    logic = Logic.find(logic_id)
    markup = InlineKeyboardMarkup(row_width=2)
    markup.row(
        InlineKeyboardButton(text=f"Название", callback_data=f"edit:logic:{logic_id}:title"),
        InlineKeyboardButton(text=f"Процент", callback_data=f"edit:logic:{logic_id}:percent"),
    )
    markup.row(
        InlineKeyboardButton(text=f"Наценка руб", callback_data=f"edit:logic:{logic_id}:margin"),
        InlineKeyboardButton(text=f"Делитель", callback_data=f"edit:logic:{logic_id}:val"),
    )
    markup.row(
        InlineKeyboardButton(text=f"Удалить", callback_data=f"delete_logic:{logic.id}:confirm"),
        InlineKeyboardButton(text=f"Назад", callback_data=f"show_task:{logic.task.id}"),
    )
    return markup

async def admin_start(message: Message):
    await message.answer('Проверки', reply_markup=admin_keyboard())

async def admin_dp(call: CallbackQuery, state: FSMContext):
    await call.message.edit_text('Проверки', reply_markup=admin_keyboard())

async def show_task_dp(call: CallbackQuery, state: FSMContext):
    task_id = call.data.split(':')[1]
    task = Task.find(task_id)
    await call.message.edit_text(f"{task.channel}\n{task.body}", reply_markup=task_keyboard(task_id))


async def show_logic_dp(call: CallbackQuery, state: FSMContext):
    logic_id = call.data.split(':')[1]
    logic = Logic.find(logic_id)
    text = [
        f"Формула {logic.title}\n(N + {logic.percent} + {logic.margin}) / {logic.val}"
    ]
    await call.message.edit_text("\n".join(text), reply_markup=logic_keyboard(logic_id))


async def edit_dp(call: CallbackQuery, state: FSMContext):
    logic_id = call.data.split(':')[2]
    await call.message.edit_text("Введите новое значение")
    await EditLogic.input.set()
    async with state.proxy() as data:
        data['logic_id'] = logic_id
        data['target'] = call.data.split(':')[3]

async def edit_input_mh(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        logic_id = data['logic_id']
        logic = Logic.find(logic_id)
        if data['target'] == 'title':
            logic.title = message.text
            logic.save()
        elif data['target'] == 'percent':
            logic.percent = message.text
            logic.save()
        elif data['target'] == 'margin':
            logic.margin = message.text
            logic.save()
        elif data['target'] == 'val':
            logic.val = message.text
            logic.save()
        text = [
            f"{logic.title}",
            f"Формула (N + {logic.percent} + {logic.margin}) / {logic.val}"
        ]
        await message.answer("\n".join(text), reply_markup=logic_keyboard(logic_id))
        await state.reset_state()

async def add_logic_dp(call: CallbackQuery, state: FSMContext):
    task_id = call.data.split(':')[1]
    await call.message.edit_text("Введите формулу строго в формате: название|процент|рублевая накрутка|делитель")
    await AddLogic.input.set()
    async with state.proxy() as data:
        data['task_id'] = task_id

async def add_logic_input_mh(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        task_id = data['task_id']
        try:
            title = message.text.split('|')[0]
            percent = message.text.split('|')[1]
            margin = message.text.split('|')[2]
            val = message.text.split('|')[3]
            Logic.create(
                task_id = task_id,
                title=title,
                percent=percent,
                margin=margin,
                val=val
            )
            task = Task.find(task_id)
            await message.answer(f"{task.channel}\n{task.body}", reply_markup=task_keyboard(task_id))
        except:
            await message.answer('Введите формулу строго в формате: название|процент|рублевая накрутка|делитель')


async def add_task_dp(call: CallbackQuery, state: FSMContext):
    await call.message.edit_text("Введите id канала с - (чтобы узнать - отправьте боту @getmyid_bot пост из канала) # текст\n\nПример: -115765674654#Кастомный текст")
    await AddTask.input.set()

async def add_task_input_mh(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        try:
            channel = message.text.split('#')[0]
            body = message.text.split('#')[1]
            Task.create(
                channel = channel,
                body=body
            )
            await message.answer('Проверки', reply_markup=admin_keyboard())
        except:
            await message.answer('что-то пошло не так')

async def delete_task_dp(call: CallbackQuery, state: FSMContext):
    action = call.data.split(':')[2]
    task_id = call.data.split(':')[1]
    if action == 'confirm':
        await call.message.edit_text('Удалить канал ?', reply_markup=confirm_btns(task_id))
    else:
        task = Task.find(task_id)
        task.delete()
        await call.message.edit_text('Проверки', reply_markup=admin_keyboard())

async def delete_logic_dp(call: CallbackQuery, state: FSMContext):
    action = call.data.split(':')[2]
    logic_id = call.data.split(':')[1]
    if action == 'confirm':
        await call.message.edit_text('Удалить формулу ?', reply_markup=confirm_log_btns(logic_id))
    else:
        logic = Logic.find(logic_id)
        task = logic.task
        logic.delete()
        await call.message.edit_text(f"{task.channel}\n{task.body}", reply_markup=task_keyboard(task.id))


async def edit_body_dp(call: CallbackQuery, state: FSMContext):
    task_id = call.data.split(':')[1]
    await call.message.edit_text("Введите новый текст")
    await EditBody.input.set()
    async with state.proxy() as data:
        data['task_id'] = task_id

async def edit_body_mh(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        task_id = data['task_id']
        task = Task.find(task_id)
        task.body = message.text
        task.save()
        await message.answer(f"{task.channel}\n{task.body}", reply_markup=task_keyboard(task.id))

def register_admin(dp: Dispatcher):
    dp.register_message_handler(admin_start, commands=["tasks"], state="*")
    dp.register_callback_query_handler(admin_dp, text_startswith="admin", state="*")
    dp.register_callback_query_handler(delete_task_dp, text_startswith="delete_task", state="*")
    dp.register_callback_query_handler(delete_logic_dp, text_startswith="delete_logic", state="*")
    
    dp.register_callback_query_handler(show_task_dp, text_startswith="show_task", state="*")
    dp.register_callback_query_handler(show_logic_dp, text_startswith="show_logic", state="*")
    dp.register_callback_query_handler(add_logic_dp, text_startswith="add_logic", state="*")
    dp.register_message_handler(add_logic_input_mh, state=AddLogic.input)

    dp.register_callback_query_handler(add_task_dp, text_startswith="add_task", state="*")
    dp.register_message_handler(add_task_input_mh, state=AddTask.input)

    dp.register_callback_query_handler(edit_dp, text_startswith="edit", state="*")
    dp.register_message_handler(edit_input_mh, state=EditLogic.input)

    dp.register_callback_query_handler(edit_body_dp, text_startswith="edbo", state="*")
    dp.register_message_handler(edit_body_mh, state=EditBody.input)
