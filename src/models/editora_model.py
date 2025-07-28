from database.connection import conectar # Importa a função de conexão
from utils import verificar_existencia # Importa funções utilitárias

def inserir_editora(nome, endereco, telefone, email, cnpj):
    """
    Insere uma nova editora no banco de dados.
    """
    conn = conectar()
    if conn:
        cur = conn.cursor()
        try:
            cur.execute("INSERT INTO Editora (Nome, Endereco, Telefone, Email, CNPJ) VALUES (%s, %s, %s, %s, %s) RETURNING ID_Editora;",
                        (nome, endereco, telefone, email, cnpj))
            editora_id = cur.fetchone()[0]
            conn.commit()
            print(f"Editora '{nome}' (ID: {editora_id}) inserida com sucesso!")
        except Exception as e:
            conn.rollback()
            print(f"Erro ao inserir editora: {e}")
            if "duplicate key value violates unique constraint" in str(e):
                print("Verifique se o Email ou CNPJ já existem.")
        finally:
            cur.close()
            conn.close()

def listar_editoras():
    """
    Lista todas as editoras cadastradas no banco de dados.
    """
    conn = conectar()
    if conn:
        cur = conn.cursor()
        try:
            cur.execute("SELECT ID_Editora, Nome, Endereco, Telefone, Email, CNPJ FROM Editora ORDER BY Nome;")
            editoras = cur.fetchall()
            if editoras:
                print("\n--- Editoras Cadastradas ---")
                print("ID   | Nome                   | Endereço               | Telefone         | Email                      | CNPJ")
                print("-----|------------------------|------------------------|------------------|----------------------------|--------------------")
                for editora in editoras:
                    print(f"{editora[0]:<4} | {editora[1]:<22} | {editora[2]:<22} | {editora[3]:<16} | {editora[4]:<26} | {editora[5]:<18}")
                print("---------------------------------------------------------------------------------------------------------------------")
            else:
                print("Nenhuma editora cadastrada.")
        except Exception as e:
            print(f"Erro ao listar editoras: {e}")
        finally:
            cur.close()
            conn.close()

def atualizar_editora(id_editora, novo_nome, novo_endereco, novo_telefone, novo_email, novo_cnpj):
    """
    Atualiza as informações de uma editora existente.
    """
    if not verificar_existencia("Editora", "ID_Editora", id_editora):
        print(f"Editora com ID {id_editora} não encontrada.")
        return

    conn = conectar()
    if conn:
        cur = conn.cursor()
        try:
            cur.execute("""
                UPDATE Editora SET Nome = %s, Endereco = %s, Telefone = %s, Email = %s, CNPJ = %s
                WHERE ID_Editora = %s;
            """, (novo_nome, novo_endereco, novo_telefone, novo_email, novo_cnpj, id_editora))
            conn.commit()
            if cur.rowcount > 0:
                print(f"Editora com ID {id_editora} atualizada com sucesso!")
            else:
                print(f"Nenhuma alteração feita para a Editora com ID {id_editora}.")
        except Exception as e:
            conn.rollback()
            print(f"Erro ao atualizar editora: {e}")
            if "duplicate key value violates unique constraint" in str(e):
                print("Verifique se o novo Email ou CNPJ já existem para outra editora.")
        finally:
            cur.close()
            conn.close()

def remover_editora(id_editora):
    """
    Remove uma editora do banco de dados, se não houver livros vinculados.
    A trigger 'trg_editora_com_livros' já cuida da validação de livros.
    """
    if not verificar_existencia("Editora", "ID_Editora", id_editora):
        print(f"Editora com ID {id_editora} não encontrada.")
        return

    conn = conectar()
    if conn:
        cur = conn.cursor()
        try:
            cur.execute("DELETE FROM Editora WHERE ID_Editora = %s;", (id_editora,))
            conn.commit()
            if cur.rowcount > 0:
                print(f"Editora com ID {id_editora} removida com sucesso!")
            else:
                print(f"Nenhuma editora removida (ID {id_editora} não encontrado ou já removido).")
        except Exception as e:
            conn.rollback()
            print(f"Erro ao remover editora: {e}")
            print("Pode ser que a editora possua livros vinculados.") # A trigger já imprime uma mensagem mais específica.
        finally:
            cur.close()
            conn.close()