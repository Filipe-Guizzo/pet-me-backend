from django.db import models
from categoria_animal.models import CategoriaAnimal
from raca.models import Raca
from endereco.models import Endereco

class Animal(models.Model):
    id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=50)
    data_nascimento = models.DateField()
    status = models.CharField(max_length=50)
    imagem = models.ImageField(upload_to="")
    categoria_animal = models.ForeignKey(CategoriaAnimal, models.DO_NOTHING)
    raca = models.ForeignKey(Raca, models.DO_NOTHING)
    endereco = models.ForeignKey(Endereco, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'animal'
