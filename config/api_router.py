from ninja import NinjaAPI
from pessoa.api import router as pessoa
from cliente.api import router as cliente
from proprietario.api import router as proprietario
from raca.api import router as raca
from categoria_animal.api import router as categoria_animal
from logradouro.api import router as logradouro
from bairro.api import router as bairro
from cidade.api import router as cidade
from estado.api import router as estado
from endereco.api import router as endereco
from animal.api import router as animal
from adocao.api import router as adocao
from authentication.api import router as auth
from ninja.security import HttpBearer
from pessoa.api import Pessoa


class GlobalAuth(HttpBearer):
    def authenticate(self, request, token):
        try:
            Pessoa.objects.get(token=token)
            return token
        except:
            return False

api = NinjaAPI()

api.add_router('auth', auth)
api.add_router('pessoas', pessoa)
api.add_router('clientes', cliente, auth=GlobalAuth())
api.add_router('proprietarios', proprietario, auth=GlobalAuth())
api.add_router('racas', raca, auth=GlobalAuth())
api.add_router('categorias_animais', categoria_animal, auth=GlobalAuth())
api.add_router('logradouros', logradouro, auth=GlobalAuth())
api.add_router('bairros', bairro, auth=GlobalAuth())
api.add_router('cidades', cidade, auth=GlobalAuth())
api.add_router('estados', estado, auth=GlobalAuth())
api.add_router('enderecos', endereco, auth=GlobalAuth())
api.add_router('animais', animal, auth=GlobalAuth())
api.add_router('adocoes', adocao, auth=GlobalAuth())


