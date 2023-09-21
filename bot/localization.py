from collections import defaultdict


def get_language(lang_code) -> str:
    """
    Returns language code from {langs} dict or "en" as fallback value

    :param lang_code: language code taken from Message object
    :return: language code from {langs} dict or "en" as fallback value
    """
    langs = defaultdict(lambda: "en", {"ua": "ua"})
    return langs[lang_code.split("-")[0]] if lang_code else "en"


def get_string(lang_code: str, string_id: str) -> str:
    """
    Returns string from {all_strings} dictionary based on user's language code

    :param lang_code: language code taken from Message object
    :param string_id: ID of string to return
    :return: requested string by lang_code and ID
    """
    lang = get_language(lang_code)
    try:
        return all_strings[lang][string_id]
    except KeyError:
        # TODO: log this error
        return "ERR_NO_STRING"


def get_settings_string(lang_code: str, chars_count: int, separators_enabled: bool, prefixes_enabled: bool) -> str:
    """
    Returns text of user's current settings

    :param lang_code: language code taken from Message object
    :param chars_count: number of chars in custom password
    :param separators_enabled: whether separators between chars are enabled
    :param prefixes_enabled: whether password should be enclosed in one extra delimiter
    :return: text of user's current settings
    """
    toggles = ["no", "yes"]  # Choose between "no" and "yes" key depending on False/True values
    lang = get_language(lang_code)
    separators_string = get_string(lang, toggles[separators_enabled])
    prefixes_string = get_string(lang, toggles[prefixes_enabled])
    return get_string(lang, "settings").format(
        num_of_chars=chars_count,
        prefixes=prefixes_string,
        separators=separators_string
    )


en_text_help = """<a href="http://imgs.xkcd.com/comics/password_strength.png">&#8203;</a>\
The idea of this bot gave from <a href="http://xkcd.com/936/">XKCD 936</a> strip. \
This tool will help quickly generate strong and readable passwords or random unreadable passwords \
without having me open KeePass or any other app.

Choose from one of presets or customize passwords with /settings command and then generate them with /generate.
You can also use this bot in <a href="https://core.telegram.org/bots/inline">inline mode</a>.

<b>Available presets</b>:
/generate_low – Random 16 chars password length  with letters, digits, separators
/generate_normal – Random 24 chars password length  with letters, digits, separators
/generate_hard – Random 32 chars password length  with letters, digits, separators
/generate_weak – 2 words, random uppercase, separated by digits
/generate_medium – 3 words, random uppercase, separated by digits
/generate_strong – 4 words, random uppercase, random separators

By the way, check out bot's source code: \
<a href="https://github.com/kraloveckey/passgen-bot">GitHub</a>."""

en_text_start = """<a href="http://imgs.xkcd.com/comics/password_strength.png">&#8203;</a>\
You can use this bot to generate <a href="http://xkcd.com/936/">readable passwords or random unreadable passwords</a>.
Press "[ / ]" to choose from presets of different strength or use /generate command to send " \
custom password (configurable in /settings)

If you would like to see the source code or get help, simply press /help."""

en_text_settings_choose = """Here are your current settings:
<b>Number of chars</b>: {num_of_chars!s}
<b>Extra prefixes/suffixes</b>: {prefixes}
<b>Separators between chars</b>: {separators}

You can edit these settings using buttons below.
After you're satisfied with results, use /generate command"""

ua_text_help = """<a href="http://imgs.xkcd.com/comics/password_strength.png">&#8203;</a>\
Ідея щодо створення цього бота взята з коміксу <a href="http://xkcd.com/936/">XKCD 936</a>. \
Даний інструмент призначений для зручної генерації складних, але читабельних паролів або рандомних нечитабельних паролів \
без необхідності відкривати KeePass або що-небудь ще.

Виберіть один із шаблонів для генерації пароля або налаштуйте його за своїм бажанням командою /settings. \
Потім створіть пароль командою /generate.
Також підтримується робота в <a href="https://core.telegram.org/bots/inline">інлайн-режимі</a>.

<b>Доступні шаблони</b>:
/generate_low – Випадковий пароль довжиною 16 символів з буквами, цифрами, розділювачами
/generate_normal – Випадковий пароль довжиною 24 символів з буквами, цифрами, розділювачами
/generate_hard – Випадковий пароль довжиною 32 символів з буквами, цифрами, розділювачами
/generate_weak – 2 слова, випадкові великі літери, розділені цифрами
/generate_medium – 3 слова, випадкові великі літери, розділені цифрами
/generate_strong – 4 слова, випадкові великі літери, випадкові розділювачі

Вихідні тексти бота доступні за посиланням: \
<a href="https://github.com/kraloveckey/passgen-bot">GitHub</a>."""

ua_text_start = """<a href="http://imgs.xkcd.com/comics/password_strength.png">&#8203;</a>\
Ви можете використовувати цього бота для генерації безпечних <a href="http://xkcd.com/936/">читабельних паролів або рандомних нечитабельних паролів</a>.
Натисніть "[ / ]" для створення пароля за одним із готових шаблонів різного ступеня складності або надішліть \
/generate для створення довільного пароля (складність налаштовується в налаштуваннях: /settings).

Довідка та вихідні коди – /help."""

ua_text_settings_choose = """Ваші налаштування:
<b>Кількість літер</b>: {num_of_chars!s}
<b>Префікси/суфікси</b>: {prefixes}
<b>Розділювачі між літерами</b>: {separators}

Використовуйте кнопки нижче для зміни налаштувань.
Потім викличте команду /generate для генерації пароля з цими налаштуваннями."""

all_strings = {
    "en": {
        "start": en_text_start,
        "help": en_text_help,
        "settings": en_text_settings_choose,
        "pluschar": "+ char",
        "minuschar": "- char",
        "pluspref": "Add prefix & suffix",
        "minuspref": "Remove prefix & suffix",
        "plussep": "Add separators",
        "minussep": "Remove separators",
        "regenerate": "🔄 Regenerate",
        "no": "No",
        "yes": "Yes",
        "inline_weak_title": "Weak password",
        "inline_weak_description": "2 words, random uppercase, separated by digits",
        "inline_medium_title": "Medium password",
        "inline_medium_description": "3 words, random uppercase, separated by digits",
        "inline_strong_title": "Strong password",
        "inline_strong_description": "4 words, random uppercase, random separators",
        "inline_low_title": "Low password",
        "inline_low_description": "Random 16 chars password length  with letters, digits, separators",
        "inline_normal_title": "Normal password",
        "inline_normal_description": "Random 24 chars password length  with letters, digits, separators",
        "inline_hard_title": "Hard password",
        "inline_hard_description": "Random 32 chars password length  with letters, digits, separators"
    },
    "ua": {
        "start": ua_text_start,
        "help": ua_text_help,
        "settings": ua_text_settings_choose,
        "pluschar": "+ літера",
        "minuschar": "- літера",
        "pluspref": "Додати префікс і суфікс",
        "minuspref": "Прибрати префікс і суфікс",
        "plussep": "Додати розділювачі",
        "minussep": "Прибрати розділювачі",
        "regenerate": "🔄 Новий пароль",
        "no": "Ні",
        "yes": "Так",
        "inline_weak_title": "Слабкий пароль",
        "inline_weak_description": "2 слова, випадкові великі літери, розділені цифрам",
        "inline_medium_title": "Звичайний пароль",
        "inline_medium_description": "3 слова, випадкові великі літери, розділені цифрами",
        "inline_strong_title": "Надійний пароль",
        "inline_strong_description": "4 слова, випадкові великі літери, випадкові розділювачі",
        "inline_low_title": "Низький рівень паролю",
        "inline_low_description": "Випадковий пароль довжиною 16 символів з буквами, цифрами, розділювачами",
        "inline_normal_title": "Середній рівень паролю",
        "inline_normal_description": "Випадковий пароль довжиною 24 символи з буквами, цифрами, розділювачами",
        "inline_hard_title": "Високий рівень паролю",
        "inline_hard_description": "Випадковий пароль довжиною 32 символи з буквами, цифрами, розділювачами"
    }
}
