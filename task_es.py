from elasticsearch import Elasticsearch
import logging

es = Elasticsearch()

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
            result = line.split(" ")
            date = str(result[0]).replace("[", "") + ' ' + str(result[1]).replace("]", "")
            print(date)
            echo = result[3:]
            echo = ' '.join(echo)
            print(echo)
            exp = {
                'date': date,
                'message': echo
            }
            res = es.index(index="test1", body=exp)
        elif 'IPv6' in line:
            result = line.split(" ")
            date = str(result[0]).replace("[", "") + ' ' + str(result[1]).replace("]", "")
            print(date)
            echo = result[2:]
            echo = ' '.join(echo)
            print(echo)
            exp = {
                'date': date,
                'message': echo
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
