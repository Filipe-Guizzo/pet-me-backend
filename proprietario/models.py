from django.db import models
from pessoa.models import Pessoa

class Proprietario(models.Model):
    id = models.AutoField(primary_key=True)
    cpf_cnpj = models.CharField(max_length=20)
    pessoa = models.ForeignKey(Pessoa, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'proprietario'
