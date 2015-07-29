from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Film)
admin.site.register(FilmCrew)
admin.site.register(PostComment)
admin.site.register(Post)
admin.site.register(Actor)
admin.site.register(Like)