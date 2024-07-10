from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton

#универсальные кнопки
back_button=KeyboardButton('Назад🔙')

#стартовые кнопки
b1=KeyboardButton('Сделать добро❤️')
b2=KeyboardButton('Профиль🔐')
b3=KeyboardButton('Примеры🔥')
b4=KeyboardButton('Топ доброделов💯')
b5=KeyboardButton('О нас🔴')
b6 = KeyboardButton('VIP🚀')
b7=KeyboardButton('Оставить отзыв💎')
start_keyboard=ReplyKeyboardMarkup(resize_keyboard=True)
start_keyboard.row(b1,b2,b3).row(b4,b6,b5).row(b7)

#меню для профиля

get=KeyboardButton('Вывести токены💸')
profile_menu=ReplyKeyboardMarkup(resize_keyboard=True)
profile_menu.row(get,back_button)


load_kind_button_video=KeyboardButton('/Загрузить_видео')
load_kind_button_photo=KeyboardButton('/Загрузить_фото')
load_keyboard=ReplyKeyboardMarkup(resize_keyboard=True)
load_keyboard.row(load_kind_button_video,load_kind_button_photo).row(back_button)

top_btn=ReplyKeyboardMarkup(resize_keyboard=True)
top_btn.row(back_button)
# btn_top_up=InlineKeyboardButton(text='Пополнить счет',callback_data='top_up')
# key_top_up=InlineKeyboardMarkup(row_width=1)
# key_top_up.insert(btn_top_up)
back=KeyboardButton('/Выйти🔙')
btn=ReplyKeyboardMarkup(resize_keyboard=True)
btn.row(back)
def buy_menu(isUrl=True,url='',bill=""):
    qiwiMenu=InlineKeyboardMarkup(row_width=1)
    if isUrl:
        btnUrlQIWI=InlineKeyboardButton(text='Ссылка на оплату', url = url)
        qiwiMenu.insert(btnUrlQIWI)
    btnCheckQIWI=InlineKeyboardButton(text='Проверить оплату',callback_data="check_"+bill)
    qiwiMenu.insert(btnCheckQIWI)
    return qiwiMenu
def kind_menu(user_id):
    btn_kind_yes=InlineKeyboardButton(text='Одобрить',callback_data='user_yes_'+str(user_id))
    btn_kind_no=InlineKeyboardButton(text='Отказать',callback_data='user_no_'+str(user_id))
    key_kind=InlineKeyboardMarkup(row_width=2)
    key_kind.insert(btn_kind_yes)
    key_kind.insert(btn_kind_no)
    return key_kind

sub_inline_markup=InlineKeyboardMarkup(row_width=1)
btnSubMonth=InlineKeyboardButton(text='Месяц - 150 рублей', callback_data='submonth')
sub_inline_markup.insert(btnSubMonth)

support=KeyboardButton("Техподдержка📞")
sup_btn=ReplyKeyboardMarkup(resize_keyboard=True)
sup_btn.row(support,back_button)