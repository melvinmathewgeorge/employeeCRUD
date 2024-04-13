
from django.db import models

class GenericModelMixin(models.Model):
    regid = models.CharField(primary_key=True,max_length=20, editable=False)


    class Meta:
        abstract = True
