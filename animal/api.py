from ninja import Router, Schema, File
from ninja.orm import create_schema
from ninja.pagination import paginate, PageNumberPagination
from typing import List
from .models import Animal
from categoria_animal.api import CategoriaAnimalSchema, CategoriaAnimal
from raca.api import RacaSchema, Raca
from endereco.api import EnderecoSchema, Endereco
from datetime import date
from ninja.files import UploadedFile

class AnimalSchema(Schema):
    id: int
    nome: str 
    data_nascimento: date
    status: str 
    imagem: str 
    categoria_animal: CategoriaAnimalSchema
    raca: RacaSchema
    endereco: EnderecoSchema 
    
AnimalSchemaIn = create_schema(Animal, exclude=['id'])

class MessageSchema(Schema):
    message: str
    status: int

router = Router()

@router.get('/', response=List[AnimalSchema])
@paginate(PageNumberPagination, page_size=20)
def get_all(request):
    animais = Animal.objects.all()
    return animais

@router.get('/{id}/', response={200:AnimalSchema, 404:MessageSchema})
def get_by_id(request, id:int):
    try:
        animal = Animal.objects.get(id=id)
        return 200,animal
    except:
        return 404, {
            'message':'Não encontrado',
            'status':404
        }

@router.post('/', response={200:AnimalSchema, 400:MessageSchema})
def create(request, payload: AnimalSchemaIn):
    try:
        json_data = payload.dict()
        
        categoria_animal = CategoriaAnimal.objects.get(id=json_data['categoria_animal'])
        json_data['categoria_animal'] = categoria_animal
        
        raca = Raca.objects.get(id=json_data['raca'])
        json_data['raca'] = raca
        
        endereco = Endereco.objects.get(id=json_data['endereco'])
        json_data['endereco'] = endereco
        
        animal = Animal.objects.create(**json_data)
        return 200, animal
        
        
    except:
        return 400, {
            'message':'Erro ao criar',
            'status':400
        }

@router.put('/{id}/', response={200:AnimalSchema, 400:MessageSchema})
def update(request, id:int, payload:AnimalSchemaIn):
    try:
        json_data = payload.dict()
        
        categoria_animal = CategoriaAnimal.objects.get(id=json_data['categoria_animal'])
        json_data['categoria_animal'] = categoria_animal
        
        raca = Raca.objects.get(id=json_data['raca'])
        json_data['raca'] = raca
        
        endereco = Endereco.objects.get(id=json_data['endereco'])
        json_data['endereco'] = endereco
        
        Animal.objects.filter(id=id).update(**json_data)
        animal = Animal.objects.get(id=id)
        return 200, animal
        
        
    except:
        return 400, {
            'message':'Erro ao atualizar',
            'status':400
        }

@router.delete('/{id}/', response={200:MessageSchema, 400:MessageSchema})
def delete(request, id:int):
    try:
        animal = Animal.objects.get(id=id)
        animal.delete()
        return 200, {
            'message':'Deletado com sucesso',
            'status':200
        }
        
        
    except:
        return 400, {
            'message':'Erro ao deletar',
            'status':400
        }

@router.post('/{id}/upload-file/', response={200:AnimalSchema, 400:MessageSchema})
def upload_file(request, id:int, file: UploadedFile = File(...)):
    try:
        animal = Animal.objects.get(id=id)
        animal.imagem = file
        animal.save()
        return 200, animal
        
        
    except:
        return 400, {
            'message':'Erro ao savar imagem',
            'status':400
        }