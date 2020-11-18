import pymongo

client = None
db = None
currentUser = None
guestMode = False

def init(port):
    client = pymongo.MongoClient("mongodb://localhost:%d/" % (port))
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

