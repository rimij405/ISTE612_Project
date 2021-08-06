import pymongo
import panda as pd

myclient = MongoClient("mongodb://queryBen:tiger123@mongodb.thelionsredmane.stream:27017") #mongo client goes here
mydb = myclient["mydatabase"]
collection = db["mydatabase"]

#results = collection.find({"zip":"city"})
#print(results)

#for result in results:
#        print(result["_id", "city", ""])
        

for x in collection.find().pretty():
  print(x)
