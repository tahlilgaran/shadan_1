from django.db import models
from datetime import datetime
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User)
    location = models.CharField(max_length=250, null=True,blank=True)
    picture = models.FileField(upload_to="static/users/img/", default="static/users/img/default.jpg" , null=True, blank=True)
    birthday = models.DateField()

    def __str__(self):
        return "{}".format(self.user.username)
    def age(self):
        year = datetime.now().year
        age = year - self.birthday.year
        return age


class Follow(models.Model):
    follower = models.ForeignKey(Profile , related_name='follower')
    followed = models.ForeignKey(Profile , related_name='followed')

    def __str__(self):
        return "follower: {} - followed: {}".format(self.follower.user.username , self.followed.user.username)


class Notification(models.Model):
    user = models.ForeignKey(User ,related_name='notification')
    producer = models.ForeignKey(Profile)
    content = models.TextField()
