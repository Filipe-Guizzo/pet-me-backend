from ninja import Router, Schema
from ninja.orm import create_schema
from ninja.pagination import paginate, PageNumberPagination
from typing import List
from .models import Estado

EstadoSchema = create_schema(Estado)    
EstadoSchemaIn = create_schema(Estado, exclude=['id'])

class MessageSchema(Schema):
    message: str
    status: int

router = Router()

@router.get('/', response=List[EstadoSchema])
@paginate(PageNumberPagination, page_size=20)
def get_all(request):
    estados = Estado.objects.all()
    return estados

@router.get('/{id}/', response={200:EstadoSchema, 404:MessageSchema})
def get_by_id(request, id:int):
    try:
        estado = Estado.objects.get(id=id)
        return 200,estado
    except:
        return 404, {
            'message':'Não encontrado',
            'status':404
        }

@router.post('/', response={200:EstadoSchema, 400:MessageSchema})
def create(request, payload: EstadoSchemaIn):
    try:
        json_data = payload.dict()
        
        estado = Estado.objects.create(**json_data)
        return 200, estado
        
    except:
        return 400, {
            'message':'Erro ao criar',
            'status':400
        }

@router.put('/{id}/', response={200:EstadoSchema, 400:MessageSchema})
def update(request, id:int, payload:EstadoSchemaIn):
    try:
        json_data = payload.dict()
        
        Estado.objects.filter(id=id).update(**json_data)
        estado = Estado.objects.get(id=id)
        return 200, estado
        
    except:
        return 400, {
            'message':'Erro ao atualizar',
            'status':400
        }

@router.delete('/{id}/', response={200:MessageSchema, 400:MessageSchema})
def delete(request, id:int):
    try:
        estado = Estado.objects.get(id=id)
        estado.delete()
        return 200, {
            'message':'Deletado com sucesso',
            'status':200
        }
        
    except:
        return 400, {
            'message':'Erro ao deletar',
            'status':400
        }