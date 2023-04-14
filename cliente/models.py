from django.db import models
from pessoa.models import Pessoa

class Cliente(models.Model):
    id = models.AutoField(primary_key=True)
    cpf = models.CharField(max_length=14)
    pessoa = models.ForeignKey(Pessoa, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'cliente'
