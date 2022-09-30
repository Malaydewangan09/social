from django.contrib.auth import get_user_model
from django.db import models
from app_api.helpers import code_generator

User = get_user_model()

SEX_CHOICES = (('Male', 'Male'), ('Female', 'Female'))
FRIEND_REQUEST_CHOICES = (('Accept', 'Accept'), ('Reject', 'Reject'), ('Pending', 'Pending'))
LIKE_CHOICES = ((1, 'Like'), (0, 'None'))
FOLLOW_CHOICES = (('Follow', 'Follow'), ('Unfollow', 'Unfollow'))


class UserProfile(models.Model):
    user = models.OneToOneField(
        verbose_name='user',
        to=User,
        on_delete=models.CASCADE,
        related_name='user_profile'
    )
    sex = models.CharField(max_length=6, choices=SEX_CHOICES, null=True, blank=True)
    age = models.IntegerField(null=True, blank=True)
    bio = models.CharField(max_length=240, blank=True)
    city = models.CharField(max_length=30, blank=True)
    avatar = models.ImageField(null=True, blank=True)
    code = models.CharField(
        verbose_name='code',
        help_text='random code used for registration and for password reset',
        max_length=15,
        default=code_generator,
        null=True,
        blank=True
    )

    def __str__(self):
        return self.user.username


class Post(models.Model):
    author = models.ForeignKey(
        to=User,
        verbose_name='user',
        on_delete=models.CASCADE,
        related_name='posts'
    )
    title = models.CharField(max_length=200)
    body = models.TextField()
    image = models.ImageField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Reaction(models.Model):
    class Meta:
        unique_together = (('user_reacted', 'posts', 'status'),)

    user_reacted = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name='user_reacted')
    # GIVE NAME "posts" IN ORDER TO RELATE WITH post table --> field 'author' related name = 'posts'
    posts = models.ForeignKey(
        to=Post,
        on_delete=models.CASCADE,
        related_name='post_reactions')
    status = models.IntegerField(choices=LIKE_CHOICES, default=1)

    def __str__(self):
        if self.status == 1:
            return f"{str(self.user_reacted).upper()} Liked: {self.posts}"
        if self.status == 0:
            return f"{str(self.user_reacted).upper()} Unliked: {self.posts}"


class Friendship(models.Model):
    class Meta:
        unique_together = (('receiver', 'sender', 'status'),)
        unique_together = (('sender', 'receiver', 'status'),)

    status = models.CharField(max_length=8, choices=FRIEND_REQUEST_CHOICES, null=True, blank=True, default='Pending')
    from_date = models.DateTimeField(auto_now_add=True)
    receiver = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name='user1')
    sender = models.ForeignKey(to=User,
                               on_delete=models.CASCADE,
                               related_name='user2')

    def __str__(self):
        if self.status == 'Accept':
            return f"ACCEPTED: {str(self.receiver).upper()} and {str(self.sender).upper()} are now friends! "
        if self.status == 'Reject':
            return f"REJECTED: {str(self.receiver).upper()} rejected {str(self.sender).upper()}"
        if self.status == 'Pending':
            return f"PENDING: {str(self.sender).upper()}'s request to {str(self.receiver).upper()} is pending...."


class Follow(models.Model):
    class Meta:
        unique_together = (('receiver', 'sender', 'status'),)

    status = models.CharField(max_length=8, choices=FOLLOW_CHOICES, default='Follow')
    from_date = models.DateTimeField(auto_now_add=True)
    receiver = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name='followed')
    sender = models.ForeignKey(to=User,
                               on_delete=models.CASCADE,
                               related_name='follower')

    def __str__(self):
        if self.status == 'Follow':
            return f"{str(self.sender).upper()} Follows {str(self.receiver).upper()}"
        if self.status == 'Unfollow':
            return f"{str(self.sender).upper()} Unfollowed {str(self.receiver).upper()}"
