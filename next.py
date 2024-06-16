import sqlite3

import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType

# Ваш токен доступа
token = ''

bh = vk_api.VkApi(token=token)
give = bh.get_api()
longpoll = VkLongPoll(bh)


def blasthack(id, text):
    bh.method('messages.send', {'user_id': id, 'message': text, 'random_id': 0})


def file_open(name):
    f = open('data/' + name, encoding="utf-8")
    f = f.read()
    return f


for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW and event.to_me:

        message = event.text.lower()

        id = event.user_id
        if message == 'старт':
            name = 'information.txt'
            text = file_open(name)
            blasthack(id, 'Здравствуйте!\nВы запустили бота\nВы согдасны со следующими условиями пользования?(да/нет)')
            blasthack(id, text)
            con = sqlite3.connect('registration.db')
            with con:
                data = con.execute("select count(*) from sqlite_master where type='table' and name='start'")
                for row in data:
                    if row[0] == 0:
                        with con:
                            con.execute("""
                                CREATE TABLE start (
                                    id INTEGER PRIMARY KEY,
                                    accept_terms TEXT,
                                    relevance TEXT
                                );
                            """)
            cursor = con.cursor()
            cursor.execute("SELECT * FROM start WHERE id = ?", (id,))
            if not cursor.fetchmany():
                cursor.execute("INSERT INTO start (id, accept_terms, relevance) VALUES (?, ?, ?)", (id, 'no', 'yes'))
                con.commit()
            cursor.close()
            con.close()


        elif message == 'да':
            con = sqlite3.connect("registration.db")
            cursor = con.cursor()

            cursor.execute("SELECT * FROM start WHERE id = ? AND relevance = 'yes' AND accept_terms = 'no'", (id,))
            if cursor.fetchmany():
                cursor.execute(
                    "UPDATE start SET relevance = 'no', accept_terms = 'yes' WHERE id = ? AND relevance = 'yes'", (id,))
                con.commit()
                cursor.close()
                con.close()
                print('jr')
                con.close()
                con1 = sqlite3.connect('registration.db')
                with con1:
                    data = con1.execute("select count(*) from sqlite_master where type='table' and name='nicknames'")
                    for row in data:
                        if row[0] == 0:
                            with con1:
                                con1.execute("""
                                                CREATE TABLE nicknames (
                                                    id INTEGER PRIMARY KEY,
                                                    nicknames TEXT,
                                                    relevance TEXT
                                                );
                                            """)
                cursor1 = con1.cursor()
                cursor1.execute("SELECT * FROM nicknames WHERE id = ?", (id,))
                if not cursor1.fetchmany():
                    cursor1.execute("INSERT INTO nicknames (id, relevance) VALUES (?,  ?)", (id, 'yes'))
                    con1.commit()
                blasthack(id, 'Введите никнейм')
            else:
                blasthack(id, 'Я вас не понимаю')

        elif message == 'нет':
            con = sqlite3.connect("registration.db")
            cursor = con.cursor()

            cursor.execute("SELECT * FROM start WHERE id = ? AND relevance = 'yes' AND accept_terms = 'no'", (id,))
            if cursor.fetchmany():
                cursor.execute("UPDATE start SET relevance = 'no' WHERE id = ? AND relevance = 'yes'", (id,))
                con.commit()
            else:
                blasthack(id, 'Я вас не понимаю')
            cursor.close()
            con.close()


        else:
            con = sqlite3.connect("registration.db")
            cursor = con.cursor()
            cursor.execute("SELECT * FROM nicknames WHERE id = ? AND relevance = 'yes'", (id,))
            con2 = sqlite3.connect("registration.db")
            cursor2 = con2.cursor()
            cursor2.execute("SELECT * FROM users WHERE id = ?", (id,))
            if cursor.fetchmany():
                con1 = sqlite3.connect('registration.db')
                with con1:
                    data = con1.execute("select count(*) from sqlite_master where type='table' and name='users'")
                    for row in data:
                        if row[0] == 0:
                            with con1:
                                con1.execute("""
                                    CREATE TABLE users (
                                        nickname TEXT PRIMARY KEY,
                                        id INTEGER,
                                        password TEXT
                                    );
                                    """)
                cursor1 = con1.cursor()
                cursor1.execute("SELECT * FROM users WHERE nickname = ?", (message,))
                if (not cursor1.fetchmany()) and 4 <= len(message) <= 24:
                    cursor1.execute("INSERT INTO users (id, nickname) VALUES (?,  ?)", (id, message))
                    con1.commit()
                    cursor.execute(
                        "UPDATE nicknames SET relevance = 'no' WHERE id = ? AND relevance = 'yes'", (id,))
                    con.commit()

                    blasthack(id, 'Введите пароль')
                else:
                    blasthack(id, 'Такой никнейм уже зарегистрирован')
                cursor1.close()
            elif cursor2.fetchmany():
                cursor2.execute("UPDATE users SET password = ? WHERE id = ?", (message, id,))
                blasthack(id, 'Вы успешно зарегистрировались')
                con2.commit()
            else:
                blasthack(id, 'Я вас не понимаю')
            cursor.close()
            cursor2.close()
