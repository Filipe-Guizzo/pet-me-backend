from ninja import Router, Schema
from ninja.orm import create_schema
from ninja.pagination import paginate, PageNumberPagination
from typing import List
from .models import Raca

RacaSchema = create_schema(Raca)    
RacaSchemaIn = create_schema(Raca, exclude=['id'])

class MessageSchema(Schema):
    message: str
    status: int

router = Router()

@router.get('/', response=List[RacaSchema])
@paginate(PageNumberPagination, page_size=20)
def get_all(request):
    racas = Raca.objects.all()
    return racas

@router.get('/{id}/', response={200:RacaSchema, 404:MessageSchema})
def get_by_id(request, id:int):
    try:
        raca = Raca.objects.get(id=id)
        return 200,raca
    except:
        return 404, {
            'message':'Não encontrado',
            'status':404
        }

@router.post('/', response={200:RacaSchema, 400:MessageSchema})
def create(request, payload: RacaSchemaIn):
    try:
        json_data = payload.dict()
        
        raca = Raca.objects.create(**json_data)
        return 200, raca
        
    except:
        return 400, {
            'message':'Erro ao criar',
            'status':400
        }

@router.put('/{id}/', response={200:RacaSchema, 400:MessageSchema})
def update(request, id:int, payload:RacaSchemaIn):
    try:
        json_data = payload.dict()
        
        Raca.objects.filter(id=id).update(**json_data)
        raca = Raca.objects.get(id=id)
        return 200, raca
        
    except:
        return 400, {
            'message':'Erro ao atualizar',
            'status':400
        }

@router.delete('/{id}/', response={200:MessageSchema, 400:MessageSchema})
def delete(request, id:int):
    try:
        raca = Raca.objects.get(id=id)
        raca.delete()
        return 200, {
            'message':'Deletado com sucesso',
            'status':200
        }
        
    except:
        return 400, {
            'message':'Erro ao deletar',
            'status':400
        }