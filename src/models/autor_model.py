from database.connection import conectar # Importa a função de conexão
from utils import verificar_existencia, solicitar_data # Importa funções utilitárias

def inserir_autor(nome, nacionalidade, data_nascimento):
    """
    Insere um novo autor no banco de dados.
    """
    conn = conectar()
    if conn:
        cur = conn.cursor()
        try:
            cur.execute("INSERT INTO Autor (Nome, Nacionalidade, Data_Nascimento) VALUES (%s, %s, %s) RETURNING ID;",
                        (nome, nacionalidade, data_nascimento))
            autor_id = cur.fetchone()[0]
            conn.commit()
            print(f"Autor '{nome}' (ID: {autor_id}) inserido com sucesso!")
        except Exception as e:
            conn.rollback()
            print(f"Erro ao inserir autor: {e}")
        finally:
            cur.close()
            conn.close()

def listar_autores():
    """
    Lista todos os autores cadastrados no banco de dados.
    """
    conn = conectar()
    if conn:
        cur = conn.cursor()
        try:
            cur.execute("SELECT ID, Nome, Nacionalidade, Data_Nascimento FROM Autor ORDER BY Nome;")
            autores = cur.fetchall()
            if autores:
                print("\n--- Autores Cadastrados ---")
                print("ID   | Nome                   | Nacionalidade | Data Nasc.")
                print("-----|------------------------|---------------|------------")
                for autor in autores:
                    print(f"{autor[0]:<4} | {autor[1]:<22} | {autor[2]:<13} | {autor[3].strftime('%Y-%m-%d') if autor[3] else 'N/A'}")
                print("-------------------------------------------------------")
            else:
                print("Nenhum autor cadastrado.")
        except Exception as e:
            print(f"Erro ao listar autores: {e}")
        finally:
            cur.close()
            conn.close()

def atualizar_autor(id_autor, novo_nome, nova_nacionalidade, nova_data_nascimento):
    """
    Atualiza as informações de um autor existente.
    """
    if not verificar_existencia("Autor", "ID", id_autor):
        print(f"Autor com ID {id_autor} não encontrado.")
        return

    conn = conectar()
    if conn:
        cur = conn.cursor()
        try:
            cur.execute("UPDATE Autor SET Nome = %s, Nacionalidade = %s, Data_Nascimento = %s WHERE ID = %s;",
                        (novo_nome, nova_nacionalidade, nova_data_nascimento, id_autor))
            conn.commit()
            if cur.rowcount > 0:
                print(f"Autor com ID {id_autor} atualizado com sucesso!")
            else:
                print(f"Nenhuma alteração feita para o Autor com ID {id_autor}.")
        except Exception as e:
            conn.rollback()
            print(f"Erro ao atualizar autor: {e}")
        finally:
            cur.close()
            conn.close()

def remover_autor(id_autor):
    """
    Remove um autor do banco de dados, se não houver livros vinculados.
    A trigger 'trg_impedir_exclusao_autor' já cuida da validação de livros.
    """
    if not verificar_existencia("Autor", "ID", id_autor):
        print(f"Autor com ID {id_autor} não encontrado.")
        return

    conn = conectar()
    if conn:
        cur = conn.cursor()
        try:
            cur.execute("DELETE FROM Autor WHERE ID = %s;", (id_autor,))
            conn.commit()
            if cur.rowcount > 0:
                print(f"Autor com ID {id_autor} removido com sucesso!")
            else:
                print(f"Nenhum autor removido (ID {id_autor} não encontrado ou já removido).")
        except Exception as e:
            conn.rollback()
            print(f"Erro ao remover autor: {e}")
            print("Pode ser que o autor possua livros vinculados.") # A trigger já imprime uma mensagem mais específica.
        finally:
            cur.close()
            conn.close()