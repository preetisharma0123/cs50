from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass
    # Add custom fields
    # username = models.CharField(max_length=191,blank = False,unique = True)
    # email = models.EmailField(primary_key = True, unique = True)    

    # def __str__(self):
    #   return "{}".format(self.email)


class Posts(models.Model):
    # create post model
    content = models.CharField(max_length=64, blank = False, unique = True)
    timestamp = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User,on_delete=models.CASCADE, blank = False, related_name="user_posts")

    def __str__(self):
        return f"{self.created_by} at {self.timestamp} wrote {self.content}"

    def is_valid_post(self):
        return self.content.length>0 and self.timestamp>= datetime.now() 



class Following(models.Model):
    #users the user is following 
    user_follow = models.ManyToManyField(User, blank = True, related_name="follower")
    #users the user is followed by 
    user_followed_by = models.ManyToManyField(User,blank = True, related_name="followed_by")


class Comment(models.Model):
     # create comment model
    post = models.ForeignKey(Posts, on_delete=models.CASCADE, null = True, blank = True,related_name = "comments")
    text = models.CharField(max_length=500,blank = True)
    created_by = models.ForeignKey(User,on_delete=models.CASCADE, related_name='comments')


    def __str__(self):
        return f"{self.text} -by {self.created_by}"


    def is_valid_comment(self):
        return self.comment.length>0


class Like(models.Model):
    # create like model
    post = models.ForeignKey(Posts, on_delete=models.CASCADE, null = True, blank = True,related_name = "likes")
    like = models.BooleanField(max_length=100,unique = False)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='liked')


  