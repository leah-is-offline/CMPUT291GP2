from pymongo import MongoClient
import os
import json
from datetime import datetime

global posts_collection, votes_collection, tags_collection

'''
TO DO: november 17
    1)take port as cmnd line arg
    2)check if db exists before instantiating new one
    4)Ways to run faster
'''

def main():

    startTime = datetime.now()
    
    client = MongoClient()
    db = client["291db"]

    clearCollectionsIfExists(db)
    createVotesCollection(db)
    createTagsCollection(db)
    createPostCollection(db)
    


    end = datetime.now() - startTime
    print("Entire db build took: {en}".format(en = end))


def clearCollectionsIfExists(db):
    global posts_collection, votes_collection, tags_collection
    startTime = datetime.now()
    
    collections = db.list_collection_names()
    print(collections)
    
    if "posts_collection" in collections:
        posts_collection = db["posts_collection"]
        posts_collection.delete_many({})

    if "tags_collection" in collections:
        tags_collection = db["tags_collection"]
        tags_collection.delete_many({})

    if "votes_collection" in collections:
        votes_collection = db["votes_collection"]
        votes_collection.delete_many({})
    
    end = datetime.now() - startTime
    print("clearing the collections took: {en}".format(en = end))

def createPostCollection(db):
    global posts_collection, votes_collection, tags_collection
    startTime = datetime.now()

    with open('Posts.json') as file: 
        file_data = json.load(file)
    
    for i in file_data['posts']['row']:
        posts_collection.insert_one(i)

    end = datetime.now() - startTime
    print("building posts collection took: {en}".format(en = end))

        
def createTagsCollection(db):
    global posts_collection, votes_collection, tags_collection
    startTime = datetime.now()
    
    with open('Tags.json') as file: 
        file_data = json.load(file)
    
    for i in file_data['tags']['row']:
        tags_collection.insert_one(i)

    end = datetime.now() - startTime
    print("building tags collection took: {en}".format(en = end))
        

def createVotesCollection(db):
    global posts_collection, votes_collection, tags_collection
    startTime = datetime.now()
    
    with open('Votes.json') as file: 
        file_data = json.load(file)
    
    for i in file_data['votes']['row']:
        votes_collection.insert_one(i)

    end = datetime.now() - startTime
    print("building votes collection took: {en}".format(en = end))

if __name__ == "__main__":
    main()

   
    

    




    
