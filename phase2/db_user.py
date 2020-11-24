import db
#ASSUMPTION: that if a score on a user question is owned - this 0 impacts the average

def questionsAnswersOwned(uid):
    # The number of questions/answers a user owns and the average score for those questions/answers owned

    question_scores = []
    answer_scores = []

    postsOwned =  list(db.db_obj.posts.find({"OwnerUserId": str(uid)})) 
    if len(postsOwned) > 0 :
        for post in postsOwned:
            if post["PostTypeId"] == "1":
                question_scores.append(post["Score"])
            elif post["PostTypeId"] == "2":
                answer_scores.append(post["Score"])

    qcount = len(question_scores)
    acount = len(answer_scores)
    qAvg = (sum(question_scores)/ max(qcount, 1))
    aAvg = (sum(answer_scores)/ max(acount, 1))
    return qcount, qAvg, acount, aAvg


def votesRegistered(uid):
    # function to return the number of votes registered to a user

    votes = list(db.db_obj.votes.find({"UserId": str(uid)})) 
    return len(list(votes))

