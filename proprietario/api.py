from ninja import Router, Schema
from ninja.orm import create_schema
from ninja.pagination import paginate, PageNumberPagination
from typing import List
from .models import Proprietario
from pessoa.api import PessoaSchema, Pessoa

class ProprietarioSchema(Schema):
    id :int
    cpf_cnpj: str
    pessoa: PessoaSchema
    
ProprietarioSchemaIn = create_schema(Proprietario, exclude=['id'])

class MessageSchema(Schema):
    message: str
    status: int

router = Router()

@router.get('/', response=List[ProprietarioSchema])
@paginate(PageNumberPagination, page_size=20)
def get_all(request):
    proprietarios = Proprietario.objects.all()
    return proprietarios

@router.get('/{id}/', response={200:ProprietarioSchema, 404:MessageSchema})
def get_by_id(request, id:int):
    try:
        proprietario = Proprietario.objects.get(id=id)
        return 200,proprietario
    except:
        return 404, {
            'message':'Não encontrado',
            'status':404
        }

@router.post('/', response={200:ProprietarioSchema, 400:MessageSchema})
def create(request, payload: ProprietarioSchemaIn):
    try:
        json_data = payload.dict()
        
        pessoa = Pessoa.objects.get(id=json_data['pessoa'])
        json_data['pessoa'] = pessoa
        
        proprietario = Proprietario.objects.create(**json_data)
        return 200, proprietario
        
        
    except:
        return 400, {
            'message':'Erro ao criar',
            'status':400
        }

@router.put('/{id}/', response={200:ProprietarioSchema, 400:MessageSchema})
def update(request, id:int, payload:ProprietarioSchemaIn):
    try:
        json_data = payload.dict()
        
        pessoa = Pessoa.objects.get(id=json_data['pessoa'])
        json_data['pessoa'] = pessoa
        
        Proprietario.objects.filter(id=id).update(**json_data)
        proprietario = Proprietario.objects.get(id=id)
        return 200, proprietario
        
        
    except:
        return 400, {
            'message':'Erro ao atualizar',
            'status':400
        }

@router.delete('/{id}/', response={200:MessageSchema, 400:MessageSchema})
def delete(request, id:int):
    try:
        proprietario = Proprietario.objects.get(id=id)
        proprietario.delete()
        return 200, {
            'message':'Deletado com sucesso',
            'status':200
        }
        
        
    except:
        return 400, {
            'message':'Erro ao deletar',
            'status':400
        }