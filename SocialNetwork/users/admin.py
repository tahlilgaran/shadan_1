from django.contrib import admin
from .models import Follow,Profile,Notification

# Register your models here.
admin.site.register(Follow)
admin.site.register(Profile)
admin.site.register(Notification)