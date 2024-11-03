from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    profile_image = models.ImageField(upload_to='./static/images', null=True, blank=True)
    bio = models.TextField(null = True)
    def __str__(self):
        return self.user.username
    def has_prof_img(self):
        return bool(self.profile_image)
    

class Room(models.Model):
    host = models.ForeignKey(User,on_delete= models.SET_NULL,null = True)
    name = models.CharField(max_length=100)
    topic = models.ForeignKey('Topic',on_delete= models.SET_NULL,null = True)
    description = models.TextField()
    participants = models.ManyToManyField(User, blank = True,related_name="participants")
    updated = models.DateTimeField(auto_now = True)
    created = models.DateTimeField(auto_now_add= True)
  
    def __str__(self):
        return self.name

class Message(models.Model):
    host = models.ForeignKey(User,on_delete= models.SET_NULL,null = True)
    room = models.ForeignKey('Room',on_delete= models.CASCADE)
    description = models.CharField(max_length=100)
    updated = models.DateTimeField(auto_now = True)
    created = models.DateTimeField(auto_now_add= True)
    class Meta:
        ordering = ['-updated','-created']
    def __str__(self):
        return self.description


class Topic(models.Model):
    name = models.CharField(max_length=100)        
    updated = models.DateTimeField(auto_now = True)
    created = models.DateTimeField(auto_now_add= True)
    def __str__(self):
        return self.name



