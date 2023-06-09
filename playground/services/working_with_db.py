import pymongo
from django.conf import settings

connect_string = 'mongodb+srv://strelchenko2010amg:k01GE0H8@diploma.cmzzvqx.mongodb.net/' 

my_client = pymongo.MongoClient(connect_string)

# First define the database name
dbname = my_client['diploma']

# Now get/create collection name (remember that you will see the database in your mongodb cluster only after you create a collection
collection_name = dbname["news"]

def insertDocument(resultBart, resultZeroShot, resultRandomForest, url, text):
    newsDocument = {
        "url": url,
        "text": text,
        "bartLabelsOrder": resultBart['labels'],
        "bartScores": resultBart["scores"],
        "zeroShotLabelsOrder": resultZeroShot['labels'],
        "zeroShotScores": resultZeroShot["scores"],
        "randomForestLabel": resultRandomForest,
        "mark": 0
    }
    collection_name.insert_one(newsDocument)
    return


def findByUrl(url):
    try:
        return collection_name.find_one({"url": url})
    except:
        return None

def makeMark(url, mark):
    collection_name.update_one(
        {'url': url },
        { "$set": { "mark": mark } }
    )
    return

def findAll():
    marks = []
    for mark in collection_name.find({}, {"_id": 0, "mark": 1}):
        marks.append(mark['mark'])
    return marks