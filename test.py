import logging
import xlsxwriter
from elasticsearch import Elasticsearch

es = Elasticsearch()
# Function of search
def connect_elasticsearch():
    '''This function test connect to Elasticsearch DateBase'''
    _es = None
    _es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
    if _es.ping():
        print('Yay Connect')
    else:
        print('Awww it could not connect!')
    return _es
if __name__ == '__main__':
  logging.basicConfig(level=logging.ERROR)

def write_xls(name="new.xlsx", index1=0, index2=0, msg=''):
    workbook = xlsxwriter.Workbook(name)
    worksheet = workbook.add_worksheet()
    worksheet.write(index1, index2, msg)
    workbook.close()


def search(index):
    '''This function search all date of column"date" from index"index"

    "index" and "date" is arguments of this function
    '''
    search_req = {
      "query": {
        "range": {
          "date": {
            "time_zone": "+01:00",
            "gte": "2020-01-01T00:00:00",
            "lte": "now"
          }
        }
      }
    }
    search1 = es.search(index=index, body=search_req, size=10000)
    index1 = 1
    worksheet.write(0, 0, "Date")
    worksheet.write(0, 1, "Message")
    for doc in search1['hits']['hits']:
        try:
            index2 = 0
            date = doc['_source']['date']
            str(date).replace(" ", "")
            worksheet.write(index1, index2, date)
            print(date)
            index2 = 1
            print(index2)
            message = doc['_source']['message']
            str(message).replace(" ","")
            worksheet.write(index1, index2, message)
            print(message)
            index1 += 1
            print(index1)
        except:
            pass

connect_elasticsearch()
workbook = xlsxwriter.Workbook("new.xlsx")
worksheet = workbook.add_worksheet()
search("test1")
workbook.close()
