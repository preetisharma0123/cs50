from django.test import Client, TestCase
 from .models import *
# Create your tests here.

class PostTestCase(TestCase):

    def setUp(self):


    	# Create user.
    	u1 = User.objects.create(username="testuser1", email = "testuser1@example.com" )
    	u2 = User.objects.create(username="testuser2", email = "testuser2@example.com" )
        u3 = User.objects.create(username="testuser3", email = "testuser3@example.com" )

        # Create posts.
        p1 = Posts.objects.create(content="post1", timestamp="datetime.now() ", created_by = u1)
        p2 = Posts.objects.create(content="post2", timestamp="datetime.now() ", created_by = u2 )

        # Create Following.
        f1 = Following.objects.create(user_follow = u1, user_followed_by = u2 )
        f2 = Following.objects.create(user_follow = u2, user_followed_by = u1 )
        f3 = Following.objects.create(user_follow = u3, user_followed_by = u2)

        # Create Comment
        c1 = Comment.objects.create(post = p1, text = "nicely said", created_by = u3)
        c2 = Comment.objects.create(post = p2, text = "that's bad!", created_by= u1)
        c3 = Comment.objects.create(post = p3, text = "wow!", created_by= u2)

        # Create Like
        l1 = Like.objects.create(post = p1, like = True, created_by = u2)
        l2 = Like.objects.create(post = p1, like = True, created_by = u3)
        l3 = Like.objects.create(post = p2, like = True, created_by = u1)



def test_following(self):
    u1 = User.objects.get(username="testuser1")
    self.assertFalse(u1.follower, u1)


def test_index(self):

    # Set up client to make requests
    c = Client()

    # Send get request to index page and store response
    response = c.get("")

    # Make sure status code is 200
    self.assertEqual(response.status_code, 200)

    # Make sure three flights are returned in the context
    self.assertEqual(response.context["post"].count(), 2)


