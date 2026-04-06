from flask import Flask

# Inicializa o aplicativo Flask
app = Flask(__name__)

# Importa as rotas 
from app.controllers import routes