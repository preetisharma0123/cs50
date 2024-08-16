from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from django.db.models import Count
from datetime import timedelta


class User(AbstractUser):
    pass
    # Add custom fields
    # username = models.CharField(max_length=191,blank = False,unique = True)
    # email = models.EmailField(primary_key = True, unique = True)    

    # def __str__(self):
    #   return "{}".format(self.email)


class Following(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="follow_instance")
    following = models.ManyToManyField(User, blank=True, related_name="followers")

    def __str__(self):
        return f"{self.user.username} is following {self.following.count()} users"



class Posts(models.Model):
    # Existing fields...
    content = models.CharField(max_length=64, blank=False, unique=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, blank=False, related_name="user_posts")

    def serialize(self):
        return {
            "id": self.id,
            "content": self.content,
            "timestamp": self.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
            "created_by": self.created_by.username,
            "hashtags": [hashtag.name for hashtag in self.hashtags.all()],
        }

    def __str__(self):
        return f"{self.created_by} at {self.timestamp} wrote {self.content}"

    def is_valid_post(self):
        return len(self.content) > 0 and self.timestamp >= datetime.now()

class Comment(models.Model):
     # create comment model
    post = models.ForeignKey(Posts, on_delete=models.CASCADE, null = True, blank = True,related_name = "comments")
    text = models.CharField(max_length=500,blank = True)
    created_by = models.ForeignKey(User,on_delete=models.CASCADE, related_name='commented')
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.text} -by {self.created_by}"


    def is_valid_comment(self):
        return self.comment.length>0

    def serialize(self):
        return {
            "id": self.id,
            "post" : self.post.serialize(),
            "text" : self.text,
            "created_by" : self.created_by.username, 
            "timestamp": self.timestamp.strftime("%Y-%m-%d %H:%M:%S")
            
        }


class Like(models.Model):
    # create like model
    post = models.ForeignKey(Posts, on_delete=models.CASCADE, null = True, blank = True,related_name = "likes")
    like = models.BooleanField(max_length=100,unique = False)
    liked_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='liked')
    timestamp = models.DateTimeField(auto_now_add=True)
    

    def serialize(self):
        return {
            "id": self.id,
            "post" : self.post,
            "like" : self.like,
            "liked_by" : self.liked_by.username, 
            "timestamp": self.timestamp.strftime("%Y-%m-%d %H:%M:%S")
                        
        }


  
class Hashtag(models.Model):
    name = models.CharField(max_length=64, unique=True)
    posts = models.ManyToManyField('Posts', related_name='hashtags')

    def __str__(self):
        return f"#{self.name}"

    @staticmethod
    def get_trending_hashtags():
        one_hour_ago = timezone.now() - timedelta(hours=1)
        hashtags = Hashtag.objects.filter(posts__timestamp__gte=one_hour_ago) \
            .annotate(num_posts=Count('posts')) \
            .order_by('-num_posts')
        return hashtags[:10]  # Return top 10 trending hashtags