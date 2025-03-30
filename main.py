import requests
from abc import ABC, abstractmethod
from dataclasses import dataclass
import json  # for organizing the output in a readable format

@dataclass
class PluginConfig:

    """Configuration for the plugin."""
    
    base_url: str # Base URL for the API endpoint!
    auth_endpoint: str # Authentication endpoint
    credentials: dict # Authentication credentials

class BasePlugin(ABC): # Inheriting from the ABC (Abstract Base Class)

    """The BasePlugin serves as an interface or blueprint for any plugin"""

    @abstractmethod
    def test_connectivity(self) -> tuple[bool, str]:
        """Perform a connectivity test (e.g., authentication)."""
        pass

    @abstractmethod
    def collect_evidence(self) -> dict:
        """Collect evidence data from the API."""
        pass

class DummyJSONPlugin(BasePlugin):
    def __init__(self, config: PluginConfig):
        self.config = config
        self.session = requests.Session()
        
    def test_connectivity(self):
        try:
            response = self.session.post(
                f"{self.config.base_url}{self.config.auth_endpoint}",
                json=self.config.credentials
            )
            response.raise_for_status()
            return True, "Connected successfully"
        except requests.HTTPError as e:
            status_code = e.response.status_code
            return False, f"HTTP Error {status_code}: {e.response.text}"
        except requests.RequestException as e:
            return False, f"Connection error: {str(e)}"
            
    def collect_evidence(self):
        return {
            "user": self._get("/auth/me"),
            "posts": self._get("/posts?limit=60"),
            "posts_with_comments": self._get_posts_with_comments()
        }
        
    def _get(self, endpoint):
        try:
            response = self.session.get(f"{self.config.base_url}{endpoint}")
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"Failed to GET {endpoint}: {str(e)}")
            return None
            
    def _get_posts_with_comments(self):
        posts_data = self._get("/posts?limit=60")
        if not posts_data:
            return None
        posts = posts_data.get("posts", [])
        for post in posts:
            comments_data = self._get(f"/posts/{post['id']}/comments")
            post["comments"] = comments_data.get("comments", []) if comments_data else []
        return posts

if __name__ == "__main__":
    # Define configuration for DummyJSON Plugin using Emily's credentials.
    config = PluginConfig(
        base_url="https://dummyjson.com",
        auth_endpoint="/auth/login",
        credentials={
            "username": "emilys",
            "password": "emilyspass",
            "expiresInMins": 30
        }
    )

    # Initialize the DummyJSON Plugin with the above configuration.
    plugin = DummyJSONPlugin(config)
    
    # Test connectivity with error handling.
    # If connectivity fails, print the error message, Otherwise, proceed to collect evidence.
    success, message = plugin.test_connectivity()
    print("Connectivity Test:", message)
    
    if success:
        # If connectivity passes, collect the evidence.
        evidence = plugin.collect_evidence()
        
        # E1: Print User Details
        # Organizing the output in a readable format
        print("\nE1 - User Details:")
        user_details = evidence.get("user")
        if user_details:
            print(json.dumps(user_details, indent=2))
        else:
            print("No user details found.")
        
        # E2: Print a summary of the 60 posts.
        # Organizing the output in a readable format
        print("\nE2 - 60 Posts:")
        posts_data = evidence.get("posts")
        if posts_data and "posts" in posts_data:
            for post in posts_data["posts"]:
                print(f"ID: {post['id']} | Title: {post['title']}")
        else:
            print("No posts found.")
        
        # E3: Print each post with its comments.
        # Organizing the output in a readable format
        print("\nE3 - Posts with Comments:")
        posts_with_comments = evidence.get("posts_with_comments")
        if posts_with_comments:
            for post in posts_with_comments:
                print(f"\nPost ID: {post['id']} | Title: {post['title']}")
                comments = post.get("comments", [])
                print(f"  Comments ({len(comments)}):")
                for comment in comments:
                    # Assuming each comment has a 'body' field. Adjust as necessary.
                    print(f"    - {comment.get('body', 'No content')}")
        else:
            print("No posts with comments found.")

    else:
        print("Please double-check your credentials and ensure your network is working properly.")

