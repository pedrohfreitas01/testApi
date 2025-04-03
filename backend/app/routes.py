from flask import Blueprint, request, jsonify  
import pandas as pd  
import os  

# carrega os dados do CSV
def load_data():
    caminho_csv = os.path.join(os.path.dirname(__file__), '../data/relatorio_cadop.csv')

    if not os.path.exists(caminho_csv):  
        return pd.DataFrame(columns=['id', 'nome', 'estado'])  

    return pd.read_csv(caminho_csv, delimiter=';', encoding='utf-8', dtype=str)  

dados = load_data()  

rotas = Blueprint('rotas', __name__)  




# rota de busca
@rotas.route('/search', methods=['GET'])
def buscar():
    termo = request.args.get('q', '').strip().lower()  

    if not termo:
        return jsonify({'erro': 'Informe um termo para buscar'}), 400  
    
    # filtro q  verifica se a consulta ta presente em qualquer coluna do CSV
    resultado = dados[dados.apply(lambda linha: linha.astype(str).str.lower().str.contains(termo).any(), axis=1)]  

    return jsonify(resultado.to_dict(orient='records'))  




# funaoo para adicionar as rotas no app
def registrar_rotas(app):
    app.register_blueprint(rotas)  

print(dados.columns)  # mostra as colunas do CSV no terminal
