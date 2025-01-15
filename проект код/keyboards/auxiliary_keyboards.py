from telebot import types


def cancel_kb() -> types.ReplyKeyboardMarkup:
    kb = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    cancel = types.KeyboardButton(text="Отмена")
    kb.row(cancel)
    return kb


def clear_kb() -> types.ReplyKeyboardRemove:
    return types.ReplyKeyboardRemove()


def yes_no_kb() -> types.ReplyKeyboardMarkup:
    kb = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    yes = types.KeyboardButton(text="Да ✅")
    no = types.KeyboardButton(text="Нет ❌")
    kb.row(no, yes)
    return kb
