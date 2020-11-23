from pymongo import MongoClient, collation
from datetime import datetime

client = None
db_obj = None
currentuid = None
guestMode = True


def init(port):
    # function to initialize database
    global db_obj
    client = MongoClient("mongodb://localhost:%d/" % (port))
    db_obj = client["291db"]

def guestLogin():
    # function to allow user to be a guest
    global guestMode
    guestMode = True
    return True


def register(uid):
    # function to register a user
    global guestMode, currentuid
    guestMode = False

    uid = str(uid)  # uid in database is STRINGGGG >:0
    results = db_obj["users"].find({"_id": uid})
    for user in results:
        # username exists in database - unavailable
        print("Username already exists.")
        return False

    # username does not exist in database - available
    db_obj["users"].insert_one({
        "_id": uid,
        "questionCount" : 0,
        "answerCount": 0,
        "voteCount": 0
    })

    currentuid = uid
    print("Username is available. Welcome user {currId}".format(currId=uid))
    return True


def login(uid):
    # function to check if a user logging in exists (IN USER COLLECTION)
    global guestMode, currentuid
    guestMode = False

    uid = str(uid)
    results = db_obj["users"].find({"_id": uid})
    for user in results:
        currentuid = uid
        print("Welcome back user {currId}".format(currId=uid))
        return True
    print("you dont exist...")
    return False

def getNextId(collectionName):
    # function to return the next available ID for a collecion
    global db_obj
    counter = db_obj.counters.find_one_and_update(
        {"_id": collectionName}, {"$inc": {"maxId": 1}}, new=True
    )
    return str(counter["maxId"])


def insertVote(postId, voteType):
    # TODO: UPDATE post.score as well ---> Done

    global guestMode, currentuid

    currentDate = datetime.now()

    document = {
        "Id": getNextId("votes"),
        "PostId": str(postId),
        "CreationData": currentDate.isoformat(),
        "VoteTypeId": voteType
    }

    if(not guestMode):
        document["UserId"] = currentuid

    db_obj.votes.insert_one(document)
    

    #update posts.score as well
    #could use getPost function?
    posts = db_obj["posts"]
    document = posts.find_one_and_update(
                {"Id": str(postId)},
                {"$inc":{"Score": 1}},
                new=True
            )



def insertTags(tags):
    # funct to Insert each tag in tags into the tags collection
    """If a user-provided tag exist in Tags collection, you will add one to the count field of the tag.
    If a user-provided tag does not exist in Tags collection,you will add it to the collection as a new row with a unique id and count 1"""
    # TODO: implementation ---> Done after figuring out what excerptPostID and WikiPostId is

    tags_coll = db_obj["tags"]
    for tag in tags:
        check_tag_exists = tags_coll.count_documents({"TagName": tag})
        if check_tag_exists > 0:
            # increase existing documents tag count by one
            document = tags_coll.find_one_and_update(
                {"TagName": tag}, {"$inc": {"Count": 1}}, new=True
            )
        else:
            # create a new document for that tag
            # TO DO: Find out what excerptPostID and WikiPostId is
            tempDigit = -1
            document = {
                "Id": getNextId("tags"),
                "TagName": str(tag),
                "Count": 1,
                "ExcerptPostId": tempDigit,
                "WikiPostId": tempDigit,
            }
            db_obj.tags.insert_one(document)


def insertPost(title: str, body: str, tags: list, postType: str):
    # function to insert a post into the database
    global guestMode, currentuid

    # only use valid tags
    tags = list(filter(lambda tag: len(tag) > 0, tags))
    insertTags(tags)

    stringTags = ""
    for tag in tags:
        stringTags += "<%s>" % tag

    currentDate = datetime.now()
    currentISODate = currentDate.isoformat()

    document = {
        "Id": getNextId("posts"),
        "PostTypeId": postType,
        "CreationDate": currentISODate,
        "Title": title,
        "Body": body,
        "Tags": stringTags,
        "Score": 0,
        "ViewCount": 0,
        "CommentCount": 0,
        "FavoriteCount": 0,
        "ContentLicense": "CC BY-SA 4.0",
    }

    # if the post is a question, set answer count to zero
    if postType == "1":
        document["AnswerCount"] = 0

    # record the user id if the user is not a guest
    if not guestMode:
        document["OwnerUserId"] = currentuid

    db_obj.posts.insert_one(document)
    return document

def getPost(postId):
    # TODO: update post.viewcount
    result = list(db_obj.posts.find({"Id": postId}))
    if(len(result) > 0):
        return result[0]
    return None

def updateViewCount(postId):
    #function to update the viewCount of a post upon being viewed by user
    #NOTE: only questions have a viewCount
    posts = db_obj["posts"]
    counter = db_obj.posts.find_one_and_update(
        {"Id": postId},
        {"$inc": {"ViewCount": 1}},
        new=True
    )
