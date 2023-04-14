from ninja import Router, Schema
from ninja.orm import create_schema
from ninja.pagination import paginate, PageNumberPagination
from typing import List
from .models import Bairro

BairroSchema = create_schema(Bairro)    
BairroSchemaIn = create_schema(Bairro, exclude=['id'])

class MessageSchema(Schema):
    message: str
    status: int

router = Router()

@router.get('/', response=List[BairroSchema])
@paginate(PageNumberPagination, page_size=20)
def get_all(request):
    bairros = Bairro.objects.all()
    return bairros

@router.get('/{id}/', response={200:BairroSchema, 404:MessageSchema})
def get_by_id(request, id:int):
    try:
        bairro = Bairro.objects.get(id=id)
        return 200,bairro
    except:
        return 404, {
            'message':'Não encontrado',
            'status':404
        }

@router.post('/', response={200:BairroSchema, 400:MessageSchema})
def create(request, payload: BairroSchemaIn):
    try:
        json_data = payload.dict()
        
        bairro = Bairro.objects.create(**json_data)
        return 200, bairro
        
    except:
        return 400, {
            'message':'Erro ao criar',
            'status':400
        }

@router.put('/{id}/', response={200:BairroSchema, 400:MessageSchema})
def update(request, id:int, payload:BairroSchemaIn):
    try:
        json_data = payload.dict()
        
        Bairro.objects.filter(id=id).update(**json_data)
        bairro = Bairro.objects.get(id=id)
        return 200, bairro
        
    except:
        return 400, {
            'message':'Erro ao atualizar',
            'status':400
        }

@router.delete('/{id}/', response={200:MessageSchema, 400:MessageSchema})
def delete(request, id:int):
    try:
        bairro = Bairro.objects.get(id=id)
        bairro.delete()
        return 200, {
            'message':'Deletado com sucesso',
            'status':200
        }
        
    except:
        return 400, {
            'message':'Erro ao deletar',
            'status':400
        }