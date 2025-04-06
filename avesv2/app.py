from flask import Flask, render_template, request, url_for, flash, redirect
import os
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
from werkzeug.exceptions import abort



# Definir o caminho do banco de dados
project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = 'sqlite:///{}'.format(os.path.join(project_dir, "database.db"))

# Inicializar a aplicação Flask
app = Flask(__name__)

# Configurações da aplicação
app.config['SECRET_KEY'] = 'your secret key'
app.config['SQLALCHEMY_DATABASE_URI'] = database_file
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = os.path.join('static', 'uploads')
app.config['ALLOWED_EXTENSIONS'] = {'jpg', 'jpeg', 'png', 'gif'}

# Inicializar o banco de dados com SQLAlchemy
db = SQLAlchemy(app)

# Definição do modelo Aves
class Aves(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(99), nullable=False)
    nome_cientifico = db.Column(db.String(99), nullable=False)
    descricao = db.Column(db.String(500), nullable=False)
    dimorfismo = db.Column(db.String(99), nullable=False)
    ocorrencia = db.Column(db.String(99), nullable=False)
    conservacao = db.Column(db.String(99), nullable=False)
    imagem = db.Column(db.String(200), nullable=True)  # Coluna para armazenar imagem

# Função para verificar se a imagem é válida
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

# Verifica se o arquivo tem uma extensão permitida para upload.
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

# Função para salvar o arquivo de imagem
def save_image(image):
    if image and allowed_file(image.filename):
        # Garante que o diretório de upload existe
        if not os.path.exists(app.config['UPLOAD_FOLDER']):
            os.makedirs(app.config['UPLOAD_FOLDER'])

        # Cria um nome seguro para o arquivo
        filename = secure_filename(image.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)

        try:
            # Salva a imagem
            image.save(filepath)
            print(f"Imagem salva com sucesso em: {filepath}")
            return filepath  # Retorna o caminho do arquivo salvo
        except Exception as e:
            print(f"Erro ao salvar a imagem: {e}")
            return None
    else:
        print("Arquivo não permitido ou não enviado!")
        return None



@app.route('/')

# Exibe todas as aves registradas no banco de dados.
def index():
    aves = Aves.query.all()  # Obter todas as aves do banco de dados
    return render_template('index.html', aves=aves)  # Passar 'aves' para o template

# Obtém uma ave a partir do ID. Se a ave não for encontrada, lança um erro 404.
def get_ave(ave_id):
    ave = Aves.query.filter_by(id=ave_id).first()
    if ave is None:
        abort(404)
    return ave

# Exibe detalhes de uma ave específica.
@app.route('/<int:ave_id>')
def ave(ave_id):
    ave = get_ave(ave_id)
    return render_template('aves.html', ave=ave)

@app.route('/create', methods=['GET', 'POST'])
# Criar uma nova ave no banco de dados. O formulário envia os dados via POST, e a imagem é salva se fornecida.
def create():
    if request.method == 'POST':
        nome = request.form['nome']
        nome_cientifico = request.form['nome_cientifico']
        descricao = request.form['descricao']
        dimorfismo = request.form['dimorfismo']
        ocorrencia = request.form['ocorrencia']
        conservacao = request.form['conservacao']
        imagem = request.files['imagem']

        # Salvar a imagem e obter o caminho do arquivo salvo
        imagem_path = save_image(imagem)

        if not nome or not nome_cientifico:
            flash('Nome e nome científico são obrigatórios')
        else:
            ave = Aves(nome=nome, nome_cientifico=nome_cientifico, descricao=descricao, dimorfismo = dimorfismo, ocorrencia = ocorrencia, conservacao = conservacao, imagem=imagem_path)
            db.session.add(ave)
            db.session.commit()
            return redirect(url_for('index'))

    return render_template('create.html')



# Função para recriar as tabelas (deleta e recria as tabelas)
@app.before_request
def create_tables():
    db.create_all()  # Cria todas as tabelas definidas nos modelos, incluindo a nova coluna de imagem



if __name__ == '__main__':
    app.run(debug=True)

