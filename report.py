import logging
import pandas as pd
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
    for doc in search1['hits']['hits']:
        try:
            date = doc['_source']['date']
            print(date)
            message = doc['_source']['message']
            print(message)
        except:
            pass

connect_elasticsearch()
search("test1")

# Assign spreadsheet filename to `file`
file = 'example.xlsx'

# Load spreadsheet
xl = pd.ExcelFile(file)

# Print the sheet names
print(xl.sheet_names)

# Load a sheet into a DataFrame by name: df1
df1 = xl.parse('Sheet1')