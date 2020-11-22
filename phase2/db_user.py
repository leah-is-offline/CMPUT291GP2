import db
'''
File to retrieve information about current user upon user login

Post Type ID LEGEND:
   "PostTypeId" : "1" --> question
   "PostTypeId" : "2" --> answer
'''

'''
this file currentley assumes the user exists in every table
'''

#IF A SCORE FOR A POST IS 0 SHOUD WE INCLUDE IT IN THE AVERAGE?

def questionsOwned(uid):
    #the number of questions owned and the average score for those questions

    posts_coll = db.db_obj["posts"]
    question_scores = []
    uid = str(uid)

    results = posts_coll.find({"OwnerUserId": uid}) #TO DO: CHECK IS RESULT NULL
    for post in results:
        if post["PostTypeId"] == "1":
            question_scores.append(post["Score"])

    qcount = len(question_scores)
    return qcount, (sum(question_scores)/ max(qcount, 1))

def answersOwned(uid):
    #the number of answers owned and the average score for those answers
    posts_coll = db.db_obj["posts"]
    answer_scores = []
    uid = str(uid)

    results = posts_coll.find({"OwnerUserId": uid}) #TO DO: CHECK IS RESULT NULL
    for post in results:
        if post["PostTypeId"] == "2":
            answer_scores.append(post["Score"])

    #length of answers score will be number of answers owned (because score is 0, never null)
    acount = len(answer_scores)
    return acount, (sum(answer_scores)/ max(acount, 1))


def votesRegistered(uid):
    #the number of votes registered for the user
    '''The number of votes registered for a user refers to all types of votes
    the user has casted (as shown in Votes.json) and not just votes of a specific type.'''

    votes_coll = db.db_obj["votes"]
    uid = str(uid)

    #TO DO: CHECK IS RESULT NULL
    results = votes_coll.find({"UserId": uid})

    return len(list(results))

