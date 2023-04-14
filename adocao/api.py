from ninja import Router, Schema
from ninja.orm import create_schema
from ninja.pagination import paginate, PageNumberPagination
from typing import List
from .models import Adocao
from cliente.api import ClienteSchema, Cliente
from proprietario.api import ProprietarioSchema, Proprietario
from animal.api import AnimalSchema, Animal

class AdocaoSchema(Schema):
    id: int
    cliente: ClienteSchema
    proprietario: ProprietarioSchema 
    animal: AnimalSchema 

AdocaoSchemaIn = create_schema(Adocao, exclude=['id'])

class MessageSchema(Schema):
    message: str
    status: int

router = Router()

@router.get('/', response=List[AdocaoSchema])
@paginate(PageNumberPagination, page_size=20)
def get_all(request):
    adocoes = Adocao.objects.all()
    return adocoes

@router.get('/{id}/', response={200:AdocaoSchema, 404:MessageSchema})
def get_by_id(request, id:int):
    try:
        adocao = Adocao.objects.get(id=id)
        return 200,adocao
    except:
        return 404, {
            'message':'Não encontrado',
            'status':404
        }

@router.post('/', response={200:AdocaoSchema, 400:MessageSchema})
def create(request, payload: AdocaoSchemaIn):
    try:
        json_data = payload.dict()
        
        cliente = Cliente.objects.get(id=json_data['cliente'])
        json_data['cliente'] = cliente
        
        proprietario = Proprietario.objects.get(id=json_data['proprietario'])
        json_data['proprietario'] = proprietario
        
        animal = Animal.objects.get(id=json_data['animal'])
        json_data['animal'] = animal
        
        adocao = Adocao.objects.create(**json_data)
        return 200, adocao
        
    except:
        return 400, {
            'message':'Erro ao criar',
            'status':400
        }

@router.put('/{id}/', response={200:AdocaoSchema, 400:MessageSchema})
def update(request, id:int, payload:AdocaoSchemaIn):
    try:
        json_data = payload.dict()
        
        cliente = Cliente.objects.get(id=json_data['cliente'])
        json_data['cliente'] = cliente
        
        proprietario = Proprietario.objects.get(id=json_data['Proprietario'])
        json_data['proprietario'] = proprietario
        
        animal = Animal.objects.get(id=json_data['animal'])
        json_data['animal'] = animal
        
        Adocao.objects.filter(id=id).update(**json_data)
        adocao= Adocao.objects.get(id=id)
        return 200, adocao
        
    except:
        return 400, {
            'message':'Erro ao atualizar',
            'status':400
        }

@router.delete('/{id}/', response={200:MessageSchema, 400:MessageSchema})
def delete(request, id:int):
    try:
        adocao = Adocao.objects.get(id=id)
        adocao.delete()
        return 200, {
            'message':'Deletado com sucesso',
            'status':200
        }
        
    except:
        return 400, {
            'message':'Erro ao deletar',
            'status':400
        }