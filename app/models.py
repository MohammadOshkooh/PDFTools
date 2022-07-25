from django.db import models


class PDF(models.Model):
    pdf = models.FileField(upload_to='pdf/')

    def __str__(self):
        return self.pdf.name
