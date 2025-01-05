from django.db import models

class Folder(models.Model):
    id = models.CharField(max_length=255, primary_key=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
class Document(models.Model):
    id = models.AutoField(primary_key=True)
    parent = models.ForeignKey(Folder, on_delete=models.CASCADE, related_name='documents')
    name = models.CharField(max_length=255)
    file = models.FileField(upload_to='documents/')

    def __str__(self):
        return self.name