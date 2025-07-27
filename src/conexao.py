import psycopg2

def conectar():
    try:
        conexao = psycopg2.connect(
            dbname="biblioteca",
            user="postgres",          
            password="sqltayllan", 
            host="localhost",
            port="5432"
        )
        print("Conexão realizada com sucesso!")
        return conexao
    except Exception as e:
        print("Erro na conexão:", e)
        return None
