from pymongo import MongoClient, collation
import LoginInfoUtils
from datetime import datetime
import searchUtils


client = None
db = None
currentuid = None
guestMode = True


def init(port):
    #function to initialize database
    global db
    client = MongoClient("mongodb://localhost:%d/" % (port))
    db = client["291db"]
    

def guestLogin():
    #function to allow user to be a guest
    global guestMode
    guestMode = True
    return True


def register(uid):
    #function to register a user 
    global guestMode, currentuid
    guestMode = False
    # TODO: add uid to database ----> Do we need to add until they perform and action? new collection?
    # return True on success -------> Done

    posts_coll = db["posts"]
    uid = str(uid) #uid in database is STRINGGGG >:0
    results = posts_coll.find({"OwnerUserId": uid})
    for user in results:
        if user["OwnerUserId"] == uid:
            #username exists in database - unavailable
            print("Username already exists.")
            return False
    #username does not exist in database - available
    currentuid = uid
    print("Username is available. Welcome user {currId}".format(currId = uid))
    return True


def login(uid):
    #function to check if a user logging in exists (IN POSTS COLLECTION)
    global guestMode, currentuid
    guestMode = False
    # TODO: verify uid exists in database  --->Done
    # return true on success ----------------->Done

    posts_coll = db["posts"]
    uid = str(uid) 
    results = posts_coll.find({"OwnerUserId": uid})
    for user in results:
        if user["OwnerUserId"] == uid:
            currentuid = uid
            print("Welcome back user {currId}".format(currId = uid))
            displayLoginInfo(currentuid)
            return True
    print("you dont exist...")
    return False


def displayLoginInfo(uid):
    #displays user information/records upon login
    LoginInfoUtils.questionsOwned(uid,db)
    LoginInfoUtils.answersOwned(uid,db)
    LoginInfoUtils.votesRegistered(uid, db)
    

def getNextId(collectionName):
    #function to return the next available ID for a collecion
    global db
    counter = db.counters.find_one_and_update(
        {"_id": collectionName},
        {"$inc":{"maxId":1}},
        new=True
    )
    return str(counter["maxId"])


def insertTags(tags):
    #funct to Insert each tag in tags into the tags collection
    '''If a user-provided tag exist in Tags collection, you will add one to the count field of the tag.
    If a user-provided tag does not exist in Tags collection,you will add it to the collection as a new row with a unique id and count 1'''
    # TODO: implementation ---> Done after figuring out what excerptPostID and WikiPostId is
    
    tags_coll = db["tags"]
    for tag in tags:
        check_tag_exists = tags_coll.count_documents({"TagName": tag})
        if check_tag_exists > 0 :
            #increase existing documents tag count by one
            document = tags_coll.find_one_and_update(
                {"TagName": tag},
                {"$inc":{"Count":1}},
                new=True
            )
            print("previous tag updated")
            print(document)
        else:
            #create a new document for that tag
            #TO DO: Find out what excerptPostID and WikiPostId is
            tempDigit = -1
            document = {
                "Id": getNextId("tags"),
                "TagName": str(tag),
                "Count" : 1,
                "ExcerptPostId": tempDigit,
                "WikiPostId": tempDigit
            }
            db.tags.insert_one(document)
            print("new post inserted")
            print(document)


def insertPost(title :str, body :str, tags :list, postType :str):
    #function to insert a post into the database
    """
    How to do this?
    - the post creation date should be set to the current date -----> Done
    """
    
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
        "CreationDate" : currentISODate,
        "Title": title,
        "Body": body,
        "Tags": stringTags,
        "Score": 0,
        "ViewCount": 0,
        "CommentCount": 0,
        "FavoriteCount": 0,
        "ContentLicense": "CC BY-SA 4.0"
    }

    #if the post is a question, set answer count to zero
    if(postType == "1"):
        document["AnswerCount"] = 0

    #record the user id if the user is not a guest
    if(not guestMode):
        document["OwnerUserId"] = currentuid

    db.posts.insert_one(document)
    print("new post inserted")
    print(document)
    input("") 


def search(keywords):
    #function to display search results
    searchUtils.getMatchingQuestions(keywords, db)
    
