

import pymongo

c = pymongo.MongoClient()

for i in c.my_db.school.find():
    print(i)