from django.db import models
from cliente.models import Cliente
from proprietario.models import Proprietario
from animal.models import Animal

class Adocao(models.Model):
    id = models.AutoField(primary_key=True)
    cliente = models.ForeignKey(Cliente, models.DO_NOTHING)
    proprietario = models.ForeignKey(Proprietario, models.DO_NOTHING)
    animal = models.ForeignKey(Animal, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'adocao'
