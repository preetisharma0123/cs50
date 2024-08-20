import random
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from network.models import Posts, Comment, Like, Hashtag, Following
from django.utils import timezone
from faker import Faker
import re

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
            content = generate_tweet()
            created_by = random.choice(users)
            post = Posts.objects.create(content=content, created_by=created_by)
            self.assign_hashtags_to_post(post)
        self.stdout.write(f'Successfully created {num_posts} posts')

    def assign_hashtags_to_post(self, post):
        content = post.content
        hashtags = re.findall(r"#(\S+)", content)
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




# List of possible tweet contents


tweet_fragments = """Just saw the most amazing sunset!, #amazing, 
Can't believe how great this new coffee shop is!, 
Started a new book today, it's #fantastic!, 
Working out is getting easier every day., 
Had an awesome time with friends last night.,
This new tech gadget is a game changer!,
Loving the weather today, perfect for a walk.,
Just finished a challenging project at work. #feeling-accomplished,
Cooking up a storm in the kitchen tonight!,
Exploring new hobbies can be so #rewarding.,
Anyone else excited for the weekend?,
Feeling grateful for all the little things. #feeling-blessed,
New favorite song on repeat all day!,
The view from my office is stunning today.,
#Travel plans are finally coming together.,
Just watched an incredible movie.,
Getting ready for a big presentation tomorrow.,
Family time is the best time.,
Staying positive and productive.,
Reflecting on how far I've come.,
Can't get enough of this amazing app!, #amazing,
Learning something new every day.,
Enjoying some well-deserved relaxation.,
This book just keeps getting better!,
Feeling inspired to start a new project.,
Nature walks are so refreshing. #Nature,
Making the most of every moment.,
Feeling motivated and energized.,
New recipes are always fun to try.,
Grateful for the supportive people in my life. #feeling-blessed,
Taking time to appreciate the small things.,
Just wrapped up a successful meeting.,
Exploring new places is always exciting.,
Setting new goals and working towards them.,
Loving the new workout routine!,
Enjoying a quiet evening at home.,
Feeling accomplished after a productive day.,
Trying out a new hobby today.,
Making progress one step at a time.,
Grateful for the opportunity to learn and grow. #feeling-blessed,
Excited about upcoming adventures!,
Finding joy in the little things.,
Embracing change and new challenges.,
This new playlist is fire!,
Relaxing with a good book tonight.,
Feeling positive and uplifted.,
New experiences are the best.,
Just signed up for an interesting workshop.,
Taking a break to recharge.,
Celebrating small victories.,
Feeling content and at peace.,
Can't wait for the next episode!,
Had a #fantastic day at the park.,
Finding balance in daily life.,
Learning to live in the moment.,
Grateful for the journey. #feeling-blessed,
Discovering new passions.,
Taking care of myself.,
Feeling connected and happy.,
Enjoying quality time with loved ones. #loved,
Finding inspiration in nature. #nature,
Making time for what matters.,
Feeling hopeful and excited for the future. #Goals,
New beginnings are always exciting.,
Loving this new adventure I'm on.,
Finding strength in challenges.,
Feeling blessed and thankful.,
Pushing myself to be better.,
Enjoying the simple pleasures of life.,
Just completed a major milestone!,
Feeling empowered and motivated.,
Appreciating the beauty around me.,
Making every day count.,
Feeling refreshed and rejuvenated.,
Taking on new challenges with confidence.,
Living life to the fullest.,
Embracing each day with positivity.,
Feeling grateful for today. #feeling-blessed,
Learning to love the journey. #love,
Finding peace in the present moment.,
Making time for creativity.,
Feeling excited about what's to come.,
Celebrating personal growth.,
Finding joy in everyday moments.,
Living with intention.,
Feeling inspired to make a difference.,
Grateful for the love and support around me. #love #feeling-blessed,
Taking steps towards my dreams.,
Feeling fulfilled and happy.,
Making the most of every opportunity.,
Learning to appreciate the journey.,
Feeling optimistic about the future. #Goals,
Creating new memories every day.,
Grateful for the lessons learned. #feeling-blessed,
Feeling determined and focused.,
Making positive changes in my life.,
Living with gratitude and joy. #feeling-blessed,
Feeling connected to the world around me.,
Finding joy in simple things.,
Embracing new opportunities with open arms.,
Feeling proud of my accomplishments.,
Making progress every day.,
Grateful for the support system I have. #feeling-blessed,
Feeling excited about new possibilities.,
Taking time to reflect and appreciate.,
Feeling empowered to make a change.,
Living with purpose and passion.,
Grateful for the journey so far. #feeling-blessed,
Feeling inspired by the people around me.,
Making a positive impact in my community.,
Finding joy in helping others.,
Living each day with a grateful heart. #feeling-blessed,
Feeling hopeful and inspired.,
Embracing each day as a new opportunity.,
Finding beauty in the everyday moments.,
Making time for what truly matters.,
Grateful for the chance to grow and learn. #feeling-blessed,
Feeling at peace with where I am.,
Making a difference, one step at a time.,
Feeling inspired to chase my dreams.,
Living a life full of love and joy. #love,
Grateful for the opportunities ahead. #feeling-blessed,
Feeling blessed and fortunate.,
Making every moment count.,
Living with an attitude of gratitude. #feeling-blessed,
Feeling thankful for all the support.,
Embracing each day with a smile.,
Finding joy in the journey.,
Feeling motivated to achieve my goals.,
Living life with purpose and meaning.,
Grateful for the beautiful moments. #feeling-blessed,
Feeling at peace and content.,
Living with a heart full of gratitude. #feeling-blessed,
Feeling inspired to create positive change.,
Grateful for the love and kindness around me. #love #feeling-blessed,
Feeling hopeful for the future. #Goals,
Living each day with joy and purpose.,
Feeling grateful for the little things. #feeling-blessed,
Making time for self-care and relaxation.,
Living with a positive mindset.,
Feeling inspired by the beauty of nature. #nature,
Grateful for the journey and the lessons learned. #feeling-blessed,
Feeling motivated to keep pushing forward.,
Living each day to the fullest.,
Feeling thankful for the support and love. #love,
Making time for what I love. #love,
Living a life of gratitude and joy. #feeling-blessed,
Grateful for the opportunities to grow. #feeling-blessed,
Feeling at peace with my journey.,
Making a positive impact in the world.,
Living with a grateful heart. #feeling-blessed,
Feeling excited for the future. #Goals,
Grateful for the support and encouragement. #feeling-blessed,
Feeling inspired to be my best self.,
Living each day with intention and purpose.,
Feeling hopeful and optimistic.,
Grateful for the beautiful journey. #feeling-blessed,
Feeling blessed and happy.,
Making every day a new adventure.,
Living with love and gratitude. #love #feeling-blessed,
Feeling inspired to achieve great things.,
Grateful for the support and love of family. #love #feeling-blessed,
Feeling motivated to pursue my dreams.,
Living each day with passion and purpose.,
Feeling at peace with my path.,
Grateful for the chance to make a difference. #feeling-blessed,
Feeling excited about new adventures.,
Living each day with gratitude and joy. #feeling-blessed,
Feeling excited for the journey ahead.,
Just saw the most amazing sunset! #sunset, #amazing,
Can't believe how great this new coffee shop is! #coffee,
Started a new book today, it's #fantastic! #newbook,
Working out is getting easier every day. #workout,
Had an awesome time with friends last night. #friends,
This new tech gadget is a game changer! #tech,
Loving the weather today, perfect for a walk. #weather,
Just finished a challenging project at work. #work #feeling-accomplished,
Cooking up a storm in the kitchen tonight! #cooking,
Exploring new hobbies can be so #rewarding. #newhobbies,
@Bill_Porter All posts from your website http://t.co/NUWn5HUFsK seems to have been deleted. I am getting a Not Found page even in homepage,http://www.billporter.info/,
@sudhamshu: Billed as Comet of the century, Comet C/12 S1(ISON) is on its way to light up our night skies (later in November this y ...,
@sudhamshu ..and we should also be prepared to view some stupid news channel doing an exclusive whether world is going to end or not,
@sudhamshu Wow!! time to invest on a better telescope and camera.,
@sudhamshu Will it be visible from Indian skies?,
Just got the connection from ACT Broadband. I am getting around 19 mbps for a 15 mbps connection. So far so good :) http://t.co/4MM1TTmqxF,http://twitter.com/sudarmuthu/status/3176154224449536/photo/1,
What is the process to repoemail spam (offers emails)? @ICICIBank_Care is sending me lot of spam without an option to unsubscribe,
@ICICIBank_Care Also in your spam (offers) emails, there is no link to unsubscribe. Also I didn't subscribe to it in the first place.,
@ICICIBank_Care I have already done that! thrice!!, but you keep sending me spam. Just today I got more than 2 spam (offers) mails from you,
@surajram Look around and observe the people around you. You can find people with different emotions around.,
FYI, @ICICIBank_Care I have given my email so that you can send me my statement. But you are spamming me, without any option to unsubscribe,
@realsubbuj @aswinanand I have not used #ingress,
@subbuj I write my blog article in markdown from Vim and then publish it in my site running WordPress using Vimpress http://t.co/Sljq7CU4Pf,http://www.vim.org/scripts/script.php?script_id=35,
@realsubbuj I have no issues if the subject line contains only text. If it contains a link then it becomes very difficult to open it.,
I hate it when someone sends me an url in the subject of the email while keeping the body empty.,
@jackerhack: We're hosting a workshop on data processing with Pig this April. @sudarmuthu is facilitating. http://t.co/OgvQEsdH5c,http://pigworkshop.fifthelephant.in/,
@hardwarefun: A guide to choosing correct accessories for @raspberry_pi with lot of options to source locally if needed http://t.co/x ...,
@PervyTeen Sure. Will let you know after I get my connection.,
@v1pl @ckailash @realsubbuj @PVRTweets Thanks for the details. I have applied for ACT broadband. Keeping my fingers crossed ;),
@realsubbuj I am not sure if it is available in my area though...,
@ckailash Yeah, he already told me about it. Any idea how much is the discount?,
@ckailash Wow! that's good to know. Hopefully it will end all my broadband issues. Also, the service guy was very professional.,
@varunkumar That's good to know.,
@galuano1 Yeah I have a poright across my home and the service guy said he can give me connection.,
As anyone used ACT broadband in Bangalore? They are promising 15 and 25 mbps. Not sure whether I can trust them.,
@tryprasannan Open source is the right way to go. But how to convince the guys responsible for making the decision?,
@AtulChitnis: RIP famous Bangalore weather. It was nice knowing you. But now you are being replaced by an Airconditioner :(,
@tryprasannan That's a good point. Hopefully the people who set up these rules think about it.,
@prashanth What feature is that?,
Govt of India has come up with a Mobile application contest. Details at http://t.co/xdhBotUv5H,http://appscontest.mgov.gov.in/mainpage.jsp,
Someone had forked my wedding invitation http://t.co/R6oIEFJLJB at @github https://t.co/U6lRscygZs Cool :),http://sudarmuthu.com/blog/how-i-designed-my-wedding-invitation,https://github.com/metrofx/wedding-invitation,
Daylight time change will happen in a couple of hours. This is the first time for me to experience it and hopefully I don't get confused ;),
Planning to go to Yosemite Park tomorrow. Hopefully the whether stays the same way.,
@UberFacts In many countries (like Bhutan) they calculate their age by adding this 9 months.,
@balajijegan Will come over to your cube later today or Monday :) You are in building B right?,
Help needed: If you have access to an Ubuntu box right now can you kindly check if this script works http://t.co/H2gsTmxESs? Thanks.,http://stackoverflow.com/a/24733/24949,
@marissamayer: Excited to see the grand lighting of the Bay Lights in San Francisco!  So beautiful! http://t.co/nCk3hvpkDX,http://flic.kr/p/dZZnEP,
Question: Do we have to disable DND completely to receive sms from Google Voice in India? Does enabling a particular category help?,
@AtulChitnis: Wow. Ankit Fadia Revealed http://t.co/CBbrkjmZN0,http://atul.ch/15MksaA,
Email from @Airtel_Presence Your mobile Internet usage as on 25-Feb-13 is Mb which is % ... They forgot to replace values in template ;),
@sudhamshu: An interactive map of all the recorded meteorite landing places on Earth. http://t.co/OM2EDjAL,http://www.guardian.co.uk/news/datablog/interactive/13/feb/15/meteorite-fall-map,
@msnarain @TakkarMachi @Fluid_Head Also a nice addition would be photography + uploading a couple of them to social network sites.,
@gauravl ha ha. You have a strong memory. If your GovWiki app is available now anywhere, I would definitely use it :),
@BabaSherlock I am still on 2.3.7 since HTC Hero doesn't suppocynogenmod with Jelly Bean.,
@BabaSherlock Okay just updated. Didn't choose to wipe data and cache. Rom got updated after reboot and my data and apps are still there.,
@BabaSherlock Thanks. Also read that it is better to do a backup using Titanium Backup. Doing that as well before updating.,
@BabaSherlock Yes I have @CyanogenMod installed. Rom manager just told me that there is an update and has downloaded it. Phone HTC Hero,
@BabaSherlock So if I backup and then update @CyanogenMod Is it possible to restore only apps and data? How to do it?,
Question: If I update my @CyanogenMod ROM, using ROM Manager will it wipe my data and apps or they will be retrained? #android,
Out of ~0 friends that I have in Facebook, I just found that ~15 have closed their accounts. Is this starting of a trend?,
These days @Airtel_Presence is adding a person's name at the end of their replies. Nice move. It gives a personal touch.,
@mayurpipaliya ha ha. Guilty as charged ;) Hope you enjoy them :),
Every few months @Airtel_Presence randomly activates some service for me. Now they started sending me some crap as MMS from 58685.,
Suddenly after moving from -something to -something over the weekend, I  feel more mature, or is it just my mind playing games again ;),
@InfinityO_O Can you give me more details about the corpus. I followed your link, but it is asking for a login.,
@mbanzi: save % on select Arduino ebooks and videos from http://t.co/zUDOilft use code WKARD,http://oreilly.com,
@asanjum Keep us updated, if you receive any reply to it.,
@tamil Do you have the schematics for this module?,
@jackerhack You complained via the Android app? @seventymm is spamming me and wouldn't stop even after I wrote to their CEO,
@CaucusLiberty Is your issue fixed?,
@ICICIBank_Care I have DM'ed my details. Hoping to get a call soon,
@ICICIBank_Care You have sent me a credit card without me applying for it. How do I make sure it is blocked and I don't have to pay for it?,
@abh33k Sure. Are you also based out of Bangalore?,
@rakesh314 It costs around twice that of a @raspberry_pi :( Thanks for the link though.,
@rakesh314 do you have a link?  Also did it come with the micro usb cable to connect to @raspberry_pi?,
@rakesh314 hey how did you power your pi robot for node.js talk? Which battery were you using?,
@varunkumar I am planning to conduct one in Chennai, but the main issue is logistics :( @hardwarefun,
@hardwarefun: The next batch of my Creating robots using @Arduino workshop will happen on Jan 26-27th http://t.co/8e4WJcvi,http://hardwarefun.com/arduino-workshop,
I like the new stats about users that @github  has started showing in user profile pages.,
I completely hate @ICICIBank_Care new design. I have to do 3-4 clicks to get to the login page. They have filed the homepage with banners,
@CruciFire You can find pics and the explanation about my wedding card design at http://t.co/pkB9q1u7,http://sudarmuthu.com/blog/how-i-designed-my-wedding-invitation,
I waited yesterday at passpooffice for 7 hours to renew my passport. Next I have to follow up for police verification.,
@vatsala The appointments get over in less than 0 sec and you have to fill up 3-4 capchas. Tougher than booking IRCTC Takal tickets.,
@vatsala Yeah even I am surprised that it works :) I tried continuously for a month every day at 6PM (it varies from city to city),
YES!! YES!! YES!!, I finally managed to book the appointment online for my passporenewal after trying for nearly a month.,
@hardwarefun: Some interesting stats. 2.32% of the traffic to @arduino site is from India. Would personally want this to go up :) (cc ...,
@Rathnavelrat Let's hope that *sorcery* continues ;),
@subbuj Are you sure we can get an offline appointment? I heard they have only online appointment now :(,
@sudhamshu I would be happy if it applies to *programming* languages as well ;),
@viralsachde The slots open at 6PM and are finished by 6:01 PM. You have to type 4 capchas and 5 page refresh to book the appointment :(,
@calvinscorner I would say IRCTC is relatively better than Passposite. Anyways I think now I have to approach a broker and pay bribe :(,
I have still not managed to book the passporenewal appointment online. I have been trying for the past 2 weeks :(,
@subbuj Time to stausing Flickr ;),
@hardwarefun: If you have a cool @arduino project and want it to get featured in @arduinoblog then add it at http://t.co/4TY7dvSH,http://arduino.cc/blog/submit-your-project/,
I am seriously thinking of moving all my WordPress Plugins http://t.co/CEVlxinO to @github,http://sudarmuthu.com/wordpress/,
""".split(",\n")

def generate_tweet():
    tweet = random.choice(tweet_fragments)
    return f"{tweet}"

