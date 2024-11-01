from django.db import models

class Document(models.Model):
    name = models.CharField(max_length=100)
    document_image = models.ImageField(upload_to='documents/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
