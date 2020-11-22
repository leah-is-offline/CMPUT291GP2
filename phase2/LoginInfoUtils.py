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

def questionsOwned(uid, db):
    #the number of questions owned and the average score for those questions

    posts_coll = db["posts"]
    question_scores = []
    uid = str(uid)
    
    results = posts_coll.find({"OwnerUserId": uid}) #TO DO: CHECK IS RESULT NULL
    for post in results:
        if post["PostTypeId"] == "1":
            question_scores.append(post["Score"])

    #length of question score will be number of questions owned (because score is 0, never null)
    questions_owned = len(question_scores)
    print("User {userid} owns {qcount} question(s)".format(userid = uid, qcount = questions_owned))
    avg_questions_score = (sum(question_scores)/ len(question_scores))
    print("The average score for those question(s) is {avgscore}".format(avgscore = avg_questions_score))
    


def answersOwned(uid, db):
    #the number of answers owned and the average score for those answers
    
    posts_coll = db["posts"]
    answer_scores = []
    uid = str(uid)
    
    results = posts_coll.find({"OwnerUserId": uid}) #TO DO: CHECK IS RESULT NULL
    for post in results:
        if post["PostTypeId"] == "2":
            answer_scores.append(post["Score"])

    #length of answers score will be number of answers owned (because score is 0, never null)
    answers_owned = len(answer_scores)
    print("User {userid} owns {acount} answer(s)".format(userid = uid, acount = answers_owned))
    avg_answers_score = (sum(answer_scores)/ len(answer_scores))
    print("The average score for those answer(s) is {avgscore}".format(avgscore = avg_answers_score))

    

def votesRegistered(uid, db):
    #the number of votes registered for the user
    '''The number of votes registered for a user refers to all types of votes
    the user has casted (as shown in Votes.json) and not just votes of a specific type.'''

    votes_coll = db["votes"]
    uid = str(uid)

    #TO DO: CHECK IS RESULT NULL
    results = votes_coll.find({"UserId": uid})
    for result in results:
        votes_casted = result["Id"]
        print("User {userid} has {vcasts} votes registered for them".format(userid = uid, vcasts = votes_casted))
        #else:
            #print("User {userid} has 0 votes registered for them".format(userid = uid))

    
