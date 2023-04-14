from ninja import Router, Schema
from pessoa.api import Pessoa
import bcrypt
from twilio.rest import Client
import random
import jwt
import os


class LoginSchema(Schema):
    token: str
    pessoa_id: int
    permissao: int
    message: str
    status: int

class LoginSchemaIn(Schema):
    email: str
    senha: str

class EnviarSms(Schema):
    pessoa_id: int
    codigo: int 

class EnviarSmsIn(Schema):
    email: str

class ReenviarSms(Schema):
    pessoa_id: int
    codigo: int 

class RecuperarSenhaSchemaIn(Schema):
    senha: str

class MessageSchema(Schema):
    message: str
    status: int


router = Router()

@router.post('/login/', response={200:LoginSchema, 401:MessageSchema})
def login(request, payload: LoginSchemaIn):
    json_data = payload.dict()
    
    email = json_data['email']
    senha = json_data['senha']
    
    try:
        pessoa = Pessoa.objects.get(email=email)
        if bcrypt.checkpw(senha.encode('ASCII'), pessoa.senha.encode('ASCII')):
            return 200, {
                'token': pessoa.token,
                'pessoa_id': pessoa.id,
                'permissao': pessoa.permissao,
                'message':'Logado com sucesso',
                'status': 200
            }
    except:
        return 401, {
            'message':'E-mail ou senha incorretos',
            'status': 401
        }

@router.post('/enviar-sms/', response={200:EnviarSms, 401:MessageSchema, 404:MessageSchema})
def send_sms(request, payload: EnviarSmsIn):
    json_data = payload.dict()
    
    email = json_data['email']
    
    try:
        pessoa = Pessoa.objects.get(email=email)
        numero = ''.join(e for e in pessoa.telefone if e.isalnum())
        codigo = random.randint(1000, 9999)
    except:
        return 404, {
            'message':'E-mail não encontrado',
            'status': 404
        }
    
    try:
        account_sid = os.environ['twilio-account-sid']
        auth_token  = os.environ['twilio-auth-token']

        client = Client(account_sid, auth_token)

        client.messages.create(
            to=f"+55{numero}", 
            from_="+19035467693",
            body=f"Codigo de recuperação de senha: {codigo}")
        return 200, {
            'pessoa_id': pessoa.id,
            'codigo':codigo
        }
    except:
        return 400, {
            'message':'Erro ao enviar SMS',
            'status': 400
        }

@router.post('/reenviar-sms/', response={200:ReenviarSms, 401:MessageSchema, 404:MessageSchema})
def resend_sms(request, payload: ReenviarSms):
    json_data = payload.dict()
    
    pessoa_id = json_data['pessoa_id']
    codigo = json_data['codigo']
    
    try:
        pessoa = Pessoa.objects.get(id=pessoa_id)
        numero = ''.join(e for e in pessoa.telefone if e.isalnum())
    except:
        return 404, {
            'message':'E-mail não encontrado',
            'status': 404
        }
    
    try:
        account_sid = os.environ['twilio-account-sid']
        auth_token  = os.environ['twilio-auth-token']

        client = Client(account_sid, auth_token)

        client.messages.create(
            to=f"+55{numero}", 
            from_="+19035467693",
            body=f"Codigo de recuperação de senha: {codigo}")
        return 200, {
            'pessoa_id': pessoa.id,
            'codigo':codigo
        }
    except:
        return 400, {
            'message':'Erro ao enviar SMS',
            'status': 400
        }

@router.post('/{id}/recuperar-senha/', response={200:MessageSchema, 400:MessageSchema})
def recover_password(request, id:int, payload: RecuperarSenhaSchemaIn):
    json_data = payload.dict()
    
    try:
        pessoa = Pessoa.objects.get(id=id)
        
        #criptografia da senha
        senha = json_data['senha']
        senha_hashed = bcrypt.hashpw(senha.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        
        #token JWT
        token = jwt.encode({'nome': pessoa.nome}, senha_hashed, algorithm="HS256")
        
        pessoa.senha = senha_hashed
        pessoa.token = token
        pessoa.save()
        
        return 200, {
            'message':'Senha alterada com sucesso',
            'status': 200
        }
    except:
        return 400, {
            'message':'Erro ao recuperar senha',
            'status': 400
        }