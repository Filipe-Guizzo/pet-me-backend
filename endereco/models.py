from django.db import models
from logradouro.models import Logradouro
from bairro.models import Bairro
from cidade.models import Cidade
from estado.models import Estado

class Endereco(models.Model):
    id = models.AutoField(primary_key=True)
    complemento = models.CharField(max_length=150, blank=True, null=True)
    logradouro = models.ForeignKey(Logradouro, models.DO_NOTHING)
    bairro = models.ForeignKey(Bairro, models.DO_NOTHING)
    cidade = models.ForeignKey(Cidade, models.DO_NOTHING)
    estado = models.ForeignKey(Estado, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'endereco'
