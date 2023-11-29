from aiogram import Router, F, types
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, ReplyKeyboardRemove, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from functions.gpt_free import ask_gpt
from functions.text import split_text_into_sentences

router = Router()

ROLE = ("программист python который специализируется на написании ботов на aiogram 3, "
        "все ответы ты даешь на русском языке")


class GPT_chat(StatesGroup):
    send_message = State()


@router.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer(
        "Привет! Напиши мне что-нибудь, и я передам это GPT.\n"
        "Для начала общения набери команду: /chat"
    )


@router.message(Command("chat"))
async def cmd_chat(message: Message, state: FSMContext):
    await message.answer("Задай вопрос:")
    await state.set_state(GPT_chat.send_message)


@router.message(StateFilter(GPT_chat.send_message))
async def process_message(message: Message, state: FSMContext):
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(
        text="Закончить общение",
        callback_data="state_clear")
    )
    await state.update_data(question=message.text.lower())
    response = await ask_gpt(role=ROLE, content=message.text)
    # Разделите ответ на части, каждая из которых не превышает 400 символов
    response_parts = split_text_into_sentences(response, max_length=1000)
    # Отправьте каждую часть ответа по отдельности
    for part in response_parts:
        await message.answer(part,
                             reply_markup=builder.as_markup()
                             )


@router.callback_query(F.data == "state_clear")
async def clear_state(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer("Чат окончен")
    await state.clear()