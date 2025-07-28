from database.connection import conectar # Importa a função de conexão

def executar_script_sql(filepath):
    """
    Lê e executa um script SQL a partir de um arquivo.
    Retorna True se bem-sucedido, False caso contrário.
    """
    try:
        with open(filepath, 'r') as f:
            sql_script = f.read()
    except FileNotFoundError:
        print(f"Erro: Arquivo '{filepath}' não encontrado.")
        return False
    except Exception as e:
        print(f"Erro ao ler o arquivo '{filepath}': {e}")
        return False

    conn = conectar()
    if conn:
        cur = conn.cursor()
        try:
            cur.execute(sql_script)
            conn.commit()
            print(f"Script '{filepath}' executado com sucesso!")
            return True
        except Exception as e:
            conn.rollback()
            print(f"Erro ao executar script SQL de '{filepath}': {e}")
            print("Verifique se o seu banco de dados 'Biblioteca' existe e se as tabelas anteriores foram limpas se for um re-criação.")
            return False
        finally:
            cur.close()
            conn.close()
    return False

def criar_estrutura_banco():
    """
    Função principal para criar todas as tabelas e triggers do banco de dados.
    """
    print("\n--- Iniciando a criação da estrutura do banco de dados ---")
    
    # Executa o script de criação de tabelas
    if not executar_script_sql('sql/create_tables.sql'):
        print("Falha crítica ao criar tabelas. Abortando criação da estrutura.")
        return

    # Executa o script de criação de funções e triggers
    if not executar_script_sql('sql/create_triggers.sql'):
        print("Falha crítica ao criar triggers. Abortando criação da estrutura.")
        return
        
    print("--- Estrutura do banco de dados inicializada com sucesso! ---")

if __name__ == "__main__":
    # Este bloco permite que você teste a criação da estrutura diretamente
    # ao executar "python src/schemas.py" no terminal.
    criar_estrutura_banco()