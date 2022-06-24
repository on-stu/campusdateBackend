
from uuid import uuid4
from django.db import models
from django.contrib.auth.models import (BaseUserManager, AbstractBaseUser)


class UserManager(BaseUserManager):
    def create_user(self, email, password):
        if not email:
            raise ValueError('Users must have an email email')

        user = self.model(
            email=email,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        user = self.create_user(
            email=email,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    username = None
    email = models.EmailField(max_length=30, unique=True, blank=True)
    password = models.CharField(max_length=255, blank=True)
    photoUrl = models.FileField(upload_to='imgs/%Y/%m/%d/%H/%M/%S', blank=True)
    nickname = models.CharField(max_length=20, blank=True)
    sex = models.CharField(max_length=8, blank=True)
    birthday = models.DateTimeField(null=True)
    payments = models.JSONField(default=list)
    myHobbies = models.JSONField(default=list)
    myIdeals = models.JSONField(default=list)
    whoAmI = models.JSONField(default=list)
    introduction = models.TextField(max_length=500, blank=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    chatRooms = models.JSONField(default=list)
    university = models.CharField(max_length=20, blank=True)
    accepted = models.JSONField(default=list)
    objects = UserManager()
    myHobbiesScore = models.JSONField(default=list)
    myIdealsScore = models.JSONField(default=list)
    whoAmIScore = models.JSONField(default=list)
    private = models.BooleanField(default=False)
    skipUser = models.JSONField(default=list)
    userNotificationToken = models.CharField(max_length=100, blank=True)

    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin


class PushToken(models.Model):
    userId = models.IntegerField()
    # pushToken = models.CharField()
    # dafsdfawefadvsd
    #sadfadfawefw


class Notice(models.Model):
    title = models.CharField(max_length=50, blank=True)
    isImportant = models.BooleanField(default=True)
    content = models.TextField(max_length=500, blank=True)
    authorId = models.IntegerField(blank=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    comments = models.JSONField(default=list)
    thumbs = models.JSONField(default=list)


class Faq(models.Model):
    title = models.CharField(max_length=50, blank=True)
    done = models.BooleanField(default=False)
    content = models.TextField(max_length=500, blank=True)
    authorId = models.IntegerField(blank=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    isSecret = models.BooleanField(default=True)
    answers = models.JSONField(default=list)


class Report(models.Model):
    title = models.CharField(max_length=50, blank=True)
    done = models.BooleanField(default=False)
    content = models.TextField(max_length=500, blank=True)
    authorId = models.IntegerField(blank=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    isSecret = models.BooleanField(default=True)
    answers = models.JSONField(default=list)


class ChatRoom(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    creatorId = models.IntegerField(default=0)
    participants = models.JSONField(default=list)
    lastAt = models.DateTimeField(auto_now=True)


class Chats(models.Model):
    senderId = models.CharField(blank=True, max_length=100000)
    receiverId = models.CharField(blank=True, max_length=100000)
    content = models.TextField()
    createdAt = models.DateTimeField(auto_now_add=True)
    isRead = models.BooleanField(default=False)
    chatRoomId = models.ForeignKey(
        "ChatRoom", related_name='chats', on_delete=models.CASCADE, db_column='chat_room_id')


class Charm(models.Model):
    title = models.CharField(max_length=50, blank=True)
    content = models.TextField(max_length=500, blank=True)
    authorId = models.IntegerField(blank=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    comments = models.JSONField(default=list)
    thumbs = models.JSONField(default=list)
    isAnonymous = models.BooleanField(default=True)


class Review(models.Model):
    title = models.CharField(max_length=50, blank=True)
    content = models.TextField(max_length=500, blank=True)
    authorId = models.IntegerField(blank=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    comments = models.JSONField(default=list)
    thumbs = models.JSONField(default=list)
    isAnonymous = models.BooleanField(default=True)


class Event(models.Model):
    title = models.CharField(max_length=50, blank=True)
    isActive = models.BooleanField(default=True)
    content = models.TextField(max_length=500, blank=True)
    authorId = models.IntegerField(blank=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    comments = models.JSONField(default=list)
    thumbs = models.JSONField(default=list)
