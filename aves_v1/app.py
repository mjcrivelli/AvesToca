from flask import Flask, render_template, jsonify, send_from_directory
import sqlite3
import os

app = Flask(__name__)

# Função para pegar os dados das espécies do banco de dados
def get_especies():
    conn = sqlite3.connect('banco_de_dados.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM especies')
    especies = cursor.fetchall()
    conn.close()
    return especies

# Função para pegar os dados de uma espécie específica
def get_especie(id):
    conn = sqlite3.connect('banco_de_dados.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM especies WHERE id = ?', (id,))
    especie = cursor.fetchone()
    conn.close()
    return especie

# Página inicial com descrição da fazenda
@app.route('/')
def descricao_fazenda():
    return render_template('descricao_fazenda.html')

# Página com lista de espécies
@app.route('/especies')
def especies():
    especies = get_especies()
    return render_template('especies.html', especies=especies)

# Página com detalhes de uma espécie
@app.route('/especies/<int:id>')
def especie_detalhada(id):
    especie = get_especie(id)
    return render_template('especie_detalhada.html', especie=especie)

# Página de contato
@app.route('/contato')
def contato():
    return render_template('contato.html')

# API para pegar a lista de espécies
@app.route('/api/especies', methods=['GET'])
def api_especies():
    especies = get_especies()
    especies_json = []
    for especie in especies:
        especies_json.append({
            'id': especie[0],
            'nome': especie[1],
            'descricao': especie[2],
            'imagem': os.path.join('static', 'imagens', especie[3])  # Caminho da imagem
        })
    return jsonify(especies_json)

# API para pegar detalhes de uma espécie
@app.route('/api/especies/<int:id>', methods=['GET'])
def api_especie(id):
    especie = get_especie(id)
    if especie:
        especie_json = {
            'id': especie[0],
            'nome': especie[1],
            'descricao': especie[2],
            'imagem': os.path.join('static', 'imagens', especie[3])  # Caminho da imagem
        }
        return jsonify(especie_json)
    else:
        return jsonify({'error': 'Espécie não encontrada'}), 404

# Rota para acessar a imagem da ave
@app.route('/static/imagens/<filename>')
def send_image(filename):
    return send_from_directory(os.path.join(app.root_path, 'static', 'imagens'), filename)

if __name__ == '__main__':
    app.run(debug=True)
