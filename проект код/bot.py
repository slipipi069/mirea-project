import telebot
from telebot import types
from config import TOKEN
import keyboards.auxiliary_keyboards as auxiliary_kb
import keyboards.public_keyboards as public_kb

from figure_builder import (build_tetrahedron, build_section_tetrahedron,
                            build_parallelepiped, build_section_parallelepiped,
                            figure_to_bytes)
from solid_geometry import point, is_positive_number, is_correct_coordinates, are_points_collinear

bot = telebot.TeleBot(token=TOKEN)

main_text = "Выбери фигуру, для которой нужно построить сечение."


@bot.message_handler(commands=['start'])
def start(message: types.Message) -> None:
    bot.send_message(chat_id=message.chat.id, text=main_text,
                     reply_markup=public_kb.select_figure())


@bot.message_handler(content_types=['text'])
def get_figure_name(message: types.Message) -> None:
    if message.text == "Тетраэдр":
        msg = bot.send_message(chat_id=message.chat.id, text="Укажи коэффициент для построения правильного тетраэдра.",
                               reply_markup=auxiliary_kb.cancel_kb())
        bot.register_next_step_handler(msg, get_coefficient_of_tetrahedron)
    elif message.text == "Параллелепипед":
        msg = bot.send_message(chat_id=message.chat.id, text="Укажи длину для построения параллелепипеда.",
                               reply_markup=auxiliary_kb.cancel_kb())
        bot.register_next_step_handler(msg, get_length_of_parallelepiped)


# tetrahedron
def get_coefficient_of_tetrahedron(message: types.Message) -> None:
    if message.content_type != "text":
        msg = bot.send_message(chat_id=message.chat.id, text="Вы можете указать только текст. "
                                                             "Попробуйте ещё раз.",
                               reply_markup=auxiliary_kb.cancel_kb())
        bot.register_next_step_handler(msg, get_coefficient_of_tetrahedron)
        return
    if message.text == "Отмена":
        bot.send_message(chat_id=message.chat.id, text=main_text,
                         reply_markup=public_kb.select_figure())
        return
    if not is_positive_number(message.text):
        msg = bot.send_message(chat_id=message.chat.id,
                               text="Вы можете указать только целое или дробное число больше 0. "
                                    "Попробуйте ещё раз.")
        bot.register_next_step_handler(msg, get_coefficient_of_tetrahedron)
        return
    coefficient = float(message.text)
    t, ax, fig = build_tetrahedron(coefficient)
    photo = figure_to_bytes(fig)
    msg = bot.send_photo(chat_id=message.chat.id, photo=photo,
                         caption=f"Правильный тетраэдр с коэффициентом {coefficient} готов.\n"
                                 "Укажите через пробел координаты перовой точки для построения сечения тетраэдра.\n"
                                 "Пример координат выглядит так (X Y Z).",
                         reply_markup=auxiliary_kb.cancel_kb())
    bot.register_next_step_handler(msg, get_first_point_tetrahedron_section, coefficient)


def get_first_point_tetrahedron_section(message: types.Message, coefficient: float) -> None:
    if message.content_type != "text":
        msg = bot.send_message(chat_id=message.chat.id, text="Вы можете указать только текст. "
                                                             "Попробуйте ещё раз.",
                               reply_markup=auxiliary_kb.cancel_kb())
        bot.register_next_step_handler(msg, get_first_point_tetrahedron_section, coefficient)
        return
    if message.text == "Отмена":
        bot.send_message(chat_id=message.chat.id, text=main_text,
                         reply_markup=public_kb.select_figure())
        return
    if not is_correct_coordinates(message.text):
        msg = bot.send_message(chat_id=message.chat.id,
                               text="Вы можете указать только 3 целых или дробных числа через пробел. "
                                    "Попробуйте ещё раз.",
                               reply_markup=auxiliary_kb.cancel_kb())
        bot.register_next_step_handler(msg, get_first_point_tetrahedron_section, coefficient)
        return
    point_1 = list(map(float, message.text.split()))
    point_1[0], point_1[1] = point_1[1], point_1[0]
    msg = bot.send_message(chat_id=message.chat.id,
                           text="Укажите через пробел координаты второй точки для построения сечения тетраэдра.\n"
                                "Пример координат выглядит так (X Y Z).")
    bot.register_next_step_handler(msg, get_second_point_tetrahedron_section, coefficient, point_1)


def get_second_point_tetrahedron_section(message: types.Message, coefficient: float, point_1: point) -> None:
    if message.content_type != "text":
        msg = bot.send_message(chat_id=message.chat.id, text="Вы можете указать только текст. "
                                                             "Попробуйте ещё раз.",
                               reply_markup=auxiliary_kb.cancel_kb())
        bot.register_next_step_handler(msg, get_second_point_tetrahedron_section, coefficient, point_1)
        return
    if message.text == "Отмена":
        bot.send_message(chat_id=message.chat.id, text=main_text,
                         reply_markup=public_kb.select_figure())
        return
    if not is_correct_coordinates(message.text):
        msg = bot.send_message(chat_id=message.chat.id,
                               text="Вы можете указать только 3 целых или дробных числа через пробел. "
                                    "Попробуйте ещё раз.",
                               reply_markup=auxiliary_kb.cancel_kb())
        bot.register_next_step_handler(msg, get_second_point_tetrahedron_section, coefficient, point_1)
        return
    point_2 = list(map(float, message.text.split()))
    point_2[0], point_2[1] = point_2[1], point_2[0]
    if point_1 == point_2:
        msg = bot.send_message(chat_id=message.chat.id,
                               text="Координаты этой точки совпадают с координатами предыдущей. "
                                    "Попробуйте ещё раз.",
                               reply_markup=auxiliary_kb.cancel_kb())
        bot.register_next_step_handler(msg, get_second_point_tetrahedron_section, coefficient, point_1)
        return
    msg = bot.send_message(chat_id=message.chat.id,
                           text="Укажите через пробел координаты третей точки для построения сечения тетраэдра.\n"
                                "Пример координат выглядит так (X Y Z).")
    bot.register_next_step_handler(msg, get_third_point_tetrahedron_section, coefficient, point_1, point_2)


def get_third_point_tetrahedron_section(message: types.Message, coefficient: float,
                                        point_1: point, point_2: point) -> None:
    if message.content_type != "text":
        msg = bot.send_message(chat_id=message.chat.id, text="Вы можете указать только текст. "
                                                             "Попробуйте ещё раз.",
                               reply_markup=auxiliary_kb.cancel_kb())
        bot.register_next_step_handler(msg, get_third_point_tetrahedron_section, coefficient, point_1, point_2)
        return
    if message.text == "Отмена":
        bot.send_message(chat_id=message.chat.id, text=main_text,
                         reply_markup=public_kb.select_figure())
        return
    if not is_correct_coordinates(message.text):
        msg = bot.send_message(chat_id=message.chat.id,
                               text="Вы можете указать только 3 целых или дробных числа через пробел. "
                                    "Попробуйте ещё раз.",
                               reply_markup=auxiliary_kb.cancel_kb())
        bot.register_next_step_handler(msg, get_third_point_tetrahedron_section, coefficient, point_1, point_2)
        return
    point_3 = list(map(float, message.text.split()))
    point_3[0], point_3[1] = point_3[1], point_3[0]
    if point_1 == point_3 or point_2 == point_3:
        msg = bot.send_message(chat_id=message.chat.id,
                               text="Координаты этой точки совпадают с координатами предыдущей. "
                                    "Попробуйте ещё раз.",
                               reply_markup=auxiliary_kb.cancel_kb())
        bot.register_next_step_handler(msg, get_third_point_tetrahedron_section, coefficient, point_1, point_2)
        return
    # noinspection PyTypeChecker
    if are_points_collinear(point_1, point_2, point_3):
        msg = bot.send_message(chat_id=message.chat.id,
                               text="Точки\n"
                                    f"A {point_1}\n"
                                    f"B {point_2}\n"
                                    f"C {point_3}\n"
                                    f"лежат на одной прямой. Сечение построить невозможно. "
                                    f"Хотите ввести заново координаты точек?",
                               reply_markup=auxiliary_kb.yes_no_kb())
        bot.register_next_step_handler(msg, collinear_points_tetrahedron_answer, coefficient)
        return
    else:
        # noinspection PyTypeChecker
        fig, msg = build_section_tetrahedron(coefficient, point_1, point_2, point_3)
        photo = figure_to_bytes(fig)
        if msg:
            bot.send_photo(chat_id=message.chat.id, photo=photo, caption=msg)
        else:
            bot.send_photo(chat_id=message.chat.id, photo=photo, caption="Тетраэдр с заданным сечением готов.")
        bot.send_message(chat_id=message.chat.id, text=main_text, reply_markup=public_kb.select_figure())


def collinear_points_tetrahedron_answer(message: types.Message, coefficient: float) -> None:
    if message.content_type != "text":
        msg = bot.send_message(chat_id=message.chat.id, text="Вы можете указать только текст. "
                                                             "Попробуйте ещё раз.",
                               reply_markup=auxiliary_kb.yes_no_kb())
        bot.register_next_step_handler(msg, collinear_points_tetrahedron_answer, coefficient)
        return
    if message.text == "Да ✅":
        msg = bot.send_message(chat_id=message.chat.id,
                               text="Укажите через пробел координаты перовой точки для построения сечения тетраэдра.\n"
                                    "Пример координат выглядит так (X Y Z).",
                               reply_markup=auxiliary_kb.cancel_kb())
        bot.register_next_step_handler(msg, get_first_point_tetrahedron_section, coefficient)
        return
    elif message.text == "Нет ❌":
        bot.send_message(chat_id=message.chat.id, text=main_text,
                         reply_markup=public_kb.select_figure())
        return
    else:
        msg = bot.send_message(chat_id=message.chat.id, text="Укажите Да ✅ / Нет ❌",
                               reply_markup=auxiliary_kb.yes_no_kb())
        bot.register_next_step_handler(msg, collinear_points_tetrahedron_answer, coefficient)


# parallelepiped
def get_length_of_parallelepiped(message: types.Message) -> None:
    if message.content_type != "text":
        msg = bot.send_message(chat_id=message.chat.id, text="Вы можете указать только текст. "
                                                             "Попробуйте ещё раз.",
                               reply_markup=auxiliary_kb.cancel_kb())
        bot.register_next_step_handler(msg, get_length_of_parallelepiped)
        return
    if message.text == "Отмена":
        bot.send_message(chat_id=message.chat.id, text=main_text,
                         reply_markup=public_kb.select_figure())
        return
    if not is_positive_number(message.text):
        msg = bot.send_message(chat_id=message.chat.id,
                               text="Вы можете указать только целое или дробное число больше 0. "
                                    "Попробуйте ещё раз.")
        bot.register_next_step_handler(msg, get_length_of_parallelepiped)
        return
    length = float(message.text)
    msg = bot.send_message(chat_id=message.chat.id, text="Укажите ширину для построения параллелепипеда.",
                           reply_markup=auxiliary_kb.cancel_kb())
    bot.register_next_step_handler(msg, get_width_of_parallelepiped, length)


def get_width_of_parallelepiped(message: types.Message, length: float) -> None:
    if message.content_type != "text":
        msg = bot.send_message(chat_id=message.chat.id, text="Вы можете указать только текст. "
                                                             "Попробуйте ещё раз.",
                               reply_markup=auxiliary_kb.cancel_kb())
        bot.register_next_step_handler(msg, get_width_of_parallelepiped, length)
        return
    if message.text == "Отмена":
        bot.send_message(chat_id=message.chat.id, text=main_text,
                         reply_markup=public_kb.select_figure())
        return
    if not is_positive_number(message.text):
        msg = bot.send_message(chat_id=message.chat.id,
                               text="Вы можете указать только целое или дробное число больше 0. "
                                    "Попробуйте ещё раз.")
        bot.register_next_step_handler(msg, get_width_of_parallelepiped, length)
        return
    width = float(message.text)
    msg = bot.send_message(chat_id=message.chat.id, text="Укажите высоту для построения параллелепипеда.",
                           reply_markup=auxiliary_kb.cancel_kb())
    bot.register_next_step_handler(msg, get_height_of_parallelepiped, length, width)


def get_height_of_parallelepiped(message: types.Message, length: float, width: float) -> None:
    if message.content_type != "text":
        msg = bot.send_message(chat_id=message.chat.id, text="Вы можете указать только текст. "
                                                             "Попробуйте ещё раз.",
                               reply_markup=auxiliary_kb.cancel_kb())
        bot.register_next_step_handler(msg, get_height_of_parallelepiped, length, width)
        return
    if message.text == "Отмена":
        bot.send_message(chat_id=message.chat.id, text=main_text,
                         reply_markup=public_kb.select_figure())
        return
    if not is_positive_number(message.text):
        msg = bot.send_message(chat_id=message.chat.id,
                               text="Вы можете указать только целое или дробное число больше 0. "
                                    "Попробуйте ещё раз.")
        bot.register_next_step_handler(msg, get_height_of_parallelepiped, length, width)
        return
    height = float(message.text)
    t, ax, fig = build_parallelepiped(length, width, height)
    photo = figure_to_bytes(fig)
    msg = bot.send_photo(chat_id=message.chat.id, photo=photo,
                         caption=f"Параллелепипед с "
                                 f"длинной {length}, шириной {width} и высотой {height} готов.\n"
                                 "Укажите через пробел координаты перовой точки для построения сечения "
                                 "параллелепипеда.\n"
                                 "Пример координат выглядит так (X Y Z).",
                         reply_markup=auxiliary_kb.cancel_kb())
    bot.register_next_step_handler(msg, get_first_point_parallelepiped_section, length, width, height)


def get_first_point_parallelepiped_section(message: types.Message, length: float, width: float, height: float) -> None:
    if message.content_type != "text":
        msg = bot.send_message(chat_id=message.chat.id, text="Вы можете указать только текст. "
                                                             "Попробуйте ещё раз.",
                               reply_markup=auxiliary_kb.cancel_kb())
        bot.register_next_step_handler(msg, get_first_point_parallelepiped_section, length, width, height)
        return
    if message.text == "Отмена":
        bot.send_message(chat_id=message.chat.id, text=main_text,
                         reply_markup=public_kb.select_figure())
        return
    if not is_correct_coordinates(message.text):
        msg = bot.send_message(chat_id=message.chat.id,
                               text="Вы можете указать только 3 целых или дробных числа через пробел. "
                                    "Попробуйте ещё раз.",
                               reply_markup=auxiliary_kb.cancel_kb())
        bot.register_next_step_handler(msg, get_first_point_parallelepiped_section, length, width, height)
        return
    point_1 = list(map(float, message.text.split()))
    point_1[0], point_1[1] = point_1[1], point_1[0]
    msg = bot.send_message(chat_id=message.chat.id,
                           text="Укажите через пробел координаты второй точки для построения сечения параллелепипеда.\n"
                                "Пример координат выглядит так (X Y Z).")
    bot.register_next_step_handler(msg, get_second_point_parallelepiped_section, length, width, height, point_1)


def get_second_point_parallelepiped_section(message: types.Message, length: float, width: float, height: float,
                                            point_1: point) -> None:
    if message.content_type != "text":
        msg = bot.send_message(chat_id=message.chat.id, text="Вы можете указать только текст. "
                                                             "Попробуйте ещё раз.",
                               reply_markup=auxiliary_kb.cancel_kb())
        bot.register_next_step_handler(msg, get_second_point_parallelepiped_section, length, width, height,
                                       point_1)
        return
    if message.text == "Отмена":
        bot.send_message(chat_id=message.chat.id, text=main_text,
                         reply_markup=public_kb.select_figure())
        return
    if not is_correct_coordinates(message.text):
        msg = bot.send_message(chat_id=message.chat.id,
                               text="Вы можете указать только 3 целых или дробных числа через пробел. "
                                    "Попробуйте ещё раз.",
                               reply_markup=auxiliary_kb.cancel_kb())
        bot.register_next_step_handler(msg, get_second_point_parallelepiped_section, length, width, height,
                                       point_1)
        return
    point_2 = list(map(float, message.text.split()))
    point_2[0], point_2[1] = point_2[1], point_2[0]
    if point_1 == point_2:
        msg = bot.send_message(chat_id=message.chat.id,
                               text="Координаты этой точки совпадают с координатами предыдущей. "
                                    "Попробуйте ещё раз.",
                               reply_markup=auxiliary_kb.cancel_kb())
        bot.register_next_step_handler(msg, get_second_point_parallelepiped_section, length, width, height,
                                       point_1)
        return
    msg = bot.send_message(chat_id=message.chat.id,
                           text="Укажите через пробел координаты третей точки для построения сечения параллелепипеда.\n"
                                "Пример координат выглядит так (X Y Z).")
    bot.register_next_step_handler(msg, get_third_point_parallelepiped_section, length, width, height,
                                   point_1, point_2)


def get_third_point_parallelepiped_section(message: types.Message, length: float, width: float, height: float,
                                           point_1: point, point_2: point) -> None:
    if message.content_type != "text":
        msg = bot.send_message(chat_id=message.chat.id, text="Вы можете указать только текст. "
                                                             "Попробуйте ещё раз.",
                               reply_markup=auxiliary_kb.cancel_kb())
        bot.register_next_step_handler(msg, get_third_point_parallelepiped_section, length, width, height,
                                       point_1, point_2)
        return
    if message.text == "Отмена":
        bot.send_message(chat_id=message.chat.id, text=main_text,
                         reply_markup=public_kb.select_figure())
        return
    if not is_correct_coordinates(message.text):
        msg = bot.send_message(chat_id=message.chat.id,
                               text="Вы можете указать только 3 целых или дробных числа через пробел. "
                                    "Попробуйте ещё раз.",
                               reply_markup=auxiliary_kb.cancel_kb())
        bot.register_next_step_handler(msg, get_third_point_parallelepiped_section, length, width, height,
                                       point_1, point_2)
        return
    point_3 = list(map(float, message.text.split()))
    point_3[0], point_3[1] = point_3[1], point_3[0]
    if point_1 == point_3 or point_2 == point_3:
        msg = bot.send_message(chat_id=message.chat.id,
                               text="Координаты этой точки совпадают с координатами предыдущей. "
                                    "Попробуйте ещё раз.",
                               reply_markup=auxiliary_kb.cancel_kb())
        bot.register_next_step_handler(msg, get_third_point_parallelepiped_section, length, width, height,
                                       point_1, point_2)
        return
    # noinspection PyTypeChecker
    if are_points_collinear(point_1, point_2, point_3):
        msg = bot.send_message(chat_id=message.chat.id,
                               text="Точки\n"
                                    f"A {point_1}\n"
                                    f"B {point_2}\n"
                                    f"C {point_3}\n"
                                    f"лежат на одной прямой. Сечение построить невозможно. "
                                    f"Хотите ввести заново координаты точек?",
                               reply_markup=auxiliary_kb.yes_no_kb())
        bot.register_next_step_handler(msg, collinear_points_parallelepiped_answer, length, width, height)
        return
    else:
        # noinspection PyTypeChecker
        fig, msg = build_section_parallelepiped(length, width, height, point_1, point_2, point_3)
        photo = figure_to_bytes(fig)
        if msg:
            bot.send_photo(chat_id=message.chat.id, photo=photo, caption=msg)
        else:
            bot.send_photo(chat_id=message.chat.id, photo=photo, caption="Параллелепипед с заданным сечением готов.")
        bot.send_message(chat_id=message.chat.id, text=main_text, reply_markup=public_kb.select_figure())


def collinear_points_parallelepiped_answer(message: types.Message, length: float, width: float, height: float):
    if message.content_type != "text":
        msg = bot.send_message(chat_id=message.chat.id, text="Вы можете указать только текст. "
                                                             "Попробуйте ещё раз.",
                               reply_markup=auxiliary_kb.yes_no_kb())
        bot.register_next_step_handler(msg, collinear_points_parallelepiped_answer, length, width, height)
        return
    if message.text == "Да ✅":
        msg = bot.send_message(chat_id=message.chat.id,
                               text="Укажите через пробел координаты перовой точки для построения сечения "
                                    "параллелепипеда.\n"
                                    "Пример координат выглядит так (X Y Z).",
                               reply_markup=auxiliary_kb.cancel_kb())
        bot.register_next_step_handler(msg, get_first_point_parallelepiped_section, length, width, height)
        return
    elif message.text == "Нет ❌":
        bot.send_message(chat_id=message.chat.id, text=main_text,
                         reply_markup=public_kb.select_figure())
        return
    else:
        msg = bot.send_message(chat_id=message.chat.id, text="Укажите Да ✅ / Нет ❌",
                               reply_markup=auxiliary_kb.yes_no_kb())
        bot.register_next_step_handler(msg, collinear_points_parallelepiped_answer, length, width, height)
