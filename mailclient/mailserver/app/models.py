from django.db import models

# Create your models here.
    
class Mail_detail(models.Model):
    sender = models.CharField(max_length=122)
    receiver = models.CharField(max_length=122)
    body = models.CharField(max_length=1024)
    subject = models.CharField(max_length=122)
    is_draft = models.BooleanField()
    in_inbox = models.BooleanField()
    in_outbox = models.BooleanField()
    file = models.FileField(blank=True)
    date = models.DateField()

    def __str__(self):
        desc = self.sender + ' - ' + self.receiver
        return desc
    