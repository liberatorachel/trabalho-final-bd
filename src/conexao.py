import psycopg2

def conectar():
    try:
        conexao = psycopg2.connect(
            dbname="biblioteca",       # nome do banco criado no pgAdmin
            user="postgres",            # seu usuário PostgreSQL
            password="130613",  # sua senha do PostgreSQL
            host="localhost",
            port="5432"
        )
        print("Conexão realizada com sucesso!")
        return conexao
    except Exception as e:
        print("Erro na conexão:", e)
        return None
