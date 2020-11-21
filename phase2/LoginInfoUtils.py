'''
File to retrieve information about current user upon user login

Post Type ID LEGEND:
   "PostTypeId" : "1" --> question
   "PostTypeId" : "2" --> answer
'''

def questionsOwned(uid, db):
    #the number of questions owned and the average score for those questions

    posts_coll = db["posts"]
    question_scores = []
    uid = str(uid)
    
    results = posts_coll.find({"OwnerUserId": uid})
    for post in results:
        if post["PostTypeId"] == "1":
            question_scores.append(post["Score"])
                    
    print(question_scores)

    #length of question score will be number of questions owned (because score is 0, never null)
    questions_owned = len(question_scores)
    print("User {userid} owns {qcount} questions".format(userid = uid, qcount = questions_owned))
    avg_questions_score = (sum(question_scores)/ len(question_scores))
    print("The average score for those questions is {avgscore}".format(avgscore = avg_questions_score))
    


def answersOwned(uid, db):
    #the number of answers owned and the average score for those answers
    pass



def getAverage(uid, db):
    #function takes in array of intergers and returns sum
    pass


def getVotes(uid, db):
    #the number of votes registered for the user
    pass
