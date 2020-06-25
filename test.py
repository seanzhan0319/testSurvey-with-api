import pymongo

# admin_mongodburi = "mongodb+srv://main:p123456@democluster-ee3kz"\
#     ".mongodb.net/demoDatabase?retryWrites=true&w=majority"
# admin_client = pymongo.MongoClient(admin_mongodburi)
# admin_db = admin_client.demoDatabase

# admin_db.command("createUser", "jack", 
#         pwd="123456", roles=["restricted"])

uri = "mongodb://jack:123456@ds263248.mlab.com:63248/heroku_5qkz777p"
client = pymongo.MongoClient(uri)
db = client["heroku_5qkz777p"]
col = db["jack-col"]
info = col.find({})
for i in info:
    print(i)
