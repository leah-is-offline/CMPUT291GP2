from pymongo import MongoClient, collation

client = None
db = None
currentuid = None
guestMode = False

def init(port):
    global db
    client = MongoClient("mongodb://localhost:%d/" % (port))
    db = client["291db"]

def guestLogin():
    guestMode = True
    return True

def register(uid):
    guestMode = False
    # TODO: add uid to database
    # return True on success
    return False

def login(uid):
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
    return counter["maxId"]

def createPost(title, body, tags):
    print("new post `id: %d" % getNextId("posts"))
    input("")
