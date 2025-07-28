from database.connection import conectar # Importa a função de conexão
from utils import verificar_existencia, solicitar_data, obter_valor_banco_dados # Importa funções utilitárias

def inserir_usuario(email, nome, idade, data_nasc):
    """
    Insere um novo usuário no banco de dados.
    """
    conn = conectar()
    if conn:
        cur = conn.cursor()
        try:
            cur.execute("INSERT INTO Usuario (Email, Nome, Idade, Data_Nasc) VALUES (%s, %s, %s, %s);",
                        (email, nome, idade, data_nasc))
            conn.commit()
            print(f"Usuário '{nome}' (Email: {email}) inserido com sucesso!")
        except Exception as e:
            conn.rollback()
            print(f"Erro ao inserir usuário: {e}")
            if "duplicate key value violates unique constraint" in str(e):
                print("Verifique se o Email do usuário já existe.")
        finally:
            cur.close()
            conn.close()

def listar_usuarios():
    """
    Lista todos os usuários cadastrados no banco de dados.
    """
    conn = conectar()
    if conn:
        cur = conn.cursor()
        try:
            cur.execute("SELECT Email, Nome, Idade, Data_Nasc FROM Usuario ORDER BY Nome;")
            usuarios = cur.fetchall()
            if usuarios:
                print("\n--- Usuários Cadastrados ---")
                print("Email                        | Nome                   | Idade | Data Nasc.")
                print("-----------------------------|------------------------|-------|------------")
                for user in usuarios:
                    print(f"{user[0]:<28} | {user[1]:<22} | {user[2]:<5} | {user[3].strftime('%Y-%m-%d') if user[3] else 'N/A'}")
                print("-----------------------------------------------------------------------------")
            else:
                print("Nenhum usuário cadastrado.")
        except Exception as e:
            print(f"Erro ao listar usuários: {e}")
        finally:
            cur.close()
            conn.close()

def atualizar_usuario(email, novo_nome, nova_idade, nova_data_nasc):
    """
    Atualiza as informações de um usuário existente.
    """
    if not verificar_existencia("Usuario", "Email", email):
        print(f"Usuário com Email {email} não encontrado.")
        return

    conn = conectar()
    if conn:
        cur = conn.cursor()
        try:
            cur.execute("""
                UPDATE Usuario SET Nome = %s, Idade = %s, Data_Nasc = %s
                WHERE Email = %s;
            """, (novo_nome, nova_idade, nova_data_nasc, email))
            conn.commit()
            if cur.rowcount > 0:
                print(f"Usuário com Email {email} atualizado com sucesso!")
            else:
                print(f"Nenhuma alteração feita para o Usuário com Email {email}.")
        except Exception as e:
            conn.rollback()
            print(f"Erro ao atualizar usuário: {e}")
        finally:
            cur.close()
            conn.close()

def remover_usuario(email):
    """
    Remove um usuário do banco de dados, se não houver empréstimos ativos vinculados.
    A restrição FOREIGN KEY (ON DELETE RESTRICT) no Emprestimo cuida da validação.
    """
    if not verificar_existencia("Usuario", "Email", email):
        print(f"Usuário com Email {email} não encontrado.")
        return

    # Verificar se o usuário possui empréstimos ativos antes de tentar remover
    possui_emprestimos_ativos = obter_valor_banco_dados(
        "SELECT EXISTS(SELECT 1 FROM Emprestimo WHERE Email = %s AND Data_Dev_Real IS NULL);",
        (email,)
    )
    if possui_emprestimos_ativos:
        print(f"Erro: Usuário com Email {email} possui empréstimos ativos e não pode ser removido.")
        return

    conn = conectar()
    if conn:
        cur = conn.cursor()
        try:
            cur.execute("DELETE FROM Usuario WHERE Email = %s;", (email,))
            conn.commit()
            if cur.rowcount > 0:
                print(f"Usuário com Email {email} removido com sucesso!")
            else:
                print(f"Nenhum usuário removido (Email {email} não encontrado ou já removido).")
        except Exception as e:
            conn.rollback()
            print(f"Erro ao remover usuário: {e}")
            print("Pode ser que o usuário possua histórico de empréstimos não finalizados.")
        finally:
            cur.close()
            conn.close()