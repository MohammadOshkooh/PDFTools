from django.db import models


class PDF(models.Model):
    pdf = models.FileField(upload_to='pdf/')

    # def save(
    #     self, force_insert=False, force_update=False, using=None, update_fields=None
    # ):
    #     return super(PDF, self).save()