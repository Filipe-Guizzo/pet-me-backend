from django.db import models

class Pessoa(models.Model):
    PERMISSAO_CHOICES = (
        (1, 'Proprietario/Estabelicimento'),
        (2, 'Cliente'),
    )
    id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=50)
    data_nascimento = models.DateField()
    sexo = models.CharField(max_length=1)
    telefone = models.CharField(max_length=14)
    email = models.CharField(max_length=100)
    senha = models.CharField(max_length=150)
    token = models.CharField(max_length=500)
    permissao = models.IntegerField(choices=PERMISSAO_CHOICES)
    imagem = models.ImageField(upload_to="")

    class Meta:
        managed = False
        db_table = 'pessoa'
