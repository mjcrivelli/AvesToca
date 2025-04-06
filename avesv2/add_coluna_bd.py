import sqlite3

# Conectar ao banco de dados (cria o arquivo se não existir)
conn = sqlite3.connect('database.db')
cursor = conn.cursor()

# Adicionar uma nova coluna à tabela
# Exemplo: Adicionando uma coluna "idade" do tipo INTEGER à tabela "aves"
cursor.execute("ALTER TABLE aves ADD COLUMN dimorfismo NOT NULL")
cursor.execute("ALTER TABLE aves ADD COLUMN ocorrencia NOT NULL")
cursor.execute("ALTER TABLE aves ADD COLUMN conservacao NOT NULL")

# Confirmar as alterações
conn.commit()

# Fechar a conexão
conn.close()

print("Nova coluna adicionada com sucesso!")