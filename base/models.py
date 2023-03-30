from django.db import models
from datetime import datetime

# Create your models here.

class Article(models.Model):
    title=models.CharField(max_length=200)
    author=models.CharField(max_length=200)
    image = models.ImageField(upload_to='articlesImages/', blank=False)
    date=models.DateTimeField(default=datetime.now, blank=False)
    article_body=models.TextField()
    
    def __str__(self):
        return self.title
