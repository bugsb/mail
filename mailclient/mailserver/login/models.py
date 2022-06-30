from django.db import models

# Create your models here.
class Security(models.Model):
    qes = models.CharField(max_length=122)
    ans = models.CharField(max_length=122)
    user = models.EmailField()

    def __str__(self):
        return self.user
    