from django.db import models

class Estado(models.Model):
    id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=50)
    uf = models.CharField(max_length=2)

    class Meta:
        managed = False
        db_table = 'estado'