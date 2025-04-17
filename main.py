import requests
import json

BASE_URL = "https://dummyjson.com"

class Plugin:
    def __init__(self):
        self.token = None
        self.headers = {}
    
    # generic api call function for GET and POST requests (I can add more methods if needed)
    def call_api(self, endpoint, method='GET', data=None):
        url = f"{BASE_URL}{endpoint}"
        try:
            if method == 'GET':
                response = requests.get(url, headers=self.headers)
            elif method == 'POST':
                response = requests.post(url, json=data, headers=self.headers)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")

            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"API call to {endpoint} failed: {e}")
            return None
#connectivity test
    def login(self,username, password):
        print("login")
        data = {"username": username, "password": password}
        response = self.call_api("/auth/login", method="POST", data=data)

        if response and "accessToken" in response:
            self.token = response["accessToken"]
            self.headers = {"Authorization": f"Bearer {self.token}"}
            print("Login successful")
            return True
        print("Login failed")
        return False
    
#  E1: User info
    def collect_user_info(self):
        print("Collecting user info")
        if not self.token:
            print("Not logged in")
            return None
        response = self.call_api("/auth/me")
        if response and "user" in response:
            user_info = response["user"]
            print(f"User info: ", user_info)
            return user_info
        return None
#E2: Posts
    def collect_posts(self, limit=60):
        print(f"Collecting {limit} posts")
        response = self.call_api(f"/posts?limit={limit}")
        return response['posts'] if response and 'posts' in response else []
#E3: Posts with comments
    def collect_comments_for_posts(self, posts):
        print("Collecting comments for each post")
        posts_with_comments = []
        for post in posts:
            post_id = post.get('id')
            if post_id is None:
                continue
            response = self.call_api(f"/posts/{post_id}/comments")
            comments = response.get('comments', []) if response else []
            post['comments'] = comments
            posts_with_comments.append(post)
        return posts_with_comments
    def evidence_collection(self):
        print("Collecting evidence")
        user_info = self.collect_user_info()
        posts = self.collect_posts()
        posts_with_comments = self.collect_comments_for_posts(posts)
        return {
            "user": user_info,
            "posts": posts,
            "posts_with_comments": posts_with_comments
        }


def main():
    client = Plugin()

    if not client.login(username="emilys", password="emilyspass"):
        return
    
    collected_data = client.evidence_collection()
    with open("output.json", "w") as f:
        json.dump(collected_data, f, indent=2)
        print("evidence written to output.json")

if __name__ == "__main__":
    main()
