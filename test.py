import pymongo
import requests

# admin_mongodburi = "mongodb+srv://main:p123456@democluster-ee3kz"\
#     ".mongodb.net/demoDatabase?retryWrites=true&w=majority"
# admin_client = pymongo.MongoClient(admin_mongodburi)
# admin_db = admin_client.demoDatabase

# admin_db.command("createUser", "jack", 
#         pwd="123456", roles=["restricted"])

# uri = "mongodb://jack:123456@ds263248.mlab.com:63248/heroku_5qkz777p"
# client = pymongo.MongoClient(uri)
# db = client["heroku_5qkz777p"]
# col = db["jack-col"]
# info = col.find({})
# for i in info:
#     print(i)

Feedback_URL = 'https://test-api-615.herokuapp.com/api/feedback/'
collection_name = 'test2/hello'
API_URL = Feedback_URL + collection_name
Headers = {'Content-Type': 'application/json'}
dataToPOST = {'sliderVal': '73'}
response = requests.put(API_URL, json=dataToPOST, headers=Headers)
print(response)

