# Certifique-se de que estas importações estão no topo do seu arquivo:
from database.connection import conectar
from utils import verificar_existencia # 'obter_valor_banco_dados' e 'solicitar_data' não são usadas diretamente AQUI
from datetime import date # Apenas 'date' é necessário aqui, não 'datetime'

# --- FUNÇÃO CORRIGIDA: registrar_emprestimo ---
def registrar_emprestimo(num_tombamento, email_usuario, data_prev_dev_obj):
    """
    Registra um novo empréstimo de um exemplar para um usuário.
    data_prev_dev_obj DEVE ser um objeto datetime.date retornado por solicitar_data.
    """
    if not verificar_existencia("Exemplar", "Num_Tombamento", num_tombamento):
        print(f"Erro: Exemplar com Nº Tombamento {num_tombamento} não encontrado.")
        return
    if not verificar_existencia("Usuario", "Email", email_usuario):
        print(f"Erro: Usuário com Email {email_usuario} não encontrado.")
        return

    # Verificação para o caso de solicitar_data retornar None
    if data_prev_dev_obj is None:
        print("Erro: Data de Devolução Prevista não pode ser vazia.")
        return

    conn = conectar()
    if conn:
        cur = conn.cursor()
        try:
            # Pré-verificação de exemplar já emprestado
            cur.execute("SELECT COUNT(*) FROM Emprestimo WHERE Num_Tombamento = %s AND Data_Dev_Real IS NULL;", (num_tombamento,))
            if cur.fetchone()[0] > 0:
                print(f"Erro ao registrar empréstimo: Exemplar {num_tombamento} já está emprestado.")
                print("Motivo: O exemplar já está emprestado e não foi devolvido.")
                return

            data_emprestimo = date.today() # Data de empréstimo é a data atual

            # >>> AQUI: Usamos data_prev_dev_obj DIRETAMENTE, pois já é um objeto date <<<

            cur.execute(
                "INSERT INTO Emprestimo (Num_Tombamento, Email, Data_Empre, Data_Prev_Dev, Data_Dev_Real) "
                "VALUES (%s, %s, %s, %s, NULL);",
                (num_tombamento, email_usuario, data_emprestimo, data_prev_dev_obj)
            )
            conn.commit()
            print(f"Empréstimo do exemplar {num_tombamento} para o usuário {email_usuario} registrado com sucesso!")
        except Exception as e:
            conn.rollback()
            print(f"Erro ao registrar empréstimo: {e}")
            if "violates not-null constraint" in str(e).lower():
                print("Motivo: Verifique se todos os campos obrigatórios foram fornecidos ou se as datas estão no formato correto.")
            elif "duplicate key value violates unique constraint" in str(e).lower():
                print("Motivo: Um empréstimo com a mesma chave primária já existe. Isso pode ocorrer se você tentar registrar o mesmo empréstimo duas vezes sem devolver.")
        finally:
            cur.close()
            conn.close()

# --- FUNÇÃO CORRIGIDA: registrar_devolucao ---
def registrar_devolucao(num_tombamento, email_usuario, data_emprestimo_original_obj, data_dev_real_obj=None):
    """
    Registra a devolução de um exemplar.
    data_emprestimo_original_obj e data_dev_real_obj devem ser objetos datetime.date ou None.
    """
    # Verificação para o caso de solicitar_data retornar None para data_emprestimo_original_obj
    if data_emprestimo_original_obj is None:
        print("Erro: A Data do Empréstimo Original não pode ser vazia para registrar a devolução.")
        return

    if data_dev_real_obj is None:
        data_dev_real = date.today() # Data atual se não for fornecida
    else:
        data_dev_real = data_dev_real_obj # Usamos o objeto diretamente

    conn = conectar()
    if conn:
        cur = conn.cursor()
        try:
            cur.execute("""
                SELECT Data_Prev_Dev, Data_Dev_Real
                FROM Emprestimo
                WHERE Num_Tombamento = %s AND Email = %s AND Data_Empre = %s;
            """, (num_tombamento, email_usuario, data_emprestimo_original_obj)) # Usamos o objeto date diretamente
            emprestimo = cur.fetchone()

            if not emprestimo:
                print("Erro: Empréstimo não encontrado para os dados fornecidos (exemplar, usuário e data de empréstimo).")
                return

            data_prev_dev = emprestimo[0]
            data_dev_ja_registrada = emprestimo[1]

            if data_dev_ja_registrada is not None:
                print(f"Este empréstimo já foi devolvido em {data_dev_ja_registrada.strftime('%Y-%m-%d')}.")
                return

            cur.execute("""
                UPDATE Emprestimo
                SET Data_Dev_Real = %s
                WHERE Num_Tombamento = %s AND Email = %s AND Data_Empre = %s;
            """, (data_dev_real, num_tombamento, email_usuario, data_emprestimo_original_obj))
            
            conn.commit()

            if cur.rowcount > 0:
                print(f"Devolução do exemplar {num_tombamento} pelo usuário {email_usuario} registrada com sucesso!")
                
                if data_dev_real > data_prev_dev:
                    dias_atraso = (data_dev_real - data_prev_dev).days
                    print(f"ATENÇÃO: Devolução com {dias_atraso} dia(s) de atraso.")
            else:
                print("Nenhuma devolução registrada. Verifique os dados do empréstimo.")
        except Exception as e:
            conn.rollback()
            print(f"Erro ao registrar devolução: {e}")
        finally:
            cur.close()
            conn.close()

def listar_emprestimos(apenas_ativos=False, email_usuario=None, num_tombamento=None):
    """
    Lista empréstimos, podendo filtrar por ativos, por usuário ou por exemplar.
    """
    conn = conectar()
    if conn:
        cur = conn.cursor()
        try:
            query = """
                SELECT EM.Num_Tombamento, EM.Email, U.Nome as Nome_Usuario, L.Titulo as Titulo_Livro,
                       EM.Data_Empre, EM.Data_Prev_Dev, EM.Data_Dev_Real
                FROM Emprestimo EM
                JOIN Usuario U ON EM.Email = U.Email
                JOIN Exemplar EX ON EM.Num_Tombamento = EX.Num_Tombamento
                JOIN Livro L ON EX.ISBN = L.ISBN
            """
            condicoes = []
            parametros = []

            if apenas_ativos:
                condicoes.append("EM.Data_Dev_Real IS NULL")
            if email_usuario:
                condicoes.append("EM.Email = %s")
                parametros.append(email_usuario)
            if num_tombamento:
                condicoes.append("EM.Num_Tombamento = %s")
                parametros.append(num_tombamento)

            if condicoes:
                query += " WHERE " + " AND ".join(condicoes)
            
            query += " ORDER BY EM.Data_Empre DESC;"
            
            cur.execute(query, tuple(parametros))
            emprestimos = cur.fetchall()

            if emprestimos:
                status = "Ativos" if apenas_ativos else "Todos"
                print(f"\n--- {status} Empréstimos ---")
                print("Tomb. | Usuário Email          | Usuário Nome           | Livro Título               | Empréstimo | Prev. Devol. | Devol. Real")
                print("------|------------------------|------------------------|----------------------------|------------|--------------|------------")
                for emp in emprestimos:
                    data_dev_real_str = emp[6].strftime('%Y-%m-%d') if emp[6] else "PENDENTE"
                    print(f"{emp[0]:<5} | {emp[1]:<22} | {emp[2]:<22} | {emp[3]:<26} | {emp[4].strftime('%Y-%m-%d')} | {emp[5].strftime('%Y-%m-%d')} | {data_dev_real_str}")
                print("---------------------------------------------------------------------------------------------------------------------------------")
            else:
                msg = "Nenhum empréstimo "
                if apenas_ativos:
                    msg += "ativo "
                if email_usuario:
                    msg += f"para o usuário {email_usuario} "
                if num_tombamento:
                    msg += f"para o exemplar {num_tombamento} "
                msg += "encontrado."
                print(msg)
        except Exception as e:
            print(f"Erro ao listar empréstimos: {e}")
        finally:
            cur.close()
            conn.close()

def listar_emprestimos_atrasados():
    """
    Lista todos os empréstimos que estão atrasados (Data_Dev_Real é NULL e Data_Prev_Dev está no passado).
    """
    conn = conectar()
    if conn:
        cur = conn.cursor()
        try:
            query = """
                SELECT EM.Num_Tombamento, EM.Email, U.Nome as Nome_Usuario, L.Titulo as Titulo_Livro,
                       EM.Data_Empre, EM.Data_Prev_Dev, EM.Data_Dev_Real
                FROM Emprestimo EM
                JOIN Usuario U ON EM.Email = U.Email
                JOIN Exemplar EX ON EM.Num_Tombamento = EX.Num_Tombamento
                JOIN Livro L ON EX.ISBN = L.ISBN
                WHERE EM.Data_Dev_Real IS NULL AND EM.Data_Prev_Dev < CURRENT_DATE
                ORDER BY EM.Data_Prev_Dev ASC;
            """
            cur.execute(query)
            emprestimos_atrasados = cur.fetchall()

            if emprestimos_atrasados:
                print("\n--- Empréstimos Atrasados ---")
                print("Tomb. | Usuário Email          | Usuário Nome           | Livro Título               | Empréstimo | Prev. Devol.")
                print("------|------------------------|------------------------|----------------------------|------------|--------------")
                for emp in emprestimos_atrasados:
                    print(f"{emp[0]:<5} | {emp[1]:<22} | {emp[2]:<22} | {emp[3]:<26} | {emp[4].strftime('%Y-%m-%d')} | {emp[5].strftime('%Y-%m-%d')}")
                print("-------------------------------------------------------------------------------------------------------------")
            else:
                print("Nenhum empréstimo atrasado encontrado.")
        except Exception as e:
            print(f"Erro ao listar empréstimos atrasados: {e}")
        finally:
            cur.close()
            conn.close()

def contar_exemplares_disponiveis(isbn):
    """
    Conta quantos exemplares de um livro específico estão disponíveis (não emprestados).
    """
    if not verificar_existencia("Livro", "ISBN", isbn):
        print(f"Livro com ISBN {isbn} não encontrado.")
        return

    conn = conectar()
    if conn:
        cur = conn.cursor()
        try:
            # Contar exemplares que não estão em empréstimos ativos
            cur.execute("""
                SELECT COUNT(EX.Num_Tombamento)
                FROM Exemplar EX
                LEFT JOIN Emprestimo EM ON EX.Num_Tombamento = EM.Num_Tombamento AND EM.Data_Dev_Real IS NULL
                WHERE EX.ISBN = %s AND EM.Num_Tombamento IS NULL;
            """, (isbn,))
            disponiveis = cur.fetchone()[0]
            titulo_livro = obter_valor_banco_dados("SELECT Titulo FROM Livro WHERE ISBN = %s;", (isbn,))
            print(f"Livro '{titulo_livro}' (ISBN: {isbn}): {disponiveis} exemplar(es) disponível(eis).")
            return disponiveis
        except Exception as e:
            print(f"Erro ao contar exemplares disponíveis: {e}")
            return 0
        finally:
            cur.close()
            conn.close()

def listar_exemplares_disponiveis_por_livro(isbn):
    """
    Lista os números de tombamento dos exemplares disponíveis para um livro específico.
    """
    if not verificar_existencia("Livro", "ISBN", isbn):
        print(f"Livro com ISBN {isbn} não encontrado.")
        return

    conn = conectar()
    if conn:
        cur = conn.cursor()
        try:
            cur.execute("""
                SELECT EX.Num_Tombamento, EX.Num_Prateleira
                FROM Exemplar EX
                LEFT JOIN Emprestimo EM ON EX.Num_Tombamento = EM.Num_Tombamento AND EM.Data_Dev_Real IS NULL
                WHERE EX.ISBN = %s AND EM.Num_Tombamento IS NULL
                ORDER BY EX.Num_Tombamento;
            """, (isbn,))
            exemplares = cur.fetchall()
            titulo_livro = obter_valor_banco_dados("SELECT Titulo FROM Livro WHERE ISBN = %s;", (isbn,))
            if exemplares:
                print(f"\n--- Exemplares Disponíveis do Livro '{titulo_livro}' (ISBN: {isbn}) ---")
                print("Tombamento | Prateleira")
                print("-----------|------------")
                for ex in exemplares:
                    print(f"{ex[0]:<10} | {ex[1]:<10}")
                print("--------------------------")
            else:
                print(f"Nenhum exemplar disponível para o livro '{titulo_livro}' (ISBN: {isbn}).")
            return exemplares
        except Exception as e:
            print(f"Erro ao listar exemplares disponíveis: {e}")
            return []
        finally:
            cur.close()
            conn.close()