from pymongo import MongoClient, collation
import os
import json
from datetime import datetime
from util import inputPort

global posts_collection, votes_collection, tags_collection

#TO DO: users collection


class Timer():
    def __init__(self):
        self.startTime = datetime.now()

    def end(self):
        return datetime.now() - self.startTime


def main():

    port = inputPort("Please enter a port number (Default is 27017): ", 27017)
    client = MongoClient("mongodb://localhost:%d/" % (port))
    db = client["291db"]

    timer= Timer()

    initializeCollections(db)
    createTagsCollection(db)
    createPostCollection(db)
    createVotesCollection(db)
    createUsersCollection(db)
    initializeCounters(db)

    print("Entire db build took: {en}".format(en = timer.end()))



def initializeCollections(db):
    global posts_collection, votes_collection, tags_collection
    timer = Timer()

    required_collections = ["posts", "votes", "tags", "counters","users"]

    existing_collections = db.list_collection_names()

    for collection_name in required_collections:
        if collection_name in existing_collections:
            db[collection_name].delete_many({})
        else:
            db.create_collection(collection_name)

    posts_collection = db["posts"]
    tags_collection = db["tags"]
    votes_collection = db["votes"]

    print("clearing the collections took: {en}".format(en = timer.end()))

def createPostCollection(db):
    global posts_collection, votes_collection, tags_collection
    timer = Timer()

    with open('Posts.json') as file:
        file_data = json.load(file)

    posts_collection.create_index("Id", unique = True)
    posts_collection.insert_many(
        file_data['posts']['row'],
        False
    )

    print("building posts collection took: {en}".format(en = timer.end()))


def createTagsCollection(db):
    global posts_collection, votes_collection, tags_collection
    startTime = datetime.now()

    with open('Tags.json') as file:
        file_data = json.load(file)

    tags_collection.create_index("Id", unique = True)
    tags_collection.insert_many(
        file_data['tags']['row'],
        False
    )

    end = datetime.now() - startTime
    print("building tags collection took: {en}".format(en = end))


def createVotesCollection(db):
    global posts_collection, votes_collection, tags_collection
    timer = Timer()

    with open('Votes.json') as file:
        file_data = json.load(file)

    votes_collection.create_index("Id", unique = True)
    votes_collection.insert_many(
        file_data['votes']['row'],
        False
    )

    print("building votes collection took: {en}".format(en = timer.end()))

def initializeCounters(db):
    timer = Timer()

    def getMaxId(collection_name):
        pipeline = [
            {"$sort": {"Id" : -1}},
            {"$limit": 1}
        ]
        col = collation.Collation("en_US", numericOrdering=True)
        cursor = db[collection_name].aggregate(pipeline, collation=col, allowDiskUse=True)
        maxIdStr = list(cursor)[0]["Id"]
        return int(maxIdStr)

    for collection_name in ["posts", "votes", "tags"]:
        db["counters"].insert_one({
            "_id": collection_name,
            "maxId": getMaxId(collection_name)
        })

    print("building counter collection took: {en}".format(en = timer.end()))

def createUsersCollection(db):
    global posts_collection, votes_collection
    timer = Timer()

    def newUser(uid):
        return {
            "_id": uid,
            "questionCount" : 0,
            "answerCount": 0,
            "voteCount": 0
        }

    users = {}
    for post in posts_collection.find({}):
        if "OwnerUserId" in post:
            uid = post["OwnerUserId"]
            postType = ("question" if post["PostTypeId"] == "1" else "answer")
            if uid in users:
                users[uid][postType+"Count"] += 1
            else:
                users[uid] = newUser(uid)
                users[uid][postType+"Count"] = 1;

    for vote in votes_collection.find({}):
        if "UserId" in vote:
            uid = vote["UserId"]
            if not uid in users:
                users[uid] = newUser(uid)
            users[uid]["voteCount"] += 1

    db["users"].insert_many(
        users.values(),
        False
    )

    print("building users collection took: {en}".format(en = timer.end()))


if __name__ == "__main__":
    main()

