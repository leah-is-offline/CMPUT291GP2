from pymongo import MongoClient, collation

client = None
db = None
currentuid = None
guestMode = True

def init(port):
    global db
    client = MongoClient("mongodb://localhost:%d/" % (port))
    db = client["291db"]

def guestLogin():
    global guestMode
    guestMode = True
    return True

def register(uid):
    global guestMode, currentuid
    guestMode = False
    # TODO: add uid to database
    # return True on success
    return False

def login(uid):
    global guestMode, currentuid
    guestMode = False
    # TODO: verify uid exists in database
    # return true on success
    return False

def getNextId(collectionName):
    global db
    counter = db.counters.find_one_and_update(
        {"_id": collectionName},
        {"$inc":{"maxId":1}},
        new=True
    )
    return str(counter["maxId"])

def insertTags(tags):
    """
    Inserts each tag in tags into the tags collection
    """
    # TODO: implementation
    for tag in tags:
        pass

def insertPost(title :str, body :str, tags :list, postType :str):
    """
    How to do this?
    - the post creation date should be set to the current date
    """
    global guestMode, currentuid

    # only use valid tags
    tags = list(filter(lambda tag: len(tag) > 0, tags))

    insertTags(tags)

    stringTags = ""
    for tag in tags:
        stringTags += "<%s>" % tag

    document = {
        "Id": getNextId("posts"),
        "PostTypeId": postType,
        "Title": title,
        "Body": body,
        "Tags": stringTags,
        "Score": 0,
        "ViewCount": 0,
        "CommentCount": 0,
        "FavoriteCount": 0,
        "ContentLicense": "CC BY-SA 4.0"
    }

    if(postType == "1"):
        document["AnswerCount"] = 0

    if(not guestMode):
        document["OwnerUserId"] = currentuid

    db.posts.insert_one(document)
    print("new post inserted")
    print(document)
    input("")
