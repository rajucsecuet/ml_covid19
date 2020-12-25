import pymongo
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
db = myclient.covid19
agg_result= db.tweet_en.aggregate(
    [
        {"$group":{"_id" : "$user.location","total" : {"$sum" : 1}}},
        {"$sort":{"total":-1,"_id":1}},
        {"$match":{"_id":{"$ne":""}}},
        {"$limit":10}
    ],allowDiskUse=True)

data_loc=pd.DataFrame(agg_result)
print(data_loc)
data_loc.plot.bar(x='_id', y='total', rot=0)
plt.xlabel("Location")
plt.ylabel("NO. Tweets")
plt.title("Top 10 Locations Posting about Covid-19")
plt.show()

agg_result_country= db.tweet_en.aggregate(
    [
        {"$group":{"_id" : "$place.country","total" : {"$sum" : 1}}},
        {"$sort":{"total":-1,"_id":1}},
        {"$match":{"_id":{"$ne":None}}},
        {"$limit":10}
    ],allowDiskUse=True)
data_country=pd.DataFrame(agg_result_country)
print(data_country)
data_country.plot.bar(x='_id', y='total', rot=0)
plt.xlabel("Country")
plt.ylabel("NO. Tweets")
plt.title("Top 10 Countries Posting about Covid-19")
plt.show()