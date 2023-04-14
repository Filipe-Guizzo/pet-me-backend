from ninja import Router, Schema
from ninja.orm import create_schema
from ninja.pagination import paginate, PageNumberPagination
from typing import List
from .models import Endereco
from logradouro.api import LogradouroSchema, Logradouro
from bairro.api import BairroSchema, Bairro
from cidade.api import CidadeSchema, Cidade
from estado.api import EstadoSchema, Estado

class EnderecoSchema(Schema):
    id: int
    complemento: str
    logradouro: LogradouroSchema 
    bairro: BairroSchema
    cidade: CidadeSchema 
    estado: EstadoSchema 
    
EnderecoSchemaIn = create_schema(Endereco, exclude=['id'])

class MessageSchema(Schema):
    message: str
    status: int

router = Router()

@router.get('/', response=List[EnderecoSchema])
@paginate(PageNumberPagination, page_size=20)
def get_all(request):
    enderecos = Endereco.objects.all()
    return enderecos

@router.get('/{id}/', response={200:EnderecoSchema, 404:MessageSchema})
def get_by_id(request, id:int):
    try:
        endereco = Endereco.objects.get(id=id)
        return 200,endereco
    except:
        return 404, {
            'message':'Não encontrado',
            'status':404
        }

@router.post('/', response={200:EnderecoSchema, 400:MessageSchema})
def create(request, payload: EnderecoSchemaIn):
    try:
        json_data = payload.dict()
        
        logradouro = Logradouro.objects.get(id=json_data['logradouro'])
        json_data['logradouro'] = logradouro
        
        bairro = Bairro.objects.get(id=json_data['bairro'])
        json_data['bairro'] = bairro
        
        cidade = Cidade.objects.get(id=json_data['cidade'])
        json_data['cidade'] = cidade
        
        estado = Estado.objects.get(id=json_data['estado'])
        json_data['estado'] = estado
        
        endereco = Endereco.objects.create(**json_data)
        return 200, endereco
        
        
    except:
        return 400, {
            'message':'Erro ao criar',
            'status':400
        }

@router.put('/{id}/', response={200:EnderecoSchema, 400:MessageSchema})
def update(request, id:int, payload:EnderecoSchemaIn):
    try:
        json_data = payload.dict()
        
        logradouro = Logradouro.objects.get(id=json_data['logradouro'])
        json_data['logradouro'] = logradouro
        
        bairro = Bairro.objects.get(id=json_data['bairro'])
        json_data['bairro'] = bairro
        
        cidade = Cidade.objects.get(id=json_data['cidade'])
        json_data['Cidade'] = cidade
        
        estado = Estado.objects.get(id=json_data['estado'])
        json_data['estado'] = estado
        
        Endereco.objects.filter(id=id).update(**json_data)
        endereco = Endereco.objects.get(id=id)
        return 200, endereco
        
        
    except:
        return 400, {
            'message':'Erro ao atualizar',
            'status':400
        }

@router.delete('/{id}/', response={200:MessageSchema, 400:MessageSchema})
def delete(request, id:int):
    try:
        endereco = Endereco.objects.get(id=id)
        endereco.delete()
        return 200, {
            'message':'Deletado com sucesso',
            'status':200
        }
        
        
    except:
        return 400, {
            'message':'Erro ao deletar',
            'status':400
        }