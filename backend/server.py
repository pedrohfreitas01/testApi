from flask import Flask
from flask_cors import CORS
from app.routes import registrar_rotas

def criar_app():
    app = Flask(__name__)
    CORS(app, resources={r"/*": {"origins": "*"}}) 
    registrar_rotas(app)
    return app

if __name__ == '__main__':
    app = criar_app()  
    app.run(debug=True)
