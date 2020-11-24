from pymongo import MongoClient, collation
from datetime import datetime
import pdb

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

    uid = str(uid)  
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
    # function to return the next available ID for a collection
    global db_obj
    counter = db_obj.counters.find_one_and_update(
        {"_id": collectionName}, {"$inc": {"maxId": 1}}, new=True
    )
    return str(counter["maxId"])


def insertVote(postId, voteType):
    # function to insert a vote (if a user has not already voted on the post)
    global guestMode, currentuid
    votedOn = False
    
    if (not guestMode):
        results = list(db_obj.votes.find({"UserId" : currentuid, "PostId" : str(postId)}))
        if (len(results) > 0):
            print("You have already voted on this post! Vote not recorded.")
            votedOn = True

    if(not votedOn):
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
        increasePostScore(postId)
        print("\nSweet! You voted on this post!")

        
def increasePostScore(postId):
    # function to increase score of a post
    db_obj.posts.find_one_and_update(
                        {"Id": str(postId)},
                        {"$inc":{"Score": 1}},
                        new=True
                    )

def insertTags(tags):
    # funct to Insert each tag in tags into the tags collection

    for tag in tags:
        check_tag_exists = db_obj.tags.count_documents({"TagName": tag})
        if check_tag_exists > 0:
            # increase existing documents tag count by one
            document = db_obj.tags.find_one_and_update(
                {"TagName": tag},
                {"$inc":{"Count": 1}},
                new=True
            )
        else:
            # create a new document for that tag
            tempDigit = -1
            document = {
                "Id": getNextId("tags"),
                "TagName": str(tag),
                "Count": 1,
                "ExcerptPostId": tempDigit,
                "WikiPostId": tempDigit,
            }
            db_obj.tags.insert_one(document)


def insertPost(title: str, body: str, tags: list, postType: str, parentId):
    # function to insert a post into the database
    global guestMode, currentuid

    # only use valid tags
    tags = list(filter(lambda tag: len(tag) > 0, tags))
    insertTags(tags)

    stringTags = ""
    for tag in tags:
        stringTags += "<%s>" % tag

    currentDate = datetime.now()

    document = {
        "Id": getNextId("posts"),
        "PostTypeId": postType,
        "CreationDate": currentDate.isoformat(),
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

    # if the post is an answer, set the parentId to the question it answers
    if postType == "2":
        document["ParentId"] = parentId

    
    # record the user id if the user is not a guest
    if not guestMode:
        document["OwnerUserId"] = currentuid

    db_obj.posts.insert_one(document)
    return document


def getPost(postId):
    # function to return post
    result = list(db_obj.posts.find({"Id": postId}))
    if(len(result) > 0):
        return result[0]
    return None

def viewPost(postId):
    # function to return post and update post viewCount
    global db_obj
    
    post = getPost(postId)
    if (post == None):
        return None

    db_obj.posts.find_one_and_update(
        {"Id": postId},
        {"$inc": {"ViewCount": 1}},
        new=True
        )

    return post


def getAnswers(postId):
    # function to get list of answers, provided a postId of a question
   
    questions = list(db_obj.posts.find({"Id": str(postId)}))
    if len(questions) == 0:
        return None
    
    question = questions[0]
    results = list(db_obj.posts.find({"ParentId" : str(postId)}))
    answers = []

    #pdb.set_trace()
    idx = 0
    if ("AcceptedAnswerId" in question):
        for i,result in enumerate(results):
            if result["Id"] == question["AcceptedAnswerId"]:
                idx = i
                break

        answers.append(results[idx])
        answers[0]["Body"] = ("***" + answers[0]["Body"])
        results.remove(results[idx])

    answers += results
    return answers
