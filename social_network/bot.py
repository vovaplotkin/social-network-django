import random
import json
import requests
from pprint import pprint


# read json config
with open('bot_config.json') as f:
    config = json.load(f)

# signup and login (number_of_users)
register_url = r"http://127.0.0.1:8000/api/register/"
login_url = r"http://127.0.0.1:8000/api/login/"
users = {}
for i in range(config['number_of_users']):
    user = f'user{i + 1}'
    data = {
        "username": user,
        "password": "admin"
    }
    requests.post(register_url, data=data | {"email": f"{user}@example.com"})
    token = requests.post(login_url, data=data)
    users[user] = token.json()

pprint(users)

# create random number of posts (max_posts_per_user)
posts_url = 'http://127.0.0.1:8000/posts/'
posts_num = 0
for i, user in enumerate(users):
    for j in range(random.randint(1, config['max_posts_per_user'])):
        data = {
            "user": i + 1,
            "text": f"Post {j + 1} by user {user}"
        }
        header = {'Authorization': f"Bearer {users[user]['access']}"}
        r = requests.post(posts_url, data=data, headers=header)
        posts_num += 1

# like random posts (max_likes_per_user)
likes_url = 'http://127.0.0.1:8000/likes/'
for i, user in enumerate(users):
    for j in range(random.randint(1, config['max_likes_per_user'])):
        user = random.randint(1, config['number_of_users'])
        post = random.randint(1, posts_num)
        data = {
            "user": user,
            "post": post,
            "value": "like"
        }
        r = requests.post(likes_url, data=data)
