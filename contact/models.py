from django.db import models
from datetime import datetime
#from django.utils.translation import ugettext_lazy as _
# Create your models here.

class contactModel(models.Model):
    email = models.EmailField(("your email"), max_length=254,null=False)
    text = models.TextField(("How can we help you?"),max_length=1000,null=False)
    image = models.TextField(null=True)
    date =models.DateField(default=datetime.now)

    def __str__(self):
        return self.email