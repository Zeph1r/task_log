import sqlite3
import os.path

check_db = os.path.exists('mydatabase.db')
if check_db == True:
    print('Существует')
    conn = sqlite3.connect("mydatabase.db")
    cursor = conn.cursor()
else:
    conn = sqlite3.connect("mydatabase.db") # или :memory: чтобы сохранить в RAM
    cursor = conn.cursor()
    cursor.execute("""CREATE TABLE logs
                    (echo text, data text)""")

 
# Сохраняем изменения
conn.commit()


# 1. Открыть файл
f = open('Log.txt', 'r+')
# 2. Читать строчку, превращать её в множество и искать ключевое слово
# 3. Если слово совпадает то внести в бд дату и событие лога, удалить строку
for line in f:
    result = line.split(" ")
    if 'PingWebSocketCM()' in result:
        date = str(result[0] + ' ' + result[1])
        print(date)
        echo = str(result[5:])
        print(echo)
        cursor.execute("INSERT INTO logs VALUES (?, ?)", (echo, date))
        conn.commit()

f.close()

