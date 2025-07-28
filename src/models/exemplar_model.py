from database.connection import conectar # Importa a função de conexão
from utils import verificar_existencia, obter_valor_banco_dados # Importa funções utilitárias

def inserir_exemplar(isbn, num_prateleira):
    """
    Insere um novo exemplar de um livro no banco de dados.
    A quantidade do livro associado será automaticamente atualizada pela trigger.
    """
    if not verificar_existencia("Livro", "ISBN", isbn):
        print(f"Erro: Livro com ISBN {isbn} não encontrado. Cadastre o livro primeiro.")
        return

    conn = conectar()
    if conn:
        cur = conn.cursor()
        try:
            cur.execute("INSERT INTO Exemplar (ISBN, Num_Prateleira) VALUES (%s, %s) RETURNING Num_Tombamento;",
                        (isbn, num_prateleira))
            num_tombamento = cur.fetchone()[0]
            conn.commit()
            print(f"Exemplar (Nº Tombamento: {num_tombamento}) inserido com sucesso para o livro ISBN: {isbn}!")
        except Exception as e:
            conn.rollback()
            print(f"Erro ao inserir exemplar: {e}")
        finally:
            cur.close()
            conn.close()

def listar_exemplares():
    """
    Lista todos os exemplares cadastrados, incluindo o título do livro associado.
    """
    conn = conectar()
    if conn:
        cur = conn.cursor()
        try:
            cur.execute("""
                SELECT E.Num_Tombamento, E.Num_Prateleira, L.Titulo as Titulo_Livro, L.ISBN
                FROM Exemplar E
                JOIN Livro L ON E.ISBN = L.ISBN
                ORDER BY L.Titulo, E.Num_Prateleira;
            """)
            exemplares = cur.fetchall()
            if exemplares:
                print("\n--- Exemplares Cadastrados ---")
                print("Tombamento | Prateleira | Título do Livro            | ISBN")
                print("-----------|------------|----------------------------|--------------------")
                for ex in exemplares:
                    print(f"{ex[0]:<10} | {ex[1]:<10} | {ex[2]:<26} | {ex[3]:<18}")
                print("---------------------------------------------------------------------")
            else:
                print("Nenhum exemplar cadastrado.")
        except Exception as e:
            print(f"Erro ao listar exemplares: {e}")
        finally:
            cur.close()
            conn.close()

def atualizar_exemplar(num_tombamento, novo_num_prateleira, novo_isbn):
    """
    Atualiza as informações de um exemplar existente.
    """
    if not verificar_existencia("Exemplar", "Num_Tombamento", num_tombamento):
        print(f"Exemplar com Nº Tombamento {num_tombamento} não encontrado.")
        return
    if not verificar_existencia("Livro", "ISBN", novo_isbn):
        print(f"Novo ISBN {novo_isbn} não encontrado. A atualização não pode ser realizada.")
        return

    conn = conectar()
    if conn:
        cur = conn.cursor()
        try:
            cur.execute("""
                UPDATE Exemplar SET Num_Prateleira = %s, ISBN = %s
                WHERE Num_Tombamento = %s;
            """, (novo_num_prateleira, novo_isbn, num_tombamento))
            conn.commit()
            if cur.rowcount > 0:
                print(f"Exemplar com Nº Tombamento {num_tombamento} atualizado com sucesso!")
            else:
                print(f"Nenhuma alteração feita para o Exemplar com Nº Tombamento {num_tombamento}.")
        except Exception as e:
            conn.rollback()
            print(f"Erro ao atualizar exemplar: {e}")
        finally:
            cur.close()
            conn.close()

def remover_exemplar(num_tombamento):
    """
    Remove um exemplar do banco de dados.
    A trigger 'trg_ajuste_quantidade_exemplar_delete' em Exemplar
    e 'trg_verifica_exemplar_emprestado' em Emprestimo
    já cuidam das validações/ajustes de quantidade.
    """
    if not verificar_existencia("Exemplar", "Num_Tombamento", num_tombamento):
        print(f"Exemplar com Nº Tombamento {num_tombamento} não encontrado.")
        return

    # Verifica se o exemplar está emprestado antes de tentar remover (se a trigger não bastar)
    # A trigger no emprestimo (ON DELETE RESTRICT) já vai impedir, mas podemos adicionar um feedback.
    is_emprestado = obter_valor_banco_dados(
        "SELECT EXISTS(SELECT 1 FROM Emprestimo WHERE Num_Tombamento = %s AND Data_Dev_Real IS NULL);",
        (num_tombamento,)
    )
    if is_emprestado:
        print(f"Erro: Exemplar Nº Tombamento {num_tombamento} está atualmente emprestado e não pode ser removido.")
        return

    conn = conectar()
    if conn:
        cur = conn.cursor()
        try:
            cur.execute("DELETE FROM Exemplar WHERE Num_Tombamento = %s;", (num_tombamento,))
            conn.commit()
            if cur.rowcount > 0:
                print(f"Exemplar com Nº Tombamento {num_tombamento} removido com sucesso!")
            else:
                print(f"Nenhum exemplar removido (Nº Tombamento {num_tombamento} não encontrado ou já removido).")
        except Exception as e:
            conn.rollback()
            print(f"Erro ao remover exemplar: {e}")
            # A trigger de Emprestimo pode lançar erro se houver histórico de empréstimos sem devolução.
        finally:
            cur.close()
            conn.close()