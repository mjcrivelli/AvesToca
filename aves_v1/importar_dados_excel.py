import sqlite3
import pandas as pd

# Caminho para o arquivo Excel
caminho_arquivo_excel = 'aves_Toca_v2.xlsx'

# Carregar a planilha com pandas
df = pd.read_excel(caminho_arquivo_excel)

# Conectar ao banco de dados SQLite (cria se não existir)
conn = sqlite3.connect('banco_de_dados.db')
cursor = conn.cursor()

# Apagar a tabela 'especies' caso ela já exista (para garantir que a estrutura seja criada corretamente)
cursor.execute('DROP TABLE IF EXISTS especies')

# Criação da tabela 'especies' no banco de dados
cursor.execute('''
    CREATE TABLE IF NOT EXISTS especies (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        especie TEXT NOT NULL,
        nome_comum TEXT NOT NULL,
        descricao TEXT NOT NULL,
        imagem TEXT NOT NULL
    )
''')

# Inserir dados do Excel no banco de dados
for index, row in df.iterrows():
    especie = row['especie']  # Variável que contém o valor para a coluna 'especie'
    nome_comum = row['nome_comum']
    descricao = row['descricao']
    imagem = row['imagem']  # Nome do arquivo da imagem (ex: 'arara_azul.jpg')

    # Inserir na tabela 'especies'
    cursor.execute('''
        INSERT INTO especies (especie, nome_comum, descricao, imagem)
        VALUES (?, ?, ?, ?)
    ''', (especie, nome_comum, descricao, imagem))  # Passando os 4 valores corretamente

# Confirmar e fechar a conexão
conn.commit()
conn.close()

print(f'{len(df)} registros foram inseridos no banco de dados.')
