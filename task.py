import sqlite3
import os.path

def parcing(name_file, name_of_newfile='Log_nev.txt'):
    '''Parcing file
    
    This function parcing a file of all sting and
    find "PingWebSocketCM()" on logs. If there string 
    is found, He push date and echo on database
    '''
    f = open(name_of_newfile, 'a')
    for line in name_file: 
        if 'PingWebSocketCM()' in line:
            result = line.split(" ")
            date = str(result[0] + ' ' + result[1])
            print(date)
            echo = str(result[5:])
            print(echo)
            cursor.execute("INSERT INTO logs VALUES (?, ?)", (echo, date))
        else:
            f.write(line)
    f.close()




# Check ald file of database
check_db = os.path.exists('mydatabase.db')
if check_db:
    print('Существует')
    conn = sqlite3.connect("mydatabase.db")
    cursor = conn.cursor()
else:
    conn = sqlite3.connect("mydatabase.db")
    cursor = conn.cursor()
    cursor.execute("""CREATE TABLE logs
                    (echo text, data text)""")

 
# Saved changes
conn.commit()


# 1. Open file
f = open('Log.txt', 'r+')
# 2. reading log.txt and parcing 
parcing(f)
# 3. If the word matches, then it is entered into the database. Else string copied on new file 

        
conn.commit()
f.close()

