from django.db import models

class Post(models.Model):
    title = models.CharField(max_length=20)
    content = models.TextField()
    head_image = models.ImageField(upload_to='blog/images/%Y/%m/%d/', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    file_upload = models.FileField(upload_to='blog/files/%Y/%m/%d/', blank=True)

    # author
    # tags
    
    def __str__(self):
        return f'({self.pk}) {self.title}'
    
    def get_absolute_url(self):
        return f'/blog/{self.pk}'
    