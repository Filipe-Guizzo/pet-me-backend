from ninja import Router, Schema
from ninja.orm import create_schema
from ninja.pagination import paginate, PageNumberPagination
from typing import List
from .models import Logradouro

LogradouroSchema = create_schema(Logradouro)    
LogradouroSchemaIn = create_schema(Logradouro, exclude=['id'])

class MessageSchema(Schema):
    message: str
    status: int

router = Router()

@router.get('/', response=List[LogradouroSchema])
@paginate(PageNumberPagination, page_size=20)
def get_all(request):
    logradouros = Logradouro.objects.all()
    return logradouros

@router.get('/{id}/', response={200:LogradouroSchema, 404:MessageSchema})
def get_by_id(request, id:int):
    try:
        logradouro = Logradouro.objects.get(id=id)
        return 200,logradouro
    except:
        return 404, {
            'message':'Não encontrado',
            'status':404
        }

@router.post('/', response={200:LogradouroSchema, 400:MessageSchema})
def create(request, payload: LogradouroSchemaIn):
    try:
        json_data = payload.dict()
        
        logradouro = Logradouro.objects.create(**json_data)
        return 200, logradouro
        
    except:
        return 400, {
            'message':'Erro ao criar',
            'status':400
        }

@router.put('/{id}/', response={200:LogradouroSchema, 400:MessageSchema})
def update(request, id:int, payload:LogradouroSchemaIn):
    try:
        json_data = payload.dict()
        
        Logradouro.objects.filter(id=id).update(**json_data)
        logradouro = Logradouro.objects.get(id=id)
        return 200, logradouro
        
    except:
        return 400, {
            'message':'Erro ao atualizar',
            'status':400
        }

@router.delete('/{id}/', response={200:MessageSchema, 400:MessageSchema})
def delete(request, id:int):
    try:
        logradouro = Logradouro.objects.get(id=id)
        logradouro.delete()
        return 200, {
            'message':'Deletado com sucesso',
            'status':200
        }
        
    except:
        return 400, {
            'message':'Erro ao deletar',
            'status':400
        }