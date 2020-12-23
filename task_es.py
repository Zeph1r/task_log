import re

import logging

from elasticsearch import Elasticsearch

es = Elasticsearch()
# Function of search
def search_date(string):
    match = re.search('(\[\d+-\d+-\d+ \d+:\d+:\d+\])', string)
    return match.group()

def search_web(string):
    match = re.search('[P]([\d\w,\(\)]+) (.+)', string)
    return match.group()

def search_ipv6(string):
    match = re.search('[I]([\d\w,\(\)]+) (.+)', string)
    return match.group()

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

def parcing(name_file, name_of_newfile='Log_nev.txt'):
    '''Parcing file
    
    This function parcing a file of all sting and
    find "PingWebSocketCM()" on logs. If there string 
    is found, He push date and echo on database
    '''
    f = open(name_of_newfile, 'a')
    for line in name_file: 
        if 'PingWebSocketCM()' in line:
            Type = 'PingWebSocketCM()'
            date = search_date(line)
            print(date)
            message = search_web(line)
            print(message)
            exp = {
                'date': date,
                'message': message,
                'type': Type
            }
            res = es.index(index="test1", body=exp)
        elif 'IPv6' in line:
            date = search_date(line)
            print(date)
            Type = 'IPv6'
            print(Type)
            message = search_ipv6(line)
            print(message)
            exp = {
                'date': date,
                'message': message,
                'type': Type
                }
            res = es.index(index="test1", body=exp)
        else:
            f.write(line)
    f.close()

# 1. Open file
f = open('Log.txt', 'r+')
# 2. reading log.txt and parcing
connect_elasticsearch()
parcing(f)
# 3. If the word matches, then it is entered into the database. Else string copied on new file
f.close()
