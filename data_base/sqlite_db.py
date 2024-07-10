import sqlite3 as sq
from create_bot import bot
import time
#создание таблиц
def sql_start():
    global base, cur
    ba  se= sq.connect('users_tokens.db')
    cur=base.cursor()
    if base:
        print('Data Base connected OK')
    base.execute('CREATE TABLE IF NOT EXISTS user_tokens (id INT , tokens INT )')
    base.commit()
    base.execute('CREATE TABLE IF NOT EXISTS users (id INT , user_id INT, money INT )')
    base.commit()
    base.execute('CREATE TABLE IF NOT EXISTS deals (user_id INT,video TEXT PRIMARY KEY, des TEXT )')
    base.commit()
    base.execute('CREATE TABLE IF NOT EXISTS subs (user_id INT PRIMARY KEY,time_sub INT )')
    base.commit()
    base.execute('CREATE TABLE IF NOT EXISTS request (user_id INT,time INT, count INT )')
    base.commit()
    base.execute('CREATE TABLE IF NOT EXISTS names (user_id INT,name TEXT)')
    base.commit()
    # base.execute('CREATE TABLE IF NOT EXISTS check (user_id INT, money INT, bill_id REAL )')
    # base.commit()

def user_exist(user_id):
    with base:
        existention=cur.execute("SELECT user_id FROM 'users' WHERE user_id = ?",(user_id,)).fetchall()
        return bool(len(existention))
def user_exist_2(user_id):
    with base:
        existention=cur.execute("SELECT user_id FROM 'names' WHERE user_id = ?",(user_id,)).fetchall()
        return bool(len(existention))
def add_user(user_id):
    with base:
        cur.execute("INSERT INTO 'users' ('user_id') VALUES (?)", (user_id,))
        base.commit()
def add_user_2(user_id,name):
    with base:
        cur.execute("INSERT INTO 'names' ('user_id','name') VALUES (?,?)", (user_id,name,))
        base.commit()
def user_money(user_id):
    with base:
        result = cur.execute("SELECT money FROM 'users' WHERE user_id = ?", (user_id,)).fetchmany(1)
        return result[0][0]

def set_money(user_id,money):
    with base:
        return ("UPDATE 'users' SET 'money' = ? WHERE 'user_id' = ?",(money,user_id,))

def create_check(user_id,money,bill_id):
    with base:
        cur.execute("INSERT INTO 'check' VALUES (?,?,?)", (user_id,money,bill_id,))
        base.commit

def get_check(bill_id):
    with base:
        result=str(cur.execute("SELECT bill_id FROM 'check' WHERE bill_id = ? ",(bill_id,)).fetchone()[0])
        if not bool(len(result)):
            return False
        return result

def delete_check(bill_id):
    with base:
        return cur.execute("DELETE FROM 'check' WHERE 'bill_id' = ?",(bill_id,))

async def sql_add_command(state):
    async with state.proxy() as data:
        cur.execute('INSERT INTO deals VALUES (?,?,?)',tuple(data.values()))
        base.commit()
def set_time_sub(user_id, time_sub):
    with base:
        return cur.execute("UPDATE subs SET time_sub = ? WHERE user_id = ?", (time_sub,user_id,))
def get_time_sub(user_id):
    with base:
        result = cur.execute("SELECT time_sub FROM subs WHERE user_id=?",(user_id,)).fetchall()
        for row in result:
            time_sub=int(row[0])
        return time_sub
def get_sub_status(user_id):
    with base:
        result = cur.execute("SELECT time_sub FROM subs WHERE user_id=?",(user_id,)).fetchall()
        for row in result:
            time_sub=int(row[0])
        if time_sub> int(time.time()):
            return True
        else:
            return False


