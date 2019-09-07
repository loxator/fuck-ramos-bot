import praw
import config
import time
import re
from pymongo import MongoClient

def bot_login():
    print ("Logging in...")
    r = praw.Reddit(username = config.username,
                    password = config.password,
                    client_id = config.client_id,
                    client_secret = config.client_secret,
                    user_agent = "Made by u/loxator")
    print ("Logged in!")

    return r


def run_bot(r, comment_records):
    print ("Searching last 1,000 comments")
    subreddit = r.subreddit('fuckramos+soccercirclejerk')
    for comment in subreddit.stream.comments():
          if re.search('ramos', comment.body, re.IGNORECASE) and not re.search('(fuckramos)|(fuck ramos)|(fukramosbot)',comment.body,re.IGNORECASE) and getComment(comment.id,comment_records) is None and comment.author != r.user.me():
              print ("String with \"ramos\" found in comment " + comment.id)
              comment.reply("""the correct spelling is **Fuck Ramos**
 ------------------------------------------------------------------------------------------------------------------------------------------------------
 Join us at r/fuckramos""")
              print ("Replied to comment " + comment.id)
              pushComments(comment.id,comment_records)

    print ("Search Completed.")

    print(comment_records)

    print ("Sleeping for 10 seconds...")
    #Sleep for 10 seconds...
    time.sleep(10)



def getComment(comment_id, comments_records):
    comments = comments_records.find_one({"comment_id":str(comment_id)})
    return comments

def pushComments(comment_id, comments_records):
    comments_records.insert_one({"comment_id":comment_id})

def setup_mongo_connection():
    MONGO_URI = "mongodb://herokuWorker:test1234@ds249583.mlab.com:49583/comments"
    client = MongoClient(MONGO_URI, connectTimeoutMS=30000)
    db = client.get_database("comments")
    return db.comment_records

comment_records = setup_mongo_connection()
r = bot_login()

while True:
    run_bot(r, comment_records)