from connection import conectar

def teste():
    conexao = conectar()
    if conexao:
        conexao.close()
        print("Conexão encerrada com sucesso!")

if __name__ == "__main__":
    teste()
