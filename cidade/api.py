from ninja import Router, Schema
from ninja.orm import create_schema
from ninja.pagination import paginate, PageNumberPagination
from typing import List
from .models import Cidade

CidadeSchema = create_schema(Cidade)    
CidadeSchemaIn = create_schema(Cidade, exclude=['id'])

class MessageSchema(Schema):
    message: str
    status: int

router = Router()

@router.get('/', response=List[CidadeSchema])
@paginate(PageNumberPagination, page_size=20)
def get_all(request):
    cidades = Cidade.objects.all()
    return cidades

@router.get('/{id}/', response={200:CidadeSchema, 404:MessageSchema})
def get_by_id(request, id:int):
    try:
        cidade = Cidade.objects.get(id=id)
        return 200,cidade
    except:
        return 404, {
            'message':'Não encontrado',
            'status':404
        }

@router.post('/', response={200:CidadeSchema, 400:MessageSchema})
def create(request, payload: CidadeSchemaIn):
    try:
        json_data = payload.dict()
        
        cidade = Cidade.objects.create(**json_data)
        return 200, cidade
        
    except:
        return 400, {
            'message':'Erro ao criar',
            'status':400
        }

@router.put('/{id}/', response={200:CidadeSchema, 400:MessageSchema})
def update(request, id:int, payload:CidadeSchemaIn):
    try:
        json_data = payload.dict()
        
        Cidade.objects.filter(id=id).update(**json_data)
        cidade = Cidade.objects.get(id=id)
        return 200, cidade
        
    except:
        return 400, {
            'message':'Erro ao atualizar',
            'status':400
        }

@router.delete('/{id}/', response={200:MessageSchema, 400:MessageSchema})
def delete(request, id:int):
    try:
        cidade = Cidade.objects.get(id=id)
        cidade.delete()
        return 200, {
            'message':'Deletado com sucesso',
            'status':200
        }
        
    except:
        return 400, {
            'message':'Erro ao deletar',
            'status':400
        }