import pandas as pd
from flask import Blueprint, jsonify, request
import os

# organaizar as rotas 
rotas = Blueprint('rotas', __name__)


def load_data():
    caminho_csv = os.path.join(os.path.dirname(__file__), '../data/relatorio_cadop.csv')
    try:
        dados = pd.read_csv(caminho_csv, delimiter=';', encoding='utf-8', dtype=str)
        dados = dados.fillna('Não disponível')  # Substitui valores ausentes
        return dados
    except FileNotFoundError:
        return pd.DataFrame() # retorna um df vazio

dados = load_data()



@rotas.route('/search', methods=['GET'])
def buscar():
    termo = request.args.get('q', '').strip().lower()
    if not termo:
        return jsonify({'erro': 'Informe um termo para buscar'}), 400
    
    # Aqui filtramos os dados para ver se o termo buscado aparece em alguma coluna da tabela
    # Para isso, percorremos cada linha e verificamos se o termo está presente em pelo menos uma das colunas
    resultado = dados[dados.apply(lambda linha: linha.astype(str).str.lower().str.contains(termo).any(), axis=1)]
    return jsonify(resultado.to_dict(orient='records'))

def registrar_rotas(app):
    app.register_blueprint(rotas)