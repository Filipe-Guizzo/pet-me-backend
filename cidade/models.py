from django.db import models


class Cidade(models.Model):
    id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'cidade'
