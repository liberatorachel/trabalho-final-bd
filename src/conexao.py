import psycopg2

def conectar():
    try:
        conexao = psycopg2.connect(
            dbname="Biblioteca",
            user="postgres",          
            password="postgre", 
            host="localhost",
            port="5432"
        )
        print("Conexão realizada com sucesso!")
        return conexao
    except Exception as e:
        print("Erro na conexão:", e)
        return None
    
def inserirAutor(nome, nacionalidade, data_nascimento):
	try:
		conn = conectar()
		cur = conn.cursor()
		cur.execute("INSERT INTO Autor (nome, nacionalidade, data_nascimento) VALUES (%s, %s, %s)", (nome, nacionalidade, data_nascimento))
		conn.commit()
		cur.close()
		conn.close()
	except Exception as e:
		print(e)

inserirAutor("Tainá Caroline", "Brasileira", "2004-08-11")
