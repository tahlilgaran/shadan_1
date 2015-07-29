from django.db import models
import datetime
from users.models import Profile,User


class FilmCrew(models.Model):
    director = models.CharField(max_length=250)
    producer = models.CharField(max_length=250)
    writer = models.CharField(max_length=250)
    player1 = models.CharField(max_length=250)
    player2 = models.CharField(max_length=250 , null=True,blank=True)

    def __str__(self):
        return "crews group for {}".format(self.director)


class Film(models.Model):
    title = models.CharField(max_length=250)
    link = models.CharField(max_length=250)
    picture = models.FileField(upload_to="static/network/img/", default="static/users/img/default.jpg" , null=True, blank=True)
    film_crew = models.OneToOneField(FilmCrew)
    rating = models.FloatField(default=0)
    text = models.TextField()
    total_rate = models.IntegerField(default=0)

    def __str__(self):
        return "{}".format(self.title)

class Post(models.Model):
    film = models.ForeignKey(Film)
    body = models.TextField(blank=True, null=True)
    author = models.ForeignKey(Profile)
    pub_date = models.DateTimeField(default=datetime.datetime.now)
    numlike = models.IntegerField(default=0)
    numComments = models.IntegerField(default=0)

    def __str__(self):
        return "{} posted for {}".format(self.author.user.username, self.film.title)


class PostComment(models.Model):
    post = models.ForeignKey(Post,related_name='postcomments')
    user = models.ForeignKey(Profile)
    comment = models.TextField()
    timestamp = models.DateTimeField(default=datetime.datetime.now)

    def __str__(self):
        return "{} commented for {}".format(self.user.user.username, self.post.film.title)


class Like(models.Model):
    liker = models.ForeignKey(User,related_name='like')
    post = models.ForeignKey(Post,related_name='like')

    def __str__(self):
        return "{} liked {} for {}".format(self.liker.username, self.post.film.title, self.post.author.user.username)


class Actor(models.Model):
    name = models.CharField(max_length=255)
    part = models.CharField(max_length=255)
    film = models.ForeignKey(Film)

    def __str__(self):
        return "{} actor for {}".format(self.name, self.film.title)