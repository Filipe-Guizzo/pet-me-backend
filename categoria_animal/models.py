from django.db import models

class CategoriaAnimal(models.Model):
    id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'categoria_animal'
