from database.connection import conectar # Importa a função de conexão
from utils import verificar_existencia, obter_valor_banco_dados # Importa funções utilitárias

def inserir_livro(isbn, titulo, ano_publi, id_editora):
    """
    Insere um novo livro no banco de dados.
    A quantidade inicial é 0 e será atualizada automaticamente ao adicionar exemplares.
    """
    if not verificar_existencia("Editora", "ID_Editora", id_editora):
        print(f"Erro: Editora com ID {id_editora} não encontrada. Por favor, cadastre a editora primeiro.")
        return

    conn = conectar()
    if conn:
        cur = conn.cursor()
        try:
            cur.execute("INSERT INTO Livro (ISBN, Titulo, Ano_Publi, quantidade, ID_Editora) VALUES (%s, %s, %s, %s, %s);",
                        (isbn, titulo, ano_publi, 0, id_editora))
            conn.commit()
            print(f"Livro '{titulo}' (ISBN: {isbn}) inserido com sucesso!")
        except Exception as e:
            conn.rollback()
            print(f"Erro ao inserir livro: {e}")
            if "duplicate key value violates unique constraint" in str(e):
                print("Verifique se o ISBN já existe.")
        finally:
            cur.close()
            conn.close()

def listar_livros():
    """
    Lista todos os livros cadastrados, incluindo o nome da editora.
    """
    conn = conectar()
    if conn:
        cur = conn.cursor()
        try:
            cur.execute("""
                SELECT L.ISBN, L.Titulo, L.Ano_Publi, L.Quantidade, E.Nome as Editora
                FROM Livro L
                JOIN Editora E ON L.ID_Editora = E.ID_Editora
                ORDER BY L.Titulo;
            """)
            livros = cur.fetchall()
            if livros:
                print("\n--- Livros Cadastrados ---")
                print("ISBN                 | Título                     | Ano | Qtd | Editora")
                print("---------------------|----------------------------|-----|-----|------------------------")
                for livro in livros:
                    print(f"{livro[0]:<20} | {livro[1]:<26} | {livro[2]:<3} | {livro[3]:<3} | {livro[4]:<22}")
                print("-------------------------------------------------------------------------------------")
            else:
                print("Nenhum livro cadastrado.")
        except Exception as e:
            print(f"Erro ao listar livros: {e}")
        finally:
            cur.close()
            conn.close()

def atualizar_livro(isbn, novo_titulo, novo_ano_publi, novo_id_editora):
    """
    Atualiza as informações de um livro existente.
    """
    if not verificar_existencia("Livro", "ISBN", isbn):
        print(f"Livro com ISBN {isbn} não encontrado.")
        return
    if not verificar_existencia("Editora", "ID_Editora", novo_id_editora):
        print(f"Editora com ID {novo_id_editora} não encontrada. A atualização não pode ser realizada.")
        return

    conn = conectar()
    if conn:
        cur = conn.cursor()
        try:
            cur.execute("""
                UPDATE Livro SET Titulo = %s, Ano_Publi = %s, ID_Editora = %s
                WHERE ISBN = %s;
            """, (novo_titulo, novo_ano_publi, novo_id_editora, isbn))
            conn.commit()
            if cur.rowcount > 0:
                print(f"Livro com ISBN {isbn} atualizado com sucesso!")
            else:
                print(f"Nenhuma alteração feita para o Livro com ISBN {isbn}.")
        except Exception as e:
            conn.rollback()
            print(f"Erro ao atualizar livro: {e}")
        finally:
            cur.close()
            conn.close()

def remover_livro(isbn):
    """
    Remove um livro do banco de dados, se não houver exemplares vinculados.
    A trigger 'trg_ajuste_quantidade_exemplar_delete' em Exemplar
    e o 'ON DELETE CASCADE' no Livro para a tabela Exemplar e Escreve
    já cuidam das validações/cascateamento.
    """
    if not verificar_existencia("Livro", "ISBN", isbn):
        print(f"Livro com ISBN {isbn} não encontrado.")
        return

    # Verifica se há exemplares vinculados (se não houver CASCADE configurado para isso)
    # No seu DDL, Livro para Exemplar é CASCADE, então exemplares são removidos.
    # Se houver empréstimos, a remoção do exemplar já será impedida.
    
    # Validações extras para evitar erro de trigger ou restrição (embora CASCADE ajude)
    num_exemplares = obter_valor_banco_dados("SELECT COUNT(*) FROM Exemplar WHERE ISBN = %s;", (isbn,))
    if num_exemplares and num_exemplares > 0:
        print(f"Erro: O livro com ISBN {isbn} possui {num_exemplares} exemplar(es) vinculado(s). Remova-os primeiro.")
        return

    conn = conectar()
    if conn:
        cur = conn.cursor()
        try:
            # A remoção em Livro fará cascade em Escreve e Exemplar (se não tiver empréstimos)
            cur.execute("DELETE FROM Livro WHERE ISBN = %s;", (isbn,))
            conn.commit()
            if cur.rowcount > 0:
                print(f"Livro com ISBN {isbn} removido com sucesso!")
            else:
                print(f"Nenhum livro removido (ISBN {isbn} não encontrado ou já removido).")
        except Exception as e:
            conn.rollback()
            print(f"Erro ao remover livro: {e}")
            # Mensagens de erro de triggers específicas ou restrições podem aparecer aqui.
        finally:
            cur.close()
            conn.close()

def associar_autor_livro(id_autor, isbn):
    """
    Associa um autor a um livro (tabela Escreve).
    """
    if not verificar_existencia("Autor", "ID", id_autor):
        print(f"Autor com ID {id_autor} não encontrado.")
        return
    if not verificar_existencia("Livro", "ISBN", isbn):
        print(f"Livro com ISBN {isbn} não encontrado.")
        return

    conn = conectar()
    if conn:
        cur = conn.cursor()
        try:
            cur.execute("INSERT INTO Escreve (ID_Autor, ISBN) VALUES (%s, %s);", (id_autor, isbn))
            conn.commit()
            print(f"Autor ID {id_autor} associado ao livro ISBN {isbn} com sucesso!")
        except Exception as e:
            conn.rollback()
            print(f"Erro ao associar autor ao livro: {e}")
            if "duplicate key value violates unique constraint" in str(e):
                print("Esta associação já existe.")
        finally:
            cur.close()
            conn.close()

def desassociar_autor_livro(id_autor, isbn):
    """
    Desassocia um autor de um livro (remove da tabela Escreve).
    """
    conn = conectar()
    if conn:
        cur = conn.cursor()
        try:
            cur.execute("DELETE FROM Escreve WHERE ID_Autor = %s AND ISBN = %s;", (id_autor, isbn))
            conn.commit()
            if cur.rowcount > 0:
                print(f"Associação entre Autor ID {id_autor} e Livro ISBN {isbn} removida com sucesso!")
            else:
                print("Associação não encontrada.")
        except Exception as e:
            conn.rollback()
            print(f"Erro ao desassociar autor do livro: {e}")
        finally:
            cur.close()
            conn.close()

def listar_livros_por_autor(id_autor):
    """
    Lista todos os livros escritos por um autor específico.
    """
    if not verificar_existencia("Autor", "ID", id_autor):
        print(f"Autor com ID {id_autor} não encontrado.")
        return

    conn = conectar()
    if conn:
        cur = conn.cursor()
        try:
            cur.execute("""
                SELECT L.ISBN, L.Titulo, L.Ano_Publi, L.Quantidade, E.Nome as Editora
                FROM Livro L
                JOIN Escreve ES ON L.ISBN = ES.ISBN
                JOIN Autor A ON ES.ID_Autor = A.ID
                JOIN Editora E ON L.ID_Editora = E.ID_Editora
                WHERE A.ID = %s
                ORDER BY L.Titulo;
            """, (id_autor,))
            livros = cur.fetchall()
            if livros:
                nome_autor = obter_valor_banco_dados("SELECT Nome FROM Autor WHERE ID = %s;", (id_autor,))
                print(f"\n--- Livros escritos por {nome_autor} (ID: {id_autor}) ---")
                print("ISBN                 | Título                     | Ano | Qtd | Editora")
                print("---------------------|----------------------------|-----|-----|------------------------")
                for livro in livros:
                    print(f"{livro[0]:<20} | {livro[1]:<26} | {livro[2]:<3} | {livro[3]:<3} | {livro[4]:<22}")
                print("-------------------------------------------------------------------------------------")
            else:
                print(f"Nenhum livro encontrado para o autor com ID {id_autor}.")
        except Exception as e:
            print(f"Erro ao listar livros por autor: {e}")
        finally:
            cur.close()
            conn.close()

def listar_autores_por_livro(isbn):
    """
    Lista todos os autores de um livro específico.
    """
    if not verificar_existencia("Livro", "ISBN", isbn):
        print(f"Livro com ISBN {isbn} não encontrado.")
        return

    conn = conectar()
    if conn:
        cur = conn.cursor()
        try:
            cur.execute("""
                SELECT A.ID, A.Nome, A.Nacionalidade
                FROM Autor A
                JOIN Escreve ES ON A.ID = ES.ID_Autor
                JOIN Livro L ON ES.ISBN = L.ISBN
                WHERE L.ISBN = %s
                ORDER BY A.Nome;
            """, (isbn,))
            autores = cur.fetchall()
            if autores:
                titulo_livro = obter_valor_banco_dados("SELECT Titulo FROM Livro WHERE ISBN = %s;", (isbn,))
                print(f"\n--- Autores do Livro '{titulo_livro}' (ISBN: {isbn}) ---")
                print("ID   | Nome                   | Nacionalidade")
                print("-----|------------------------|---------------")
                for autor in autores:
                    print(f"{autor[0]:<4} | {autor[1]:<22} | {autor[2]:<13}")
                print("-----------------------------------------------")
            else:
                print(f"Nenhum autor encontrado para o livro com ISBN {isbn}.")
        except Exception as e:
            print(f"Erro ao listar autores por livro: {e}")
        finally:
            cur.close()
            conn.close()