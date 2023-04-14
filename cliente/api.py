from ninja import Router, Schema
from ninja.orm import create_schema
from ninja.pagination import paginate, PageNumberPagination
from typing import List
from .models import Cliente
from pessoa.api import PessoaSchema, Pessoa

class ClienteSchema(Schema):
    id :int
    cpf: str
    pessoa: PessoaSchema
    
ClienteSchemaIn = create_schema(Cliente, exclude=['id'])

class MessageSchema(Schema):
    message: str
    status: int

router = Router()

@router.get('/', response=List[ClienteSchema])
@paginate(PageNumberPagination, page_size=20)
def get_all(request):
    clientes = Cliente.objects.all()
    return clientes

@router.get('/{id}/', response={200:ClienteSchema, 404:MessageSchema})
def get_by_id(request, id:int):
    try:
        cliente = Cliente.objects.get(id=id)
        return 200,cliente
    except:
        return 404, {
            'message':'Não encontrado',
            'status':404
        }

@router.post('/', response={200:ClienteSchema, 400:MessageSchema})
def create(request, payload: ClienteSchemaIn):
    try:
        json_data = payload.dict()
        
        pessoa = Pessoa.objects.get(id=json_data['pessoa'])
        json_data['pessoa'] = pessoa
        
        cliente = Cliente.objects.create(**json_data)
        return 200, cliente
        
        
    except:
        return 400, {
            'message':'Erro ao criar',
            'status':400
        }

@router.put('/{id}/', response={200:ClienteSchema, 400:MessageSchema})
def update(request, id:int, payload:ClienteSchemaIn):
    try:
        json_data = payload.dict()
        
        pessoa = Pessoa.objects.get(id=json_data['pessoa'])
        json_data['pessoa'] = pessoa
        
        Cliente.objects.filter(id=id).update(**json_data)
        cliente = Cliente.objects.get(id=id)
        return 200, cliente
        
        
    except:
        return 400, {
            'message':'Erro ao atualizar',
            'status':400
        }

@router.delete('/{id}/', response={200:MessageSchema, 400:MessageSchema})
def delete(request, id:int):
    try:
        cliente = Cliente.objects.get(id=id)
        cliente.delete()
        return 200, {
            'message':'Deletado com sucesso',
            'status':200
        }
        
        
    except:
        return 400, {
            'message':'Erro ao deletar',
            'status':400
        }