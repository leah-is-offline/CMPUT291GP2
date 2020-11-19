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
    createPostCollection(db)
    createVotesCollection(db)
    createTagsCollection(db)


    end = datetime.now() - startTime
    print("Entire db build took: {en}".format(en = end))


def clearCollectionsIfExists(db):
    global posts_collection, votes_collection, tags_collection
    startTime = datetime.now()

    required_collections = ["posts", "votes", "tags"]

    existing_collections = db.list_collection_names()

    for collection_name in required_collections:
        if collection_name in existing_collections:
            db[collection_name].delete_many({})
        else:
            db.create_collection(collection_name)

    posts_collection = db["posts"]
    tags_collection = db["tags"]
    votes_collection = db["votes"]

    end = datetime.now() - startTime
    print("clearing the collections took: {en}".format(en = end))

def createPostCollection(db):
    global posts_collection, votes_collection, tags_collection
    startTime = datetime.now()

    with open('Posts.json') as file:
        file_data = json.load(file)

    posts_collection.insert_many(
        file_data['posts']['row'],
        False
    )

    end = datetime.now() - startTime
    print("building posts collection took: {en}".format(en = end))


def createTagsCollection(db):
    global posts_collection, votes_collection, tags_collection
    startTime = datetime.now()

    with open('Tags.json') as file:
        file_data = json.load(file)

    tags_collection.insert_many(
        file_data['tags']['row'],
        False
    )

    end = datetime.now() - startTime
    print("building tags collection took: {en}".format(en = end))


def createVotesCollection(db):
    global posts_collection, votes_collection, tags_collection
    startTime = datetime.now()

    with open('Votes.json') as file:
        file_data = json.load(file)

    tags_collection.insert_many(
        file_data['votes']['row'],
        False
    )


    end = datetime.now() - startTime
    print("building votes collection took: {en}".format(en = end))

if __name__ == "__main__":
    main()

