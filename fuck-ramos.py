import praw
import time
import re
from pymongo import MongoClient
import os
from dotenv import load_dotenv
import sys
load_dotenv()

def bot_login():
    print ("Logging in...")
    r = praw.Reddit(username = os.environ.get('username'),
                    password = os.environ.get('password'),
                    client_id = os.environ.get('client_id'),
                    client_secret = os.environ.get('client_secret'),
                    user_agent = "Made by u/loxator")
    print ("Logged in!")

    return r


def run_bot(r, comment_records):
    print ("Searching last 1,000 comments")
    subreddit = r.subreddit('fuckramos+soccercirclejerk')
    x=0
    for comment in subreddit.stream.comments():
          x=x+1
          if(x==100):
              break
          if re.search('ramos', comment.body, re.IGNORECASE) and not re.search('(fuckramos)|(fuck ramos)|(fukramosbot)',comment.body,re.IGNORECASE) and getComment(comment.id,comment_records) is None and comment.author != r.user.me():
              print ("String with \"ramos\" found in comment " + comment.id)
              comment.reply("""the correct spelling is **Fuck Ramos**
 ------------------------------------------------------------------------------------------------------------------------------------------------------
 Join us at r/fuckramos""")
              print ("Replied to comment " + comment.id)
              pushComments(comment.id,comment_records)

    print ("Search Completed.")

    print(comment_records)

    #print ("Sleeping for 10 seconds...")
    #Sleep for 10 seconds...
    #time.sleep(10)
    



def getComment(comment_id, comments_records):
    comments = comments_records.find_one({"comment_id":str(comment_id)})
    return comments

def pushComments(comment_id, comments_records):
    comments_records.insert_one({"comment_id":comment_id})

def setup_mongo_connection():
    MONGO_URI = os.environ.get('mongo_uri')
    client = MongoClient(MONGO_URI, connectTimeoutMS=30000)
    db = client.get_database("comments")
    return db.comment_records

comment_records = setup_mongo_connection()
r = bot_login()


run_bot(r, comment_records)
