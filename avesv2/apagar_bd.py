import sqlite3

# Conectar ao banco de dados
conn = sqlite3.connect('database.db')
cursor = conn.cursor()

# Apagar todos os registros da tabela 'clientes'
cursor.execute("DELETE FROM aves")

# Confirmar a transação
conn.commit()

# Fechar a conexão
conn.close()

print("Todos os registros foram apagados com sucesso!")