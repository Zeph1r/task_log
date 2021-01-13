import re

import logging

from elasticsearch import Elasticsearch

es = Elasticsearch()
# Function of search
def connect_elasticsearch():
    _es = None
    _es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
    if _es.ping():
        print('Yay Connect')
    else:
        print('Awww it could not connect!')
    return _es
if __name__ == '__main__':
  logging.basicConfig(level=logging.ERROR)

def esimport(date='date', Type='type', message='message'):
    exp = {
        'date': date,
        'message': message,
        'type': Type
    }
    res = es.index(index="test1", body=exp)

def parcing(name_file, name_of_newfile='Log_nev.txt'):
    '''Parcing file
    
    This function parcing a file of all sting and
    find "PingWebSocketCM()" on logs. If there string 
    is found, He push date and echo on database
    '''
    f = open(name_of_newfile, 'a')
    for line in name_file:
        try:
            match = re.search('(\[\d+-\d+-\d+ \d+:\d+:\d+\]) \[\d+,\d+\] ([\d\w,\(\)]+) (.+)', line)
            date, Type, message = match.group(1), match.group(2), match.group(3)
            date = date.replace("[", "")
            date = date.replace("]", "")
            print(date)
            print(message)
            esimport(date, Type, message)
            continue
        except:
            pass
        try:
            match = re.search('(\[\d+-\d+-\d+ \d+:\d+:\d+\]) ([\d\w,\(\)]+) (.+)', line)
            date, Type, message = match.group(1), match.group(2), match.group(3)
            date = date.replace("[", "")
            date = date.replace("]", "")
            print(date)
            print(Type)
            print(message)
            esimport(date, Type, message)
            continue
        except:
            f.write(line)
    f.close()

# 1. Open file
f = open('Log.txt', 'r+')
# 2. reading log.txt and parcing
connect_elasticsearch()
parcing(f)
# 3. If the word matches, then it is entered into the database. Else string copied on new file
f.close()
