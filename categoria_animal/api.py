from ninja import Router, Schema
from ninja.orm import create_schema
from ninja.pagination import paginate, PageNumberPagination
from typing import List
from .models import CategoriaAnimal

CategoriaAnimalSchema = create_schema(CategoriaAnimal)    
CategoriaAnimalSchemaIn = create_schema(CategoriaAnimal, exclude=['id'])

class MessageSchema(Schema):
    message: str
    status: int

router = Router()

@router.get('/', response=List[CategoriaAnimalSchema])
@paginate(PageNumberPagination, page_size=20)
def get_all(request):
    categorias_animais = CategoriaAnimal.objects.all()
    return categorias_animais

@router.get('/{id}/', response={200:CategoriaAnimalSchema, 404:MessageSchema})
def get_by_id(request, id:int):
    try:
        categoria_animal = CategoriaAnimal.objects.get(id=id)
        return 200,categoria_animal
    except:
        return 404, {
            'message':'Não encontrado',
            'status':404
        }

@router.post('/', response={200:CategoriaAnimalSchema, 400:MessageSchema})
def create(request, payload: CategoriaAnimalSchemaIn):
    try:
        json_data = payload.dict()
        
        categoria_animal = CategoriaAnimal.objects.create(**json_data)
        return 200, categoria_animal
        
    except:
        return 400, {
            'message':'Erro ao criar',
            'status':400
        }

@router.put('/{id}/', response={200:CategoriaAnimalSchema, 400:MessageSchema})
def update(request, id:int, payload:CategoriaAnimalSchemaIn):
    try:
        json_data = payload.dict()
        
        CategoriaAnimal.objects.filter(id=id).update(**json_data)
        categoria_animal= CategoriaAnimal.objects.get(id=id)
        return 200, categoria_animal
        
    except:
        return 400, {
            'message':'Erro ao atualizar',
            'status':400
        }

@router.delete('/{id}/', response={200:MessageSchema, 400:MessageSchema})
def delete(request, id:int):
    try:
        categoria_animal = CategoriaAnimal.objects.get(id=id)
        categoria_animal.delete()
        return 200, {
            'message':'Deletado com sucesso',
            'status':200
        }
        
    except:
        return 400, {
            'message':'Erro ao deletar',
            'status':400
        }