import re
import db
'''
TO DO:
The user should be able to select a question to see all fields of
the question from Posts. After a question is selected,
the view count of the question should increase by one (in Posts) and
the user should be able to perform a question action (as discussed next).
'''


def getMatchingQuestions(keywords: list):
    #function to retrieve matching posts from keyword search
    '''contain at least one keyword either in title, body, or tag fields
    (case-insensitive)'''
    #TO DO : find matches in also "Tags" and "Body" ----> Done
    #I think that i might be searching for spaces ------> Done
    #TO DO: remove duplicates

    #https://docs.mongodb.com/manual/reference/operator/query/regex/

    posts_coll = db.db_obj["posts"]
    keywords = list(filter(lambda word: len(word) > 2, keywords))
    regexKeywords = '|'.join(keywords)
    regex = ".*\\b({})\\b.*".format(regexKeywords)

    matches = []

    for field in ["Title", "Body", "Tags"]:
        print("Searching for matches of {} in {}..."
              .format(regexKeywords, field))

        query = {
            "PostTypeId": "1",
            field: {
                "$regex": regex,
                "$options" :'i'
            }
        }

        matches += list(posts_coll.find(query))

    return matches
