import re

import logging

from elasticsearch import Elasticsearch

es = Elasticsearch()
# Function of search
def search_date(string):
    match = re.search('\d{4}\W\d{2}\W\d{2}\s\d{2}\W\d{2}\W\d{2}', string)
    return match.group()

def search_web(string):
    match = re.search('[P]\w{14}[(][)] .{48}', string)
    return match.group()

def search_web2(string):
    match = re.search('[P]\w{14}[(][)] .{50,86}', string)
    return match.group()

def search_ipv6(string):
    match = re.search('[I]\w{2}[6]', string)
    return match.group()

def search_http(string):
    match = re.search('[H]\w{3} \w{12} \w{4} .{69}', string)
    return match.group()

def search_udp(string):
    match = re.search('[U]\w{2} \w{12} .{69}', string)
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
            date = search_date(line)
            print(date)
            try:
                if 86 < len(line) < 100:
                    message = search_web(line)
                    print(message)
                else:
                    message = search_web2(line)
                    print(message)
            except:
                continue
            exp = {
                'date': date,
                'message': message
            }
            res = es.index(index="test1", body=exp)
        elif 'IPv6' in line:
            date = search_date(line)
            print(date)
            Type = 'IPv6'
            print(Type)
            try:
                message = search_http(line)
                print(message)
            except:
                message = search_udp(line)
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
