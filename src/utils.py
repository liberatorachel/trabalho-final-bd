from datetime import date, datetime
from database.connection import conectar

def obter_valor_banco_dados(consulta, parametros=None):
    conexao_db = conectar()
    if conexao_db:
        try:
            cursor = conexao_db.cursor()
            cursor.execute(consulta, parametros)
            resultado = cursor.fetchone()
            cursor.close()
            conexao_db.close()
            return resultado[0] if resultado else None
        except Exception as e:
            print(f"Erro ao obter valor do banco de dados: {e}")
            return None
    return None

def verificar_existencia(tabela, coluna, valor):
    consulta = f"SELECT EXISTS(SELECT 1 FROM {tabela} WHERE {coluna} = %s)"
    return obter_valor_banco_dados(consulta, (valor,))

def obter_isbn_livro_de_exemplar(numero_tombamento):
    consulta = "SELECT ISBN FROM Exemplar WHERE Num_Tombamento = %s"
    return obter_valor_banco_dados(consulta, (numero_tombamento,))

def solicitar_data(mensagem):
    while True:
        data_str = input(mensagem)
        if not data_str:
            return None
        try:
            return date.fromisoformat(data_str)
        except ValueError:
            print("Formato de data inválido. Por favor, use AAAA-MM-DD.")

def solicitar_inteiro(mensagem):
    while True:
        try:
            return int(input(mensagem))
        except ValueError:
            print("Entrada inválida. Por favor, digite um número inteiro.")
            