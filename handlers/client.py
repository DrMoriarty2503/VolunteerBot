from aiogram import types, Dispatcher
from create_bot import dp,bot,p2p
from keyboards import client_kb, admin_kb
from aiogram.types import ReplyKeyboardRemove
from data_base import sqlite_db
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
import time
import datetime
from pyqiwip2p import QiwiP2P
import random
from aiogram.dispatcher.filters import Text
from aiogram.types.message import ContentType

admin1_ID=1082853437
YOOTOKEN ="381764678:TEST:44467"
chanel_id="-1001514630925"



def days_to_seconds(days):
    return days*24*60*60
def time_sub_day(get_time):
    time_now = int(time.time())
    middle_time=int(get_time)- time_now
    if middle_time <=0:
        return False
    else:
        dt=str(datetime.timedelta(seconds=middle_time))
        dt = dt.replace("days", "дней")
        dt = dt.replace("day", "дня")
        return dt

#обработчик обычных кнопок
# @dp.message_handler(commands=['start','help'])
async def start_commands(message : types.Message):
    try:
        await bot.send_message(message.from_user.id,f'➖➖➖➖➖➖➖➖➖➖\nПривет, {message.from_user.full_name}! Я умный бот Джой. Меня создали, чтобы превратить вашу доброту в маленькую работу. Это значит, что именно ты сможешь сделать этот мир немного лучше!\n➖➖➖➖➖➖➖➖➖➖', reply_markup=client_kb.start_keyboard)
        if sqlite_db.user_exist(message.from_user.id)==False:
            sqlite_db.add_user(message.from_user.id)
        if sqlite_db.user_exist_2(message.from_user.id)==False:
            sqlite_db.add_user_2(message.from_user.id,str(message.from_user.username))
        # print(bool(len(sqlite_db.cur.ececute('SELECT user_id FROM names WHERE user_id = ?',(message.from_user.id,)).fetchall())))
        await message.delete()
    except:
        # await message.reply('Общение с ботом через лс, напишите ему')
        pass
def is_number(_str):
    try:
        int(_str)
        return True
    except ValueError:
        return False
#основное меню для пользователя
async def kind(message: types.Message):
    user_channel_status = await bot.get_chat_member(chat_id=chanel_id, user_id=message.from_user.id)
    if message.text=='Сделать добро❤️' and user_channel_status["status"] != 'left':
        await bot.send_message(message.from_user.id, 'Загрузите видео/фото c результатами Вашего действия и пришлите описание☺️\nМаксимальное число запросов в сутки - 10❗️',reply_markup=client_kb.load_keyboard)
        await message.delete()
    if message.text=='Профиль🔐' and user_channel_status["status"] != 'left':
        tokens=0
        p=0
        places= sqlite_db.cur.execute("SELECT id FROM user_tokens ORDER BY tokens DESC").fetchall()
        for i in range(len(places)):
            if places[i][0] == message.from_user.id:
                p=i+1
        if not sqlite_db.cur.execute('SELECT id FROM user_tokens WHERE id = ?',(message.from_user.id,)).fetchone():
            sqlite_db.cur.execute('INSERT INTO user_tokens VALUES(?,?)', (message.from_user.id, tokens))
            balance_tokens = sqlite_db.cur.execute('SELECT tokens FROM user_tokens WHERE id = ?',(message.from_user.id,)).fetchone()
            balance_rub=balance_tokens[0]//3
            sqlite_db.base.commit()
            await bot.send_message(message.from_user.id,f"Ваш баланс в токенах - {str(balance_tokens)[1:-2]} \nВаш баланс в рублях - {balance_rub}\nМесто в рейтинге -{p}",reply_markup=client_kb.profile_menu)
        else:
            balance_tokens = sqlite_db.cur.execute('SELECT tokens FROM user_tokens WHERE id = ?',(message.from_user.id,)).fetchone()
            balance_rub = balance_tokens[0] // 3
            sqlite_db.base.commit()
            await bot.send_message(message.from_user.id,f"Ваш баланс в токенах - {str(balance_tokens)[1:-2]} \nВаш баланс в рублях - {balance_rub}\nМесто в рейтинге -{p}",reply_markup=client_kb.profile_menu)
        await message.delete()

    if message.text=='О нас🔴' and user_channel_status["status"] != 'left':
        await bot.send_message(message.from_user.id,"Мир меняется, а это значит что меняются и духовные ценности людей .Многие низ них стали более эгоистичными, равнодушными и ожесточёнными. Именно поэтому мы решили хоть как то повлиять данную ситуацию, создав данный проект.\nДобрые дела— это не просто возможность сделать мир немножечко лучше это способ получить материальное вознаграждение за нетрудные действия, приносящие пользую обществу.  Всё просто!Начните диалог с нашим ботом,отправьте ему результаты своего доброго поступка.Мы его просмотрим и  пришлем вам токены, которые можно обменять на настоящие деньги.\nПо поводу выплат.Деньги вы можете вывести сразу после того,  как наберёте 1500 токенов.В конвертации 3 к 1 . Также у вас есть возможность удвоить вознаграждение за свои действия, оформив премиум-подписку. Сделав это, вы получите доступ к премиум-чату, в котором проводятся розыгрыши и публикуется эксклюзивная информация.Если у вас есть предложения или какие-либо пожелания для улучшения качества проекта, то смело пишите нам в поддержку. Сделать это можно через бота Вместе мы можем сделать этот мир чуточку лучше!",reply_markup=client_kb.sup_btn)
        await message.delete()
    if message.text=='Топ доброделов💯' and user_channel_status["status"] != 'left':
        sqlite_db.cur.execute("SELECT id, tokens FROM user_tokens ORDER BY tokens DESC")
        leader_id_1=sqlite_db.cur.execute("SELECT id FROM user_tokens ORDER BY tokens DESC").fetchall()[0][0]
        leader_tokens_1=sqlite_db.cur.execute("SELECT tokens FROM user_tokens ORDER BY tokens DESC").fetchall()[0][0]
        leader_name_1=sqlite_db.cur.execute("SELECT name FROM names WHERE user_id = ?",(int(leader_id_1),)).fetchall()[0][0]
        leader_id_2 = sqlite_db.cur.execute("SELECT id FROM user_tokens ORDER BY tokens DESC").fetchall()[1][0]
        leader_tokens_2 = sqlite_db.cur.execute("SELECT tokens FROM user_tokens ORDER BY tokens DESC").fetchall()[1][0]
        leader_name_2 = sqlite_db.cur.execute("SELECT name FROM names WHERE user_id = ?", (int(leader_id_2),)).fetchall()[0][0]
        leader_id_3 = sqlite_db.cur.execute("SELECT id FROM user_tokens ORDER BY tokens DESC").fetchall()[2][0]
        leader_tokens_3 = sqlite_db.cur.execute("SELECT tokens FROM user_tokens ORDER BY tokens DESC").fetchall()[2][0]
        leader_name_3 = sqlite_db.cur.execute("SELECT name FROM names WHERE user_id = ?", (int(leader_id_3),)).fetchall()[0][0]
        await bot.send_message(message.from_user.id,f"💯Лучшие доброделы на данный момент:💯\n@{leader_name_1} - {leader_tokens_1} токенов\n@{leader_name_2} - {leader_tokens_2} токенов\n@{leader_name_3} - {leader_tokens_3} токенов",reply_markup=client_kb.top_btn)
        await message.delete()
    if message.text=="Примеры🔥" and user_channel_status["status"] != 'left':
        await bot.send_message(message.from_user.id,"Вы можете совершать любые добрые и полезные действия, а вот вам первые идеи:\n1. Убраться во дворе\n2. Помочь пожилым людям\n3. Собрать мусор в парке \n4.  Взять себе домой бездомное животное\n5. Купить букет цветов и раздать девушкам на улице\n6. Сделать комплимент незнакомцу\n7. Помочь соседке спустить коляску\n8. Подвезти автостопщика\n9. Подари то, что тебе уже не нужно тому, кто в этом нуждается\n10. Сделать скворечник\n11. Благоустроить двор\n12. Организовать или участвовать в субботнике\n13. Перевести бабушку через дорогу\n14. Убрать в подъезде",reply_markup=client_kb.top_btn)
        await message.delete()
    if message.text=="Вывести токены💸" and user_channel_status["status"] != 'left':
        tokens = 0
        if not sqlite_db.cur.execute('SELECT id FROM user_tokens WHERE id = ?', (message.from_user.id,)).fetchone():
            sqlite_db.cur.execute('INSERT INTO user_tokens VALUES(?,?)', (message.from_user.id, tokens))
            balance_tokens = sqlite_db.cur.execute('SELECT tokens FROM user_tokens WHERE id = ?',
                                                   (message.from_user.id,)).fetchone()[0]
            sqlite_db.base.commit()
        else:
            balance_tokens = sqlite_db.cur.execute('SELECT tokens FROM user_tokens WHERE id = ?',(message.from_user.id,)).fetchone()[0]
            sqlite_db.base.commit()
        await bot.send_message(message.from_user.id,f"Скоро будет доступно.\nМинимальное количество токенов для вывода - 1500\nВам осталось накопить {1500-balance_tokens} токенов")
        await message.delete()
    if message.text=="Назад🔙" and user_channel_status["status"] != 'left':
        await bot.send_message(message.from_user.id,"Главное меню",reply_markup=client_kb.start_keyboard)
        # await bot.delete_message(chat_id=message.from_user.id, message_id=message.message_id)
        await message.delete()
    if message.text=="VIP🚀" and user_channel_status["status"] != 'left':
        user_sub=0
        time_sub=0
        if(sqlite_db.cur.execute('SELECT time_sub FROM subs WHERE user_id=?',(message.from_user.id,)).fetchone()[0])<=0 or not(sqlite_db.cur.execute('SELECT user_id FROM subs WHERE user_id=?',(message.from_user.id,)).fetchone()[0]):
            await bot.send_message(message.from_user.id,'Подписка открывает участникам нашего проекта ряд преимуществ: участие в конкурсах и розыгрышах призов, получение эксклюзивных фишек. Но самое главное, наличие VIP-статуса позволяет увеличить заработанные Вами токены в 2 раза. ',reply_markup=client_kb.sub_inline_markup)
        else:
            result = sqlite_db.cur.execute("SELECT time_sub FROM subs WHERE user_id=?",(message.from_user.id,)).fetchone()[0]
            time_sub += int(result)
            # user_sub = time_sub_day(sqlite_db.get_time_sub(message.from_user.id))
            user_sub = time_sub_day(time_sub)
            await bot.send_message(message.from_user.id,f"У вас уже есть подписка. Оставшееся время подписки: {user_sub}")

    if message.text=='Техподдержка📞' and user_channel_status["status"] != 'left':
        await bot.send_message(message.from_user.id, "По всем вопросам пишите нам в личку:\n@Olezha_0 - Олег,владелец проекта\n@maxon_rd - Макс,разработчик\n@rikkominase - Миша, контент-менеджер")

    if user_channel_status["status"] == 'left':
        await bot.send_message(message.from_user.id,"Чтобы пользоваться ботом нужно подписаться на наш канал")

def is_number(_str):
    try:
        int(_str)
        return True
    except:
        return False
#обработка согласия на заявку от пользователя
class SendToken(StatesGroup):
    choosing_tokens = State()

# @dp.callback_query_handler(text_contains='user_yes_')
async def welc_kind(callback : types.CallbackQuery,state: FSMContext):
    if callback.from_user.id==admin1_ID:
        user = int(callback.data[9:])
        await SendToken.choosing_tokens.set()
        await bot.send_message(callback.from_user.id,"Введите количество токенов")
        # bot.delete_message(callback.chat.id, mes1.id)
        async with state.proxy() as data:
            data["user1"]=user
        await bot.delete_message(chat_id=callback.from_user.id, message_id=callback.message.message_id)

async def load_token(message: types.Message,state: FSMContext):
    async with state.proxy() as data:
        user=data["user1"]
    if is_number(message.text):
        tokens = message.text;
        if not sqlite_db.cur.execute('SELECT id FROM user_tokens WHERE id = ?',(user,)).fetchone():
            sqlite_db.cur.execute('INSERT INTO user_tokens VALUES(?,?)', (user, tokens))
            sqlite_db.base.commit()
        else:
            balance=sqlite_db.cur.execute('SELECT tokens FROM user_tokens WHERE id = ?', (user,)).fetchone()
            res= int(balance[0]) + int(message.text)
            sqlite_db.cur.execute('UPDATE user_tokens SET tokens = ? WHERE id = ?',(res, user,))
            sqlite_db.base.commit()
        await bot.send_message(user,f"Вам начислено {tokens} токенов")
        await message.delete()
    else:
        await bot.send_message(message.from_user.id, "Введите целое число")
    await state.finish()

#обработка отказа на заявку от пользователя
class RefKind(StatesGroup):
    choosing_proof = State()
# @dp.callback_query_handler(text_contains='user_no_')
async def ref_kind(callback : types.CallbackQuery,state: FSMContext):
    if callback.from_user.id==admin1_ID:
        user = int(callback.data[8:])
        await RefKind.choosing_proof.set()
        await bot.send_message(callback.from_user.id,"Укажите причину отказа")
        async with state.proxy() as data:
            data["user1"]=user
        await bot.delete_message(chat_id=callback.from_user.id, message_id=callback.message.message_id)

async def send_proof_refusing(message: types.Message,state: FSMContext):
    async with state.proxy() as data:
        user=data["user1"]
        proof_refusing = message.text;
        await message.delete()
        await bot.send_message(user,f"К сожалению,Вам отказали в начислении токенов.\nПричина:{proof_refusing}")
    await state.finish()
#############





##########подписка
@dp.callback_query_handler(text="submonth")
async def submonth(call: types.CallbackQuery):
    await bot.delete_message(call.from_user.id, call.message.message_id)
    moneyy = int(150)
    comment = str(moneyy) + '_' + str(random.randint(1000, 9999))  # генерируем коммент
    bill = p2p.bill(amount=moneyy, lifetime=15,comment=comment)  # создаем форму платежа(передаем сумму, время, коммент)
    sqlite_db.create_check(call.from_user.id, moneyy, str(bill.bill_id))
    await bot.send_message(call.from_user.id,f'Перейдите по ссылке для оформления платежа на сумму {moneyy} рублей.',reply_markup=client_kb.buy_menu(url=bill.pay_url, bill=bill.bill_id))
async def check(callback : types.CallbackQuery):
    bill=str(callback.data[6:])
    print(bill)
    info=sqlite_db.get_check(bill)
    print(info)
    print(sqlite_db.cur.execute("SELECT bill_id FROM 'check' WHERE bill_id = ? ",(bill,)).fetchone()[0])
    if info != False:
        if str(p2p.check(bill_id=bill).status)=="PAID":
            sqlite_db.delete_check(bill)
            time_sub = int(time.time()) + days_to_seconds(30)
            if not (sqlite_db.cur.execute('SELECT user_id FROM subs WHERE user_id=?', (callback.from_user.id,)).fetchone()):
                sqlite_db.cur.execute('INSERT INTO subs VALUES (? ,?)', (callback.from_user.id, 0,))
                sqlite_db.base.commit()
            sqlite_db.set_time_sub(callback.from_user.id, time_sub)
            await bot.send_message(callback.from_user.id, "Вам выдана подписка на месяц.\nt.me/+JVbzJ_aDD9xlOWYy - ссылка на закрытый VIP-чат")
        else:
            await bot.send_message(callback.from_user.id, 'Оплата не прошла',reply_markup=nav.buy_menu(False,bill=bill))
            sqlite_db.delete_check(bill)
    else:
        await bot.send_message(callback.from_user.id,'Счет не найден')
        sqlite_db.delete_check(bill)


# загрузка видео с добрым делом
class FSMDeal(StatesGroup):
    video = State()
    des=State()
# @dp.message_handler(commands='load',state=None)
async def load_deal_start_video(message: types.Message):
    await FSMDeal.video.set()
    await message.reply("Загрузи видео",reply_markup=client_kb.btn)
# @dp.message_handler(state="*",commands='exit')
# @dp.message_handler(Text(equals ="exit", ignore_case=True),state="*")
async def cancel_deal(message: types.Message, state: FSMContext):
    current_state=await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await bot.send_message(message.from_user.id,"Отмена загрузки",reply_markup=client_kb.load_keyboard)

# @dp.message_handler(content_types=['video'], state=FSMDeal.video)
async def load_video(message: types.Message,state: FSMContext):
    async with state.proxy() as data:
        data['user_id']=int(message.from_user.id)
        data['video']=str(message.video.file_id)
    await FSMDeal.next()
    await message.reply("Теперь введи описание")
# @dp.message_handler(state=FSMDeal.des)
async def load_des(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['des']=str(message.text)
    await sqlite_db.sql_add_command(state)

    # await bot.send_message(admin1_ID, f"Вам пришла заявка от пользователя {message.from_user.id}",reply_markup=client_kb.kind_menu(message.from_user.id))
    # await message.delete()
    async with state.proxy() as data:
        video_kind=data['video']
        des_kind=data['des']
    if (sqlite_db.cur.execute('SELECT user_id FROM request WHERE user_id=?', (message.from_user.id,)).fetchone())==None:
        now=time.ctime()[-13:-11]
        sqlite_db.cur.execute('INSERT INTO request VALUES(?,?,?)', (message.from_user.id,now,0,))
        sqlite_db.base.commit()
    if int(sqlite_db.cur.execute('SELECT time FROM request WHERE user_id=?', (message.from_user.id,)).fetchone()[0])<=int(time.ctime()[-13:-11]):
        if int(sqlite_db.cur.execute('SELECT count FROM request WHERE user_id=?', (message.from_user.id,)).fetchone()[0])<11:
            if not(sqlite_db.cur.execute('SELECT user_id FROM subs WHERE user_id=?',(message.from_user.id,)).fetchone()):
                await bot.send_video(admin1_ID, video_kind,caption=f"Вам пришла заявка от пользователя @{message.from_user.username}\nОписание:{des_kind}",reply_markup=client_kb.kind_menu(message.from_user.id))
            else:
                await bot.send_video(admin1_ID, video_kind,caption=f"Вам пришла заявка от 🔴VIP🔴 пользователя @{message.from_user.username}\nОписание:{des_kind}",reply_markup=client_kb.kind_menu(message.from_user.id))
            count=int(sqlite_db.cur.execute('SELECT count FROM request WHERE user_id=?', (message.from_user.id,)).fetchone()[0])
            count+=1
            sqlite_db.cur.execute('UPDATE request SET count = ? WHERE user_id = ?',(count,message.from_user.id,))
            sqlite_db.base.commit()
            await bot.send_message(message.from_user.id,"Видео и описание Вашего поступка успешно загружены и доставлены администраторам✅",reply_markup=client_kb.load_keyboard)
        elif int(sqlite_db.cur.execute('SELECT count FROM request WHERE user_id=?', (message.from_user.id,)).fetchone()[0])>=10:
            await bot.send_message(message.from_user.id,"Превышен лимит запросов",reply_markup=client_kb.start_keyboard)
    elif int(time.ctime()[-13:-11])<=int(sqlite_db.cur.execute('SELECT time FROM request WHERE user_id=?', (message.from_user.id,)).fetchone()[0]):
        sqlite_db.cur.execute('UPDATE request SET time = ? WHERE user_id = ?', (int(time.ctime()[-13:-11]), message.from_user.id))
        sqlite_db.base.commit()
        sqlite_db.cur.execute('UPDATE request SET count = ? WHERE user_id = ?', (1, message.from_user.id,))
        sqlite_db.base.commit()
        if not (sqlite_db.cur.execute('SELECT user_id FROM subs WHERE user_id=?', (message.from_user.id,)).fetchone()):
            await bot.send_video(admin1_ID, video_kind,caption=f"Вам пришла заявка от пользователя @{message.from_user.username}\nОписание:{des_kind}",reply_markup=client_kb.kind_menu(message.from_user.id))
        else:
            await bot.send_video(admin1_ID, video_kind,caption=f"Вам пришла заявка от 🔴VIP🔴 пользователя @{message.from_user.username}\nОписание:{des_kind}",reply_markup=client_kb.kind_menu(message.from_user.id))
        await bot.send_message(message.from_user.id,"Видео и описание Вашего поступка успешно загружены и доставлены администраторам✅",reply_markup=client_kb.load_keyboard)

    await state.finish()
# загрузка фото с добрым делом
class FSMDeal_2(StatesGroup):
    photo = State()
    des=State()
# @dp.message_handler(commands='load',state=None)
async def load_deal_start_photo(message: types.Message):
    await FSMDeal_2.photo.set()
    await message.reply("Загрузи фото",reply_markup=client_kb.btn)
# @dp.message_handler(state="*",commands='exit')
# @dp.message_handler(Text(equals ="exit", ignore_case=True),state="*")
async def cancel_deal(message: types.Message, state: FSMContext):
    current_state=await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await bot.send_message(message.from_user.id,"Отмена загрузки",reply_markup=client_kb.load_keyboard)

# @dp.message_handler(content_types=['photo'], state=FSMDeal.video)
async def load_photo(message: types.Message,state: FSMContext):
    async with state.proxy() as data:
        data['user_id']=int(message.from_user.id)
        data['photo']=str(message.photo[0].file_id)
    await FSMDeal_2.next()
    await message.reply("Теперь введи описание")
# @dp.message_handler(state=FSMDeal.des)
async def load_des_2(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['des']=str(message.text)
    await sqlite_db.sql_add_command(state)

    # await bot.send_message(admin1_ID, f"Вам пришла заявка от пользователя {message.from_user.id}",reply_markup=client_kb.kind_menu(message.from_user.id))
    # await message.delete()
    async with state.proxy() as data:
        photo_kind=data['photo']
        des_kind=data['des']
    if (sqlite_db.cur.execute('SELECT user_id FROM request WHERE user_id=?', (message.from_user.id,)).fetchone())==None:
        now=time.ctime()[-13:-11]
        sqlite_db.cur.execute('INSERT INTO request VALUES(?,?,?)', (message.from_user.id,now,0,))
        sqlite_db.base.commit()
    if int(sqlite_db.cur.execute('SELECT time FROM request WHERE user_id=?', (message.from_user.id,)).fetchone()[0])<=int(time.ctime()[-13:-11]):
        if int(sqlite_db.cur.execute('SELECT count FROM request WHERE user_id=?', (message.from_user.id,)).fetchone()[0])<11:
            if not (sqlite_db.cur.execute('SELECT user_id FROM subs WHERE user_id=?', (message.from_user.id,)).fetchone()):
                await bot.send_photo(admin1_ID, photo_kind,caption=f"Вам пришла заявка от пользователя @{message.from_user.username}\nОписание:{des_kind}",reply_markup=client_kb.kind_menu(message.from_user.id))
            else:
                await bot.send_photo(admin1_ID, photo_kind,caption=f"Вам пришла заявка от 🔴VIP🔴 пользователя @{message.from_user.username}\nОписание:{des_kind}",reply_markup=client_kb.kind_menu(message.from_user.id))
            await bot.send_message(message.from_user.id,"Фото и описание Вашего поступка успешно загружены и доставлены администраторам✅",reply_markup=client_kb.load_keyboard)
            count = int(sqlite_db.cur.execute('SELECT count FROM request WHERE user_id=?', (message.from_user.id,)).fetchone()[0])
            count += 1
            sqlite_db.cur.execute('UPDATE request SET count = ? WHERE user_id = ?', (count, message.from_user.id,))
            sqlite_db.base.commit()
        elif int(sqlite_db.cur.execute('SELECT count FROM request WHERE user_id=?', (message.from_user.id,)).fetchone()[0])>=10:
            await bot.send_message(message.from_user.id,"Превышен лимит запросов",reply_markup=client_kb.start_keyboard)
    elif int(time.ctime()[-13:-11])>=int(sqlite_db.cur.execute('SELECT time FROM request WHERE user_id=?', (message.from_user.id,)).fetchone()[0]):
        sqlite_db.cur.execute('UPDATE request SET time = ? WHERE user_id = ?', (int(time.ctime()[-13:-11]), message.from_user.id))
        sqlite_db.base.commit()
        sqlite_db.cur.execute('UPDATE request SET count = ? WHERE user_id = ?', (1, message.from_user.id,))
        sqlite_db.base.commit()
        if not (sqlite_db.cur.execute('SELECT user_id FROM subs WHERE user_id=?', (message.from_user.id,)).fetchone()):
            await bot.send_photo(admin1_ID, photo_kind,caption=f"Вам пришла заявка от пользователя @{message.from_user.username}\nОписание:{des_kind}",reply_markup=client_kb.kind_menu(message.from_user.id))
        else:
            await bot.send_photo(admin1_ID, photo_kind,caption=f"Вам пришла заявка от 🔴VIP🔴 пользователя @{message.from_user.username}\nОписание:{des_kind}",reply_markup=client_kb.kind_menu(message.from_user.id))

    await state.finish()

class Form1(StatesGroup):
    fb = State() # Задаем состояние

# @dp.message_handler(message.text="Оставить отзыв💎")
async def feed(message: types.Message):
    user_channel_status = await bot.get_chat_member(chat_id=chanel_id, user_id=message.from_user.id)
    if user_channel_status["status"] != 'left':
        await bot.send_message(message.from_user.id,
                               "Напишите, что вы думаете об этом проекте. Чтобы хотели улучшить/изменить",reply_markup=client_kb.btn)
    else:
        await bot.send_message(message.from_user.id,'Работа с ботом доступна только подписчикам канала')
        await state.finish()
    await Form1.fb.set()
async def cancel_deal(message: types.Message, state: FSMContext):
    current_state=await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await bot.send_message(message.from_user.id,"Главное меню",reply_markup=client_kb.start_keyboard)
# @dp.message_handler(state=Form.fb)
async def send_feed(message: types.Message, state: FSMContext):
    await bot.send_message('@otzovisDD',message.text)
    await bot.send_message(message.from_user.id,"Благодарим вас за отзыв❤️.\nВсе отзывы Вы можете посмотреть тут @otzovisDD ")
    await state.finish()

def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(start_commands,commands=['start','help'])
    dp.register_message_handler(load_deal_start_video,commands=['Загрузить_видео'],state=None)
    dp.register_message_handler(load_deal_start_photo,commands=['Загрузить_фото'],state=None)
    dp.register_message_handler(feed, Text(equals='Оставить отзыв💎',ignore_case=True),state=None)
    dp.register_message_handler(cancel_deal,commands=['Выйти🔙'],state="*")
    dp.register_message_handler(cancel_deal,Text(equals ="Выйти🔙", ignore_case=True),state="*")
    dp.register_callback_query_handler(check, text_contains='check_')
    dp.register_message_handler(kind)
    dp.register_message_handler(send_feed,state=Form1.fb)
    dp.register_callback_query_handler(submonth,text='submonth')
    dp.register_message_handler(load_token,state=SendToken.choosing_tokens)
    dp.register_callback_query_handler(welc_kind,text_contains='user_yes_',state= None)
    dp.register_callback_query_handler(ref_kind,text_contains='user_no_',state=None)
    dp.register_message_handler(send_proof_refusing,state=RefKind.choosing_proof)
    dp.register_message_handler(load_video,content_types=['video'], state=FSMDeal.video)
    dp.register_message_handler(load_photo,content_types=['photo'], state=FSMDeal_2.photo)
    dp.register_message_handler(load_des,content_types=['text'],state=FSMDeal.des)
    dp.register_message_handler(load_des_2,content_types=['text'],state=FSMDeal_2.des)

