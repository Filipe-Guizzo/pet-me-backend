from ninja import Router, Schema, File
from ninja.orm import create_schema
from ninja.pagination import paginate, PageNumberPagination
from typing import List
from ninja.files import UploadedFile
from .models import Pessoa
import bcrypt
import jwt
from ninja.security import HttpBearer


class GlobalAuth(HttpBearer):
    def authenticate(self, request, token):
        try:
            Pessoa.objects.get(token=token)
            return token
        except:
            return False

PessoaSchema = create_schema(Pessoa)
PessoaSchemaIn = create_schema(Pessoa, exclude=['id','token'])

class MessageSchema(Schema):
    message: str
    status: int

router = Router()

@router.get('/', response=List[PessoaSchema] , auth=GlobalAuth())
@paginate(PageNumberPagination, page_size=20)
def get_all(request):
    pessoas = Pessoa.objects.all()
    return pessoas

@router.get('/{id}/', response={200:PessoaSchema, 404:MessageSchema}, auth=GlobalAuth())
def get_by_id(request, id:int):
    try:
        pessoa = Pessoa.objects.get(id=id)
        return 200,pessoa
    except:
        return 404, {
            'message':'Não encontrado',
            'status':404
        }

@router.post('/', response={200:PessoaSchema, 400:MessageSchema})
def create(request, payload: PessoaSchemaIn):
    try:
        json_data = payload.dict()
        
        #criptografia da senha
        senha = json_data['senha']
        senha_hashed = bcrypt.hashpw(senha.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        json_data['senha'] = senha_hashed
        
        #token JWT
        nome = json_data['nome']
        token = jwt.encode({'nome': nome}, senha_hashed, algorithm="HS256")
        json_data['token'] = token
        
        pessoa = Pessoa.objects.create(**json_data)
        return 200, pessoa
        
        
    except:
        return 400, {
            'message':'Erro ao criar',
            'status':400
        }

@router.put('/{id}/', response={200:PessoaSchema, 400:MessageSchema}, auth=GlobalAuth())
def update(request, id:int, payload:PessoaSchemaIn):
    try:
        json_data = payload.dict()
        
        #criptografia da senha
        senha = json_data['senha']
        senha_hashed = bcrypt.hashpw(senha.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        json_data['senha'] = senha_hashed
        
        #token JWT
        nome = json_data['nome']
        token = jwt.encode({'nome': nome}, senha_hashed, algorithm="HS256")
        json_data['token'] = token
        
        Pessoa.objects.filter(id=id).update(**json_data)
        pessoa = Pessoa.objects.get(id=id)
        return 200, pessoa
        
        
    except:
        return 400, {
            'message':'Erro ao atualizar',
            'status':400
        }

@router.delete('/{id}/', response={200:MessageSchema, 400:MessageSchema}, auth=GlobalAuth())
def delete(request, id:int):
    try:
        pessoa = Pessoa.objects.get(id=id)
        pessoa.delete()
        return 200, {
            'message':'Deletado com sucesso',
            'status':200
        }
        
        
    except:
        return 400, {
            'message':'Erro ao deletar',
            'status':400
        }

@router.post('/{id}/upload-file/', response={200:PessoaSchema, 400:MessageSchema}, auth=GlobalAuth())
def upload_file(request, id:int, file: UploadedFile = File(...)):
    try:
        pessoa = Pessoa.objects.get(id=id)
        pessoa.imagem = file
        pessoa.save()
        return 200, pessoa
        
        
    except:
        return 400, {
            'message':'Erro ao savar imagem',
            'status':400
        }