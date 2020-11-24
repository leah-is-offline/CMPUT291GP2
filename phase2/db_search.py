import re
import db

def getMatchingQuestions(keywords: list):
    # function to retrieve matching posts from keyword search (title, body, tags)
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

    matches = removeDuplicates(matches)
    return matches


def removeDuplicates(matches):
    # function that removes duplicates from a list of dictionaries
    hashable = []
    for dictionary in matches:
        hashable.append(frozenset(dictionary.items())) #makes dictionary immutable
    hashable = set(hashable)

    uniqueResults = []
    for post in hashable:
        uniqueResults.append(dict(post))
   
    return uniqueResults

