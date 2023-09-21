from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.utils.markdown import hcode

from bot.config_reader import settings
from bot.keyboards import make_settings_keyboard, make_regenerate_keyboard
from bot.localization import get_string, get_settings_string
from bot.pwdgen import XKCD


async def cmd_start(message: types.Message, state: FSMContext):
    data = await state.get_data()

    # Check whether user's settings exist and initialize if missing
    if data.get("chars_count") is None:
        await state.update_data(chars_count=settings.chars.default)
    if data.get("prefixes_suffixes") is None:
        await state.update_data(prefixes_suffixes=settings.chars.prefixes_suffixes_by_default)
    if data.get("separators") is None:
        await state.update_data(separators=settings.chars.prefixes_suffixes_by_default)

    await message.answer(get_string(message.from_user.language_code, "start"))


async def cmd_help(message: types.Message):
    await message.answer(get_string(message.from_user.language_code, "help"))


async def cmd_generate_low(message: types.Message):
    pwd: XKCD = message.bot.get("pwd")
    await message.answer(hcode(pwd.low()))


async def cmd_generate_normal(message: types.Message):
    pwd: XKCD = message.bot.get("pwd")
    await message.answer(hcode(pwd.normal()))


async def cmd_generate_hard(message: types.Message):
    pwd: XKCD = message.bot.get("pwd")
    await message.answer(hcode(pwd.hard()))


async def cmd_generate_weak(message: types.Message):
    pwd: XKCD = message.bot.get("pwd")
    await message.answer(hcode(pwd.weak()))


async def cmd_generate_medium(message: types.Message):
    pwd: XKCD = message.bot.get("pwd")
    await message.answer(hcode(pwd.medium()))


async def cmd_generate_strong(message: types.Message):
    pwd: XKCD = message.bot.get("pwd")
    await message.answer(hcode(pwd.strong()))


async def cmd_generate_custom(message: types.Message, state: FSMContext):
    pwd: XKCD = message.bot.get("pwd")
    data = await state.get_data()
    custom_pwd = pwd.custom(
        data.get("chars_count", settings.chars.default),
        data.get("separators", settings.chars.separators_by_default),
        data.get("prefixes_suffixes", settings.chars.prefixes_suffixes_by_default)
    )
    await message.answer(
        hcode(custom_pwd),
        reply_markup=make_regenerate_keyboard(message.from_user.language_code)
    )


async def default(message: types.Message):
    # same as cmd_generate_normal()
    pwd: XKCD = message.bot.get("pwd")
    await message.answer(hcode(pwd.normal()))


async def cmd_settings(message: types.Message, state: FSMContext):
    data = await state.get_data()
    lang_code = message.from_user.language_code
    chars_count = data.get("chars_count", settings.chars.default)
    separators = data.get("separators", settings.chars.separators_by_default)
    prefixes = data.get("prefixes_suffixes", settings.chars.prefixes_suffixes_by_default)
    kb = make_settings_keyboard(
        config=settings,
        language=lang_code,
        current_charcount=chars_count,
        separators_enabled=separators,
        prefixes_enabled=prefixes
    )
    message_text = get_settings_string(
        lang_code=lang_code,
        chars_count=chars_count,
        separators_enabled=separators,
        prefixes_enabled=prefixes
    )
    await message.answer(message_text, reply_markup=kb)


def register_commands(dp: Dispatcher):
    dp.register_message_handler(cmd_start, commands="start")
    dp.register_message_handler(cmd_help, commands="help")
    dp.register_message_handler(cmd_settings, commands="settings")
    dp.register_message_handler(cmd_generate_low, commands="generate_low")
    dp.register_message_handler(cmd_generate_normal, commands="generate_normal")
    dp.register_message_handler(cmd_generate_hard, commands="generate_hard")
    dp.register_message_handler(cmd_generate_weak, commands="generate_weak")
    dp.register_message_handler(cmd_generate_medium, commands="generate_medium")
    dp.register_message_handler(cmd_generate_strong, commands="generate_strong")
    dp.register_message_handler(cmd_generate_custom, commands="generate")
    dp.register_message_handler(default, content_types=types.ContentTypes.ANY)
