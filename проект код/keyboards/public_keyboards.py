from telebot import types


def select_figure() -> types.ReplyKeyboardMarkup:
    kb = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    tetrahedron = types.KeyboardButton(text="Тетраэдр")
    parallelepiped = types.KeyboardButton(text="Параллелепипед")
    kb.row(tetrahedron, parallelepiped)
    return kb
