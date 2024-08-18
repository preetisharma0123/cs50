import random
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from network.models import Posts, Comment, Like, Hashtag, Following
from django.utils import timezone
from faker import Faker
import re
from tweet_generator import tweet_generator

User = get_user_model()
fake = Faker()

class Command(BaseCommand):
    help = 'Generate dummy data for the Twitter-like website'

    def add_arguments(self, parser):
        parser.add_argument('--users', type=int, default=0, help='Number of users to create')
        parser.add_argument('--posts', type=int, default=0, help='Number of posts to create')
        parser.add_argument('--comments', type=int, default=0, help='Number of comments to create')
        parser.add_argument('--likes', type=int, default=0, help='Number of likes to create')
        parser.add_argument('--hashtags', type=int, default=0, help='Number of hashtags to create')

    def handle(self, *args, **options):
        self.create_users(options['users'])
        self.create_posts(options['posts'])
        self.create_following_relations()
        self.create_comments(options['comments'])
        self.create_likes(options['likes'])
        self.create_hashtags(options['hashtags'])
        self.assign_hashtags_to_posts()
        self.stdout.write(self.style.SUCCESS('Successfully generated dummy data'))

    def create_users(self, num_users):
        for _ in range(num_users):
            username = fake.user_name()
            email = fake.email()
            password = 'password'
            User.objects.create_user(username=username, email=email, password=password)
        self.stdout.write(f'Successfully created {num_users} users')

    def create_posts(self, num_posts):
        users = list(User.objects.all())
        for _ in range(num_posts):
            TPCK = '<public_consumer_key>'
            TSCK = '<secret_consumer_key>'
            TPAK = '<public_access_key>'
            TSAK = '<secret_access_key>'
            twitter_bot = tweet_generator.PersonTweeter('25073877',TPCK,TSCK,TPAK,TSAK)
            content = twitter_bot.generate_random_tweet()
            created_by = random.choice(users)
            post = Posts.objects.create(content=content, created_by=created_by)
            self.assign_hashtags_to_post(post)
        self.stdout.write(f'Successfully created {num_posts} posts')

    def assign_hashtags_to_post(self, post):
        content = post.content
        hashtags = re.findall(r"#(\w+)", content)
        for tag in hashtags:
            hashtag, created = Hashtag.objects.get_or_create(name=tag)
            post.hashtags.add(hashtag)
        self.stdout.write(f'Successfully assigned hashtags to post {post.id}')

    def create_following_relations(self):
        users = list(User.objects.all())
        for user in users:
            follow_instance = Following.objects.filter(user=user).first()
            if not follow_instance:
                follow_instance = Following(user=user)
                follow_instance.save()
            following = random.sample(users, random.randint(1, len(users) // 2))
            for follow_user in following:
                if follow_user != user:
                    follow_instance.following.add(follow_user)
        self.stdout.write('Successfully created following relations')

    def create_comments(self, num_comments):
        users = list(User.objects.all())
        posts = list(Posts.objects.all())
        for _ in range(num_comments):
            text = fake.sentence(nb_words=10)
            created_by = random.choice(users)
            post = random.choice(posts)
            Comment.objects.create(text=text, created_by=created_by, post=post)
        self.stdout.write(f'Successfully created {num_comments} comments')

    def create_likes(self, num_likes):
        users = list(User.objects.all())
        posts = list(Posts.objects.all())
        for _ in range(num_likes):
            liked_by = random.choice(users)
            post = random.choice(posts)
            like = Like.objects.filter(liked_by=liked_by, post=post).first()
            if like:
                like.like = not like.like
                like.save()
            else:
                Like.objects.create(liked_by=liked_by, post=post, like=True)
        self.stdout.write(f'Successfully created {num_likes} likes')

    def create_hashtags(self, num_hashtags):
        for _ in range(num_hashtags):
            name = fake.word()
            Hashtag.objects.create(name=name)
        self.stdout.write(f'Successfully created {num_hashtags} hashtags')

    def assign_hashtags_to_posts(self):
        posts = list(Posts.objects.all())
        hashtags = list(Hashtag.objects.all())
        for post in posts:
            assigned_hashtags = random.sample(hashtags, random.randint(1, 5))
            for hashtag in assigned_hashtags:
                post.hashtags.add(hashtag)
        self.stdout.write('Successfully assigned hashtags to posts')
