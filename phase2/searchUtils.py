import re
'''
TO DO:
The user should be able to select a question to see all fields of
the question from Posts. After a question is selected,
the view count of the question should increase by one (in Posts) and
the user should be able to perform a question action (as discussed next).
'''

def validateKeywords(keywords, separator):
    #function to validate user provided keywords, user must provide one or more
    while keywords.isspace() or len(keywords) == 0:
        print("Invalid Entry")
        keywords = input("Enter one or more keywords (separated by a space): ")
    validKeywordsList = list(keywords.split(separator))
    return validKeywordsList


def getMatchingQuestions(keywords, db):
    #function to retrieve matching posts from keyword search
    '''contain at least one keyword either in title, body, or tag fields
    (case-insensitive)'''
    #TO DO : find matches in also "Tags" and "Body"
    #I think that i might be searching for spaces

    #https://docs.mongodb.com/manual/reference/operator/query/regex/

    posts_coll = db["posts"]
    for key in keywords:
        print("FINDING MATCHES FOR {key}".format(key=key))
        print(keywords)
    
        query = {
            "Title": {
                "$regex": key+".*",
                "$options" :'i'
                },
            "PostTypeId": "1"
            }
        
        matches = posts_coll.find(query)

        for match in matches:
            title = match["Title"]
            creationDate = match["CreationDate"]
            score = match["Score"]
            answerCount = match["AnswerCount"]
            print("Title: {title} | Creation Date: {cd} | Score : {score} | AnswerCount {ac}\n".format(
                    title = title, cd = creationDate, score = score, ac = answerCount))
    
    
    



