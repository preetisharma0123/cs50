from django.test import Client, TestCase
from .models import *
from selenium import webdriver
import os
import pathlib
import unittest

# Create your tests here.

class PostTest(TestCase):

    def setUp(self):
        print('here')

        # Create users, posts, following, comments, and likes
        u1 = User.objects.create(username="testuser1", email="testuser1@example.com")
        u2 = User.objects.create(username="testuser2", email="testuser2@example.com")
        u3 = User.objects.create(username="testuser3", email="testuser3@example.com")

        p1 = Posts.objects.create(content="post1", created_by=u1)
        p2 = Posts.objects.create(content="post2", created_by=u2)

        Following.objects.create(user_follow=u1, user_followed_by=u2)
        Following.objects.create(user_follow=u2, user_followed_by=u1)
        Following.objects.create(user_follow=u3, user_followed_by=u2)

        Comment.objects.create(post=p1, text="nicely said", created_by=u3)
        Comment.objects.create(post=p2, text="that's bad!", created_by=u1)
        Comment.objects.create(post=p1, text="wow!", created_by=u2)

        Like.objects.create(post=p1, like=True, created_by=u2)
        Like.objects.create(post=p1, like=True, created_by=u3)
        Like.objects.create(post=p2, like=True, created_by=u1)


    def test_following1(self):
        u1 = User.objects.get(username="testuser1")
        self.assertFalse(u1.followers.contains(u1))

    def test_following2(self):
        u2 = User.objects.get(username="testuser2")
        self.assertTrue(u2.following.contains(u1))


    def test_index(self):

        # Set up client to make requests
        c = Client()

        # Send get request to index page and store response
        response = c.get("/post/")

        """ Make sure status code is 200"""
        self.assertEqual(response.status_code, 200)

        """ Make sure 2 posts are returned in the context"""
        self.assertEqual(response.context["post"].count(), 2)


class WebpageTests(unittest.TestCase):

    def setUp(self):
        """ Finds the Uniform Resource Identifier of a file"""
        self.driver = webdriver.Chrome()

    def tearDown(self):
        # Close the browser window
        self.driver.quit()
    
    def file_uri(filename):
        """Finds the Uniform Resourse Identifier of a file"""
        return pathlib.Path(os.path.abspath(filename)).as_uri()

    def test_title(self):
        """Make sure title is correct"""
        driver.get(file_uri("layout.html"))
        self.assertEqual(self.driver.title, "Social Network")

    def test_new_post(self):
        """Make sure new post is submitted"""

        self.driver.get(file_uri("index.html"))
        textarea  = self.driver.find_element_by_id("post_content")
        submit_button = self.driver.find_element_by_id("submit")

        # Type something into the textarea
        textarea.send_keys("This is a new post content")

        # Click the submit button to submit the form
        submit_button.click()

        # Wait for a few seconds to see the result
        self.driver.implicitly_wait(5)

        # Assert test
        self.assertEqual(self.driver.find_element_by_tag_name("ul").text, "1")
       
if __name__ == "__main__":
    unittest.main()
