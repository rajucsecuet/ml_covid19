from pathlib import Path
import pymongo
import os
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["covid19"]
mycol_post = mydb["post"]
mycol_tweet = mydb["tweet_en_test"]
print(mydb.list_collection_names())

os.chdir('F:\\processing\\')
data_dirs = ['files']
count=0
for data_dir in data_dirs:
    for path in Path(data_dir).iterdir():
        count=count+1
        print(count)
        file_path="F:\\processing\\files\\"+path.name
        cmd="mongoimport --file "+file_path+" --db covid19 --collection post"
        print(cmd)
        os.system(cmd)
        os.system("del /f "+file_path)
        if(count%12==0):
            print(mycol_post.count_documents({"lang":"en"}))
            agg_result = mycol_post.aggregate([{"$match": {"lang": "en"}}, {"$project": {"id": 1, "created_at": 1, "full_text": 1, "geo": 1, "user.id": 1,"user.location": 1, "place.country": 1,"retweeted_status.id": 1,"retweeted_status.created_at": 1,"retweeted_status.full_text": 1}}, {"$merge": "tweet_en_test"}])
            print(mycol_tweet.count_documents({}))
            mycol_post.drop();
            print(mycol_post.count_documents({}))

print(mycol_post.count_documents({"lang":"en"}))
agg_result = mycol_post.aggregate([{"$match": {"lang": "en"}}, {"$project": {"id": 1, "created_at": 1, "full_text": 1, "geo": 1, "user.id": 1,"user.location": 1, "place.country": 1,"retweeted_status.id": 1,"retweeted_status.created_at": 1,"retweeted_status.full_text": 1}}, {"$merge": "tweet_en_test"}])
print(mycol_tweet.count_documents({}))
mycol_post.drop();
print(mycol_post.count_documents({}))
