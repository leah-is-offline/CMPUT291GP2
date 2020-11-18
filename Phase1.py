from pymongo import MongoClient
import os
import json

'''
TO DO: november 17
    1)take port as cmnd line arg
    2)check if db exists before instantiating new one
    3)check if collections exists before instantiating new ones
    4)Ways to run faster
'''

def main():

    client = MongoClient()
    db = client["291db"]
    createPostCollection(db)
    createTagsCollection(db)
    createVotesCollection(db)

def createPostCollection(db):

    #create or open collection in db
    posts_collection = db["posts_collection"]
    #delete previous entries if they exist 
    posts_collection.delete_many({})

    with open('Posts.json') as file: 
        file_data = json.load(file)
    
    for i in file_data['posts']['row']:
        posts_collection.insert_one(i)

        
def createTagsCollection(db):

    #create or open collection in db
    tags_collection = db["tags_collection"]
    #delete previous entries if they exist 
    tags_collection.delete_many({})

    with open('Tags.json') as file: 
        file_data = json.load(file)
    
    for i in file_data['tags']['row']:
        tags_collection.insert_one(i)
        

def createVotesCollection(db):

    #create or open collection in db
    votes_collection = db["votes_collection"]
    #delete previous entries if they exist 
    votes_collection.delete_many({})

    with open('Votes.json') as file: 
        file_data = json.load(file)
    
    for i in file_data['votes']['row']:
        votes_collection.insert_one(i)

if __name__ == "__main__":
    main()

   
    

    




    
