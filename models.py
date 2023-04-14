# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Adocao(models.Model):
    cliente = models.ForeignKey('Cliente', models.DO_NOTHING)
    proprietario = models.ForeignKey('Proprietario', models.DO_NOTHING)
    animal = models.ForeignKey('Animal', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'adocao'


class Animal(models.Model):
    nome = models.CharField(max_length=50)
    data_nascimento = models.DateField()
    status = models.CharField(max_length=50)
    imagem = models.CharField(max_length=150)
    categoria_animal = models.ForeignKey('CategoriaAnimal', models.DO_NOTHING)
    raca = models.ForeignKey('Raca', models.DO_NOTHING)
    endereco = models.ForeignKey('Endereco', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'animal'

class Bairro(models.Model):
    nome = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'bairro'


class CategoriaAnimal(models.Model):
    nome = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'categoria_animal'


class Cidade(models.Model):
    nome = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'cidade'


class Cliente(models.Model):
    cpf = models.CharField(max_length=14)
    pessoa = models.ForeignKey('Pessoa', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'cliente'

class Endereco(models.Model):
    complemento = models.CharField(max_length=150, blank=True, null=True)
    logradouro = models.ForeignKey('Logradouro', models.DO_NOTHING)
    bairro = models.ForeignKey(Bairro, models.DO_NOTHING)
    cidade = models.ForeignKey(Cidade, models.DO_NOTHING)
    estado = models.ForeignKey('Estado', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'endereco'


class Estado(models.Model):
    nome = models.CharField(max_length=50)
    uf = models.CharField(max_length=2)

    class Meta:
        managed = False
        db_table = 'estado'


class Logradouro(models.Model):
    nome = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'logradouro'


class Pessoa(models.Model):
    nome = models.CharField(max_length=50)
    data_nascimento = models.DateField()
    sexo = models.CharField(max_length=1)
    telefone = models.CharField(max_length=14)
    email = models.CharField(max_length=100)
    senha = models.CharField(max_length=150)
    token = models.CharField(max_length=500)
    permissao = models.IntegerField()
    imagem = models.CharField(max_length=150, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'pessoa'


class Proprietario(models.Model):
    cpf_cnpj = models.CharField(max_length=20)
    pessoa = models.ForeignKey(Pessoa, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'proprietario'


class Raca(models.Model):
    nome = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'raca'
