from django.db import models

class UploadedFile(models.Model):
    file_name = models.CharField(max_length=255)

    def __str__(self):
        return self.file_name
    