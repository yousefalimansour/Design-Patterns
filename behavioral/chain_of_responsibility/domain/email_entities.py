from django.db import models

class Email(models.Model):
    sender = models.CharField(max_length=255)
    subject = models.CharField(max_length=255)
    body = models.TextField()
    is_spam = models.BooleanField(default=False)

    def __str__(self):
        return self.subject
