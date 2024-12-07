from django.db import models

# Create your models here.

class LoginTable(models.Model):
    username = models.CharField(max_length=1000, unique=True)
    email = models.EmailField(max_length=255, default='example@example.com')
    password = models.CharField(max_length=1000)
    type = models.CharField(max_length=1000)  

class Course(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    
    def __str__(self):
        return self.name

    
class Video(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(default="Default description for videos") 
    url = models.URLField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    order = models.PositiveIntegerField() 
    is_locked = models.BooleanField(default=True) 

    def __str__(self):
        return self.title

class UserProgress(models.Model):
    user = models.ForeignKey(LoginTable, on_delete=models.CASCADE) 
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    is_watched = models.BooleanField(default=False) 

    def __str__(self):
        return f"{self.user.username} - {self.video.title} - Watched: {self.is_watched}"