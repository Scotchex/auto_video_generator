import os

import praw
from dotenv import load_dotenv

load_dotenv()

reddit = praw.Reddit(
    client_id=os.environ["REDDIT_CLIENT_ID"],
    client_secret=os.environ["REDDIT_CLIENT_SECRET"],
    user_agent=os.getenv("REDDIT_USER_AGENT", "money by u/scotchex")
)

""" subreddit = reddit.subreddit('memes')

top_posts = subreddit.top(limit = 10)
new_posts = subreddit.new(limit = 10) """

""" for post in top_posts:
    print(post.title) #title
    print(post.id) #uniquie id
    print(post.url) #returns the url
    print(post.selftext) #get main text
    print(post.score) #number of votes
    print(post.num_comments) #number of comments
    print(post.created_utc) #utc time of time created
    print('\n') """

def find_top(subreddit, filter = 'day', top_picks = 10):
    subreddit = reddit.subreddit(subreddit)
    titles_lst = []
    text_lst = []
    dict = {}
    top_posts = subreddit.top(time_filter = filter, limit = top_picks)
    for post in top_posts:
        titles_lst.append(post.title)
        text_lst.append(post.selftext)
    for i in range(len(titles_lst)):
        dict[titles_lst[i]] = text_lst[i]
    return dict

def prepare(dict):
    result = []
    for index, (title, text) in enumerate(dict.items()):
        result.append(f"index:{index}, title:{title}, text:{text}")
    return "\n".join(result)
