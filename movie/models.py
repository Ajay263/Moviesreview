from django.db import models
from django.contrib.auth.models import User





class Movie(models.Model):
 title = models.CharField(max_length=100)
 description = models.CharField(max_length=250)
 image = models.ImageField(upload_to='movie/images/')
 url = models.URLField(blank=True)

 
class Review(models.Model):
 text = models.CharField(max_length=100)
 date = models.DateTimeField(auto_now_add=True)
 user = models.ForeignKey(User,on_delete=models.CASCADE)     #we are link the user field with an inbuilt odel called User,upon deleting the user the review will be deleted bt upon deleting the review the user will not be deleted 
 movie = models.ForeignKey(Movie,on_delete=models.CASCADE)   #movie is being link with another model called Movie,upon deleting the Movie model the movie review will be deleted and the opposite is not true
 watchAgain = models.BooleanField()

def __str__(self):
      return self.text