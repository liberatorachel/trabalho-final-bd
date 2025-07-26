import psycopg2
from datetime import date, datetime, timedelta

def conectar():
    try:
        conexao_db = psycopg2.connect(
            dbname="Biblioteca",
            user="postgres",          
            password="postgre", 
            host="localhost",
            port="5432"
        )
        return conexao_db
    except Exception as e:
        print(f"Erro na conexão: {e}")
        return None

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

def inserir_autor(nome, nacionalidade, data_nascimento):
    conexao_db = conectar()
    if conexao_db:
        try:
            cursor = conexao_db.cursor()
            cursor.execute("INSERT INTO Autor (nome, nacionalidade, data_nascimento) VALUES (%s, %s, %s)", (nome, nacionalidade, data_nascimento))
            conexao_db.commit()
            print(f"Autor '{nome}' inserido com sucesso!")
        except Exception as e:
            print(f"Erro ao inserir autor: {e}")
        finally:
            if cursor: cursor.close()
            if conexao_db: conexao_db.close()

def atualizar_autor(id_autor, nome, nacionalidade, data_nascimento):
    conexao_db = conectar()
    if conexao_db:
        try:
            cursor = conexao_db.cursor()
            consulta = "UPDATE Autor SET Nome = %s, Nacionalidade = %s, Data_Nascimento = %s WHERE ID = %s"
            cursor.execute(consulta, (nome, nacionalidade, data_nascimento, id_autor))
            if cursor.rowcount > 0:
                print(f"Dados do autor ID {id_autor} atualizados com sucesso!")
            else:
                print(f"Nenhum autor encontrado com ID {id_autor}. Nenhuma linha foi atualizada.")
            conexao_db.commit()
        except Exception as e:
            print(f"Erro ao atualizar autor: {e}")
        finally:
            if cursor: cursor.close()
            if conexao_db: conexao_db.close()

def listar_autores():
    conexao_db = conectar()
    if conexao_db:
        try:
            cursor = conexao_db.cursor()
            cursor.execute("SELECT ID, Nome, Nacionalidade, Data_Nascimento FROM Autor ORDER BY ID")
            autores = cursor.fetchall()
            
            if autores:
                print("\n--- Lista de Autores ---")
                print(f"{'ID':<5} {'Nome':<30} {'Nacionalidade':<18} {'Data Nasc.':<12}")
                print("-" * 65)
                for autor in autores:
                    data_nasc_formatada = autor[3].strftime('%Y-%m-%d') if isinstance(autor[3], date) else "N/A"
                    print(f"{autor[0]:<5} {autor[1]:<30} {autor[2]:<18} {data_nasc_formatada:<12}")
                print("------------------------")
            else:
                print("Nenhum autor cadastrado.")
        except Exception as e:
            print(f"Erro ao listar autores: {e}")
        finally:
            if cursor: cursor.close()
            if conexao_db: conexao_db.close()

def inserir_editora(nome, endereco, telefone, email, cnpj):
    conexao_db = conectar()
    if conexao_db:
        try:
            cursor = conexao_db.cursor()
            nome_limpo = nome.strip().lower() 
            cursor.execute("INSERT INTO Editora (Nome, Endereco, Telefone, Email, CNPJ) VALUES (%s, %s, %s, %s, %s)", (nome_limpo, endereco, telefone, email, cnpj))
            conexao_db.commit()
            print(f"Editora '{nome_limpo}' inserida com sucesso!")
        except psycopg2.IntegrityError:
            print(f"Erro: Editora com o nome '{nome.strip().lower()}' já existe ou CNPJ duplicado.")
        except Exception as e:
            print(f"Erro ao inserir editora: {e}")
        finally:
            if cursor: cursor.close()
            if conexao_db: conexao_db.close()

def listar_editoras():
    conexao_db = conectar()
    if conexao_db:
        try:
            cursor = conexao_db.cursor()
            cursor.execute("SELECT ID_Editora, Nome, Endereco, Telefone, Email, CNPJ FROM Editora ORDER BY ID_Editora")
            editoras = cursor.fetchall()
            
            if editoras:
                print("\n--- Lista de Editoras ---")
                print(f"{'ID':<5} {'Nome':<20} {'Endereço':<25} {'Telefone':<15} {'Email':<25} {'CNPJ':<20}")
                print("-" * 115)
                for editora in editoras:
                    print(f"{editora[0]:<5} {editora[1]:<20} {editora[2]:<25} {editora[3]:<15} {editora[4]:<25} {editora[5]:<20}")
                print("------------------------")
            else:
                print("Nenhuma editora cadastrada.")
        except Exception as e:
            print(f"Erro ao listar editoras: {e}")
        finally:
            if cursor: cursor.close()
            if conexao_db: conexao_db.close()

def inserir_livro(isbn, titulo, ano_publicacao, quantidade, id_editora):
    if not verificar_existencia("Editora", "ID_Editora", id_editora):
        print(f"Erro: ID da Editora {id_editora} não existe. Por favor, insira a editora primeiro.")
        return

    conexao_db = conectar()
    if conexao_db:
        try:
            cursor = conexao_db.cursor()
            consulta = "INSERT INTO Livro (ISBN, Titulo, Ano_Publi, Quantidade, ID_Editora) VALUES (%s, %s, %s, %s, %s)"
            cursor.execute(consulta, (isbn, titulo, ano_publicacao, quantidade, id_editora))
            conexao_db.commit()
            print(f"Livro '{titulo}' (ISBN: {isbn}) inserido com sucesso!")
            for i in range(quantidade):
                inserir_exemplar("", isbn) 
            print(f"{quantidade} exemplares para o livro '{titulo}' (ISBN: {isbn}) inseridos automaticamente.")
        except psycopg2.IntegrityError:
            print(f"Erro: Livro com ISBN '{isbn}' já existe.")
        except Exception as e:
            print(f"Erro ao inserir livro: {e}")
        finally:
            if cursor: cursor.close()
            if conexao_db: conexao_db.close()

def atualizar_livro(isbn, titulo=None, ano_publicacao=None, quantidade=None, id_editora=None):
    conexao_db = conectar()
    if conexao_db:
        try:
            cursor = conexao_db.cursor()
            atualizacoes = []
            parametros = []
            
            if titulo is not None:
                atualizacoes.append("Titulo = %s")
                parametros.append(titulo)
            if ano_publicacao is not None:
                atualizacoes.append("Ano_Publi = %s")
                parametros.append(ano_publicacao)
            if quantidade is not None:
                atualizacoes.append("Quantidade = %s")
                parametros.append(quantidade)
            if id_editora is not None:
                if not verificar_existencia("Editora", "ID_Editora", id_editora):
                    print(f"Erro: ID da Editora {id_editora} não existe. Não é possível atualizar.")
                    return
                atualizacoes.append("ID_Editora = %s")
                parametros.append(id_editora)

            if not atualizacoes:
                print("Nenhum dado fornecido para atualização do livro.")
                return

            consulta = f"UPDATE Livro SET {', '.join(atualizacoes)} WHERE ISBN = %s"
            parametros.append(isbn)
            
            cursor.execute(consulta, parametros)
            if cursor.rowcount > 0:
                print(f"Livro com ISBN {isbn} atualizado com sucesso!")
            else:
                print(f"Nenhum livro encontrado com ISBN {isbn}. Nenhuma linha foi atualizada.")
            conexao_db.commit()
        except Exception as e:
            print(f"Erro ao atualizar livro: {e}")
        finally:
            if cursor: cursor.close()
            if conexao_db: conexao_db.close()

def listar_livros():
    conexao_db = conectar()
    if conexao_db:
        try:
            cursor = conexao_db.cursor()
            consulta = """
            SELECT L.ISBN, L.Titulo, L.Ano_Publi, L.Quantidade, E.Nome
            FROM Livro L
            JOIN Editora E ON L.ID_Editora = E.ID_Editora
            ORDER BY L.Titulo
            """
            cursor.execute(consulta)
            livros = cursor.fetchall()
            
            if livros:
                print("\n--- Lista de Livros ---")
                print(f"{'ISBN':<17} {'Título':<40} {'Ano':<6} {'Qtd':<5} {'Editora':<25}")
                print("-" * 95)
                for livro in livros:
                    print(f"{livro[0]:<17} {livro[1]:<40} {livro[2]:<6} {livro[3]:<5} {livro[4]:<25}")
                print("------------------------")
            else:
                print("Nenhum livro cadastrado.")
        except Exception as e:
            print(f"Erro ao listar livros: {e}")
        finally:
            if cursor: cursor.close()
            if conexao_db: conexao_db.close()

def inserir_exemplar(numero_prateleira, isbn):
    if not verificar_existencia("Livro", "ISBN", isbn):
        print(f"Erro: ISBN '{isbn}' não existe. Por favor, insira o livro primeiro.")
        return

    conexao_db = conectar()
    if conexao_db:
        try:
            cursor = conexao_db.cursor()
            consulta = "INSERT INTO Exemplar (Num_Prateleira, ISBN) VALUES (%s, %s)"
            cursor.execute(consulta, (numero_prateleira, isbn))
            conexao_db.commit()
            print(f"Exemplar inserido para ISBN '{isbn}'.")
        except Exception as e:
            print(f"Erro ao inserir exemplar: {e}")
        finally:
            if cursor: cursor.close()
            if conexao_db: conexao_db.close()

def listar_exemplares():
    conexao_db = conectar()
    if conexao_db:
        try:
            cursor = conexao_db.cursor()
            consulta = """
            SELECT E.Num_Tombamento, E.Num_Prateleira, L.Titulo, L.ISBN
            FROM Exemplar E
            JOIN Livro L ON E.ISBN = L.ISBN
            ORDER BY E.Num_Tombamento
            """
            cursor.execute(consulta)
            exemplares = cursor.fetchall()
            
            if exemplares:
                print("\n--- Lista de Exemplares ---")
                print(f"{'Tomb.':<8} {'Prateleira':<15} {'Título do Livro':<40} {'ISBN':<17}")
                print("-" * 85)
                for exemplar in exemplares:
                    print(f"{exemplar[0]:<8} {exemplar[1]:<15} {exemplar[2]:<40} {exemplar[3]:<17}")
                print("--------------------------")
            else:
                print("Nenhum exemplar cadastrado.")
        except Exception as e:
            print(f"Erro ao listar exemplares: {e}")
        finally:
            if cursor: cursor.close()
            if conexao_db: conexao_db.close()

def inserir_usuario(email, nome, idade, data_nascimento):
    conexao_db = conectar()
    if conexao_db:
        try:
            cursor = conexao_db.cursor()
            consulta = "INSERT INTO Usuario (Email, Nome, Idade, Data_Nasc) VALUES (%s, %s, %s, %s)"
            cursor.execute(consulta, (email, nome, idade, data_nascimento))
            conexao_db.commit()
            print(f"Usuário '{nome}' ({email}) inserido com sucesso!")
        except psycopg2.IntegrityError:
            print(f"Erro: Usuário com Email '{email}' já existe.")
        except Exception as e:
            print(f"Erro ao inserir usuário: {e}")
        finally:
            if cursor: cursor.close()
            if conexao_db: conexao_db.close()

def atualizar_usuario(email, nome=None, idade=None, data_nascimento=None):
    conexao_db = conectar()
    if conexao_db:
        try:
            cursor = conexao_db.cursor()
            atualizacoes = []
            parametros = []
            
            if nome is not None:
                atualizacoes.append("Nome = %s")
                parametros.append(nome)
            if idade is not None:
                atualizacoes.append("Idade = %s")
                parametros.append(idade)
            if data_nascimento is not None:
                atualizacoes.append("Data_Nasc = %s")
                parametros.append(data_nascimento)

            if not atualizacoes:
                print("Nenhum dado fornecido para atualização do usuário.")
                return

            consulta = f"UPDATE Usuario SET {', '.join(atualizacoes)} WHERE Email = %s"
            parametros.append(email)
            
            cursor.execute(consulta, parametros)
            if cursor.rowcount > 0:
                print(f"Usuário com Email {email} atualizado com sucesso!")
            else:
                print(f"Nenhum usuário encontrado com Email {email}. Nenhuma linha foi atualizada.")
            conexao_db.commit()
        except Exception as e:
            print(f"Erro ao atualizar usuário: {e}")
        finally:
            if cursor: cursor.close()
            if conexao_db: conexao_db.close()

def listar_usuarios():
    conexao_db = conectar()
    if conexao_db:
        try:
            cursor = conexao_db.cursor()
            cursor.execute("SELECT Email, Nome, Idade, Data_Nasc FROM Usuario ORDER BY Nome")
            usuarios = cursor.fetchall()
            
            if usuarios:
                print("\n--- Lista de Usuários ---")
                print(f"{'Email':<30} {'Nome':<30} {'Idade':<6} {'Data Nasc.':<12}")
                print("-" * 80)
                for usuario in usuarios:
                    data_nasc_formatada = usuario[3].strftime('%Y-%m-%d') if isinstance(usuario[3], date) else "N/A"
                    print(f"{usuario[0]:<30} {usuario[1]:<30} {usuario[2]:<6} {data_nasc_formatada:<12}")
                print("-------------------------")
            else:
                print("Nenhum usuário cadastrado.")
        except Exception as e:
            print(f"Erro ao listar usuários: {e}")
        finally:
            if cursor: cursor.close()
            if conexao_db: conexao_db.close()

def associar_autor_livro(id_autor, isbn):
    if not verificar_existencia("Autor", "ID", id_autor):
        print(f"Erro: ID do Autor {id_autor} não existe.")
        return
    if not verificar_existencia("Livro", "ISBN", isbn):
        print(f"Erro: ISBN '{isbn}' não existe.")
        return

    conexao_db = conectar()
    if conexao_db:
        try:
            cursor = conexao_db.cursor()
            consulta = "INSERT INTO Escreve (ID_Autor, ISBN) VALUES (%s, %s)"
            cursor.execute(consulta, (id_autor, isbn))
            conexao_db.commit()
            print(f"Autor ID {id_autor} associado ao livro ISBN '{isbn}' com sucesso!")
        except psycopg2.IntegrityError:
            print(f"Erro: Esta associação (Autor ID {id_autor} - Livro ISBN '{isbn}') já existe.")
        except Exception as e:
            print(f"Erro ao associar autor ao livro: {e}")
        finally:
            if cursor: cursor.close()
            if conexao_db: conexao_db.close()

def listar_livros_por_autor(id_autor):
    conexao_db = conectar()
    if conexao_db:
        try:
            cursor = conexao_db.cursor()
            consulta = """
            SELECT L.ISBN, L.Titulo, L.Ano_Publi
            FROM Livro L
            JOIN Escreve E ON L.ISBN = E.ISBN
            WHERE E.ID_Autor = %s
            ORDER BY L.Titulo
            """
            cursor.execute(consulta, (id_autor,))
            livros = cursor.fetchall()
            
            if livros:
                nome_autor = obter_valor_banco_dados("SELECT Nome FROM Autor WHERE ID = %s", (id_autor,))
                print(f"\n--- Livros Escritos por {nome_autor or 'ID ' + str(id_autor)} ---")
                print(f"{'ISBN':<17} {'Título':<40} {'Ano':<6}")
                print("-" * 65)
                for livro in livros:
                    print(f"{livro[0]:<17} {livro[1]:<40} {livro[2]:<6}")
                print("---------------------------------------------")
            else:
                print(f"Nenhum livro encontrado para o autor ID {id_autor}.")
        except Exception as e:
            print(f"Erro ao listar livros por autor: {e}")
        finally:
            if cursor: cursor.close()
            if conexao_db: conexao_db.close()

def registrar_emprestimo(numero_tombamento, email_usuario, data_emprestimo, data_prevista_devolucao):
    if not verificar_existencia("Exemplar", "Num_Tombamento", numero_tombamento):
        print(f"Erro: Exemplar com número de tombamento {numero_tombamento} não existe.")
        return
    if not verificar_existencia("Usuario", "Email", email_usuario):
        print(f"Erro: Usuário com email '{email_usuario}' não existe.")
        return

    isbn = obter_isbn_livro_de_exemplar(numero_tombamento)
    if not isbn:
        print(f"Erro: Não foi possível encontrar o livro associado ao exemplar {numero_tombamento}.")
        return

    conexao_db = conectar()
    if conexao_db:
        try:
            cursor = conexao_db.cursor()
            
            cursor.execute("SELECT Quantidade FROM Livro WHERE ISBN = %s FOR UPDATE", (isbn,))
            quantidade_atual = cursor.fetchone()[0]
            
            if quantidade_atual <= 0:
                print(f"Erro: Livro (ISBN: {isbn}) não tem exemplares disponíveis para empréstimo.")
                conexao_db.rollback()
                return

            cursor.execute("""
                SELECT COUNT(*) FROM Emprestimo 
                WHERE Num_Tombamento = %s AND Data_Dev_Real IS NULL
            """, (numero_tombamento,))
            if cursor.fetchone()[0] > 0:
                print(f"Erro: Exemplar {numero_tombamento} já está emprestado e não foi devolvido.")
                conexao_db.rollback()
                return

            consulta_emprestimo = "INSERT INTO Emprestimo (Num_Tombamento, Email, Data_Empre, Data_Prev_Dev) VALUES (%s, %s, %s, %s)"
            cursor.execute(consulta_emprestimo, (numero_tombamento, email_usuario, data_emprestimo, data_prevista_devolucao))

            consulta_atualizar_livro = "UPDATE Livro SET Quantidade = Quantidade - 1 WHERE ISBN = %s"
            cursor.execute(consulta_atualizar_livro, (isbn,))
            
            conexao_db.commit()
            print(f"Empréstimo do exemplar {numero_tombamento} para {email_usuario} registrado com sucesso!")
        except Exception as e:
            print(f"Erro ao registrar empréstimo: {e}")
            if conexao_db: conexao_db.rollback()
        finally:
            if cursor: cursor.close()
            if conexao_db: conexao_db.close()

def registrar_devolucao(numero_tombamento, email_usuario, data_emprestimo_original, data_real_devolucao):
    conexao_db = conectar()
    if conexao_db:
        try:
            cursor = conexao_db.cursor()

            cursor.execute("""
                SELECT ISBN, Data_Prev_Dev 
                FROM Emprestimo E JOIN Exemplar EX ON E.Num_Tombamento = EX.Num_Tombamento
                WHERE E.Num_Tombamento = %s AND E.Email = %s AND E.Data_Empre = %s AND E.Data_Dev_Real IS NULL FOR UPDATE
            """, (numero_tombamento, email_usuario, data_emprestimo_original))
            
            resultado = cursor.fetchone()
            if not resultado:
                print("Erro: Empréstimo não encontrado ou já foi devolvido.")
                conexao_db.rollback()
                return

            isbn, data_prevista_devolucao = resultado[0], resultado[1]

            consulta_atualizar_emprestimo = "UPDATE Emprestimo SET Data_Dev_Real = %s WHERE Num_Tombamento = %s AND Email = %s AND Data_Empre = %s"
            cursor.execute(consulta_atualizar_emprestimo, (data_real_devolucao, numero_tombamento, email_usuario, data_emprestimo_original))

            consulta_atualizar_livro = "UPDATE Livro SET Quantidade = Quantidade + 1 WHERE ISBN = %s"
            cursor.execute(consulta_atualizar_livro, (isbn,))
            
            conexao_db.commit()
            print(f"Devolução do exemplar {numero_tombamento} por {email_usuario} registrada com sucesso!")

            if data_real_devolucao > data_prevista_devolucao:
                dias_atraso = (data_real_devolucao - data_prevista_devolucao).days
                print(f"ATENÇÃO: Este livro foi devolvido com {dias_atraso} dia(s) de atraso.")

        except Exception as e:
            print(f"Erro ao registrar devolução: {e}")
            if conexao_db: conexao_db.rollback()
        finally:
            if cursor: cursor.close()
            if conexao_db: conexao_db.close()

def listar_emprestimos(apenas_ativos=False):
    conexao_db = conectar()
    if conexao_db:
        try:
            cursor = conexao_db.cursor()
            consulta = """
            SELECT 
                E.Num_Tombamento, L.Titulo, U.Nome AS Usuario_Nome, 
                E.Data_Empre, E.Data_Prev_Dev, E.Data_Dev_Real
            FROM Emprestimo E
            JOIN Usuario U ON E.Email = U.Email
            JOIN Exemplar EX ON E.Num_Tombamento = EX.Num_Tombamento
            JOIN Livro L ON EX.ISBN = L.ISBN
            """
            if apenas_ativos:
                consulta += " WHERE E.Data_Dev_Real IS NULL"
            consulta += " ORDER BY E.Data_Empre DESC"

            cursor.execute(consulta)
            emprestimos = cursor.fetchall()
            
            if emprestimos:
                status = "Ativos" if apenas_ativos else "Todos"
                print(f"\n--- Lista de Empréstimos ({status}) ---")
                print(f"{'Tomb.':<8} {'Livro':<35} {'Usuário':<25} {'Empréstimo':<12} {'Prev. Dev.':<12} {'Dev. Real':<12}")
                print("-" * 110)
                for emp in emprestimos:
                    data_emprestimo_formatada = emp[3].strftime('%Y-%m-%d')
                    data_prevista_formatada = emp[4].strftime('%Y-%m-%d')
                    data_real_formatada = emp[5].strftime('%Y-%m-%d') if emp[5] else "Em Aberto"
                    print(f"{emp[0]:<8} {emp[1]:<35} {emp[2]:<25} {data_emprestimo_formatada:<12} {data_prevista_formatada:<12} {data_real_formatada:<12}")
                print("--------------------------------------------------------------------------------------------------")
            else:
                status = "ativos" if apenas_ativos else "cadastrados"
                print(f"Nenhum empréstimo {status}.")
        except Exception as e:
            print(f"Erro ao listar empréstimos: {e}")
        finally:
            if cursor: cursor.close()
            if conexao_db: conexao_db.close()

def menu_autores():
    while True:
        print("\n--- Gerenciar Autores ---")
        print("1. Inserir Novo Autor")
        print("2. Atualizar Autor Existente")
        print("3. Listar Todos os Autores")
        print("4. Voltar ao Menu Principal")
        
        escolha = input("Escolha uma opção: ")

        if escolha == '1':
            nome = input("Digite o nome do autor: ")
            nacionalidade = input("Digite a nacionalidade do autor: ")
            data_nascimento = solicitar_data("Digite a data de nascimento (AAAA-MM-DD): ")
            inserir_autor(nome, nacionalidade, data_nascimento)
        
        elif escolha == '2':
            id_autor = solicitar_inteiro("Digite o ID do autor para atualizar: ")
            if not verificar_existencia("Autor", "ID", id_autor):
                print(f"Erro: Autor com ID {id_autor} não existe.")
                continue
            
            conexao_db = conectar()
            nome_atual = nacionalidade_atual = data_nascimento_atual = None
            if conexao_db:
                try:
                    cursor = conexao_db.cursor()
                    cursor.execute("SELECT Nome, Nacionalidade, Data_Nascimento FROM Autor WHERE ID = %s", (id_autor,))
                    dados = cursor.fetchone()
                    if dados:
                        nome_atual, nacionalidade_atual, data_nascimento_atual = dados
                except Exception as e:
                    print(f"Erro ao buscar dados atuais do autor: {e}")
                finally:
                    if cursor: cursor.close()
                    if conexao_db: conexao_db.close()
            
            nome = input(f"Digite o novo nome (atual: {nome_atual or 'N/A'}, deixe em branco para não alterar): ") or nome_atual
            nacionalidade = input(f"Digite a nova nacionalidade (atual: {nacionalidade_atual or 'N/A'}, deixe em branco para não alterar): ") or nacionalidade_atual
            
            entrada_data_nascimento = solicitar_data(f"Digite a nova data de nascimento (atual: {data_nascimento_atual.strftime('%Y-%m-%d') if data_nascimento_atual else 'N/A'}, AAAA-MM-DD, deixe em branco para não alterar): ")
            data_nascimento = entrada_data_nascimento if entrada_data_nascimento is not None else data_nascimento_atual

            atualizar_autor(id_autor, nome, nacionalidade, data_nascimento)

        elif escolha == '3':
            listar_autores()

        elif escolha == '4':
            break
        
        else:
            print("Opção inválida. Por favor, tente novamente.")

def menu_editoras():
    while True:
        print("\n--- Gerenciar Editoras ---")
        print("1. Inserir Nova Editora")
        print("2. Listar Todas as Editoras")
        print("3. Voltar ao Menu Principal")
        
        escolha = input("Escolha uma opção: ")

        if escolha == '1':
            nome = input("Digite o nome da editora: ")
            endereco = input("Digite o endereço da editora: ")
            telefone = input("Digite o telefone da editora: ")
            email = input("Digite o email da editora: ")
            cnpj = input("Digite o CNPJ da editora: ")
            inserir_editora(nome, endereco, telefone, email, cnpj) # Passa todos os campos
        
        elif escolha == '2':
            listar_editoras()

        elif escolha == '3':
            break
        
        else:
            print("Opção inválida. Por favor, tente novamente.")

def menu_livros():
    while True:
        print("\n--- Gerenciar Livros ---")
        print("1. Inserir Novo Livro")
        print("2. Atualizar Livro Existente")
        print("3. Listar Todos os Livros")
        print("4. Associar Autor a Livro")
        print("5. Listar Livros por Autor")
        print("6. Voltar ao Menu Principal")
        
        escolha = input("Escolha uma opção: ")

        if escolha == '1':
            isbn = input("Digite o ISBN do livro (ex: 978-3-16-148410-0): ")
            titulo = input("Digite o título do livro: ")
            ano_publicacao = solicitar_inteiro("Digite o ano de publicação: ")
            quantidade = solicitar_inteiro("Digite a quantidade inicial de exemplares: ")
            listar_editoras()
            id_editora = solicitar_inteiro("Digite o ID da Editora: ")
            inserir_livro(isbn, titulo, ano_publicacao, quantidade, id_editora)
        
        elif escolha == '2':
            isbn = input("Digite o ISBN do livro para atualizar: ")
            if not verificar_existencia("Livro", "ISBN", isbn):
                print(f"Erro: Livro com ISBN '{isbn}' não existe.")
                continue

            conexao_db = conectar()
            titulo_atual = ano_publicacao_atual = quantidade_atual = id_editora_atual = None
            if conexao_db:
                try:
                    cursor = conexao_db.cursor()
                    cursor.execute("SELECT Titulo, Ano_Publi, Quantidade, ID_Editora FROM Livro WHERE ISBN = %s", (isbn,))
                    dados = cursor.fetchone()
                    if dados:
                        titulo_atual, ano_publicacao_atual, quantidade_atual, id_editora_atual = dados
                except Exception as e:
                    print(f"Erro ao buscar dados atuais do livro: {e}")
                finally:
                    if cursor: cursor.close()
                    if conexao_db: conexao_db.close()
            
            titulo = input(f"Digite o novo título (atual: {titulo_atual or 'N/A'}, deixe em branco para não alterar): ") or titulo_atual
            
            str_ano_publicacao = input(f"Digite o novo ano de publicação (atual: {ano_publicacao_atual or 'N/A'}, deixe em branco para não alterar): ")
            ano_publicacao = solicitar_inteiro("Digite o novo ano de publicação: ") if str_ano_publicacao else ano_publicacao_atual

            str_quantidade = input(f"Digite a nova quantidade (atual: {quantidade_atual or 'N/A'}, deixe em branco para não alterar): ")
            quantidade = solicitar_inteiro("Digite a nova quantidade: ") if str_quantidade else quantidade_atual

            listar_editoras()
            str_id_editora = input(f"Digite o novo ID da Editora (atual: {id_editora_atual or 'N/A'}, deixe em branco para não alterar): ")
            id_editora = solicitar_inteiro("Digite o novo ID da Editora: ") if str_id_editora else id_editora_atual

            atualizar_livro(isbn, titulo, ano_publicacao, quantidade, id_editora)

        elif escolha == '3':
            listar_livros()

        elif escolha == '4':
            listar_autores()
            id_autor = solicitar_inteiro("Digite o ID do autor para associar: ")
            listar_livros()
            isbn = input("Digite o ISBN do livro para associar: ")
            associar_autor_livro(id_autor, isbn)

        elif escolha == '5':
            listar_autores()
            id_autor = solicitar_inteiro("Digite o ID do autor para listar seus livros: ")
            listar_livros_por_autor(id_autor)

        elif escolha == '6':
            break
        
        else:
            print("Opção inválida. Por favor, tente novamente.")

def menu_exemplares():
    while True:
        print("\n--- Gerenciar Exemplares ---")
        print("1. Inserir Novo Exemplar")
        print("2. Listar Todos os Exemplares")
        print("3. Voltar ao Menu Principal")
        
        escolha = input("Escolha uma opção: ")

        if escolha == '1':
            numero_prateleira = input("Digite o número da prateleira do exemplar: ")
            listar_livros()
            isbn = input("Digite o ISBN do livro ao qual este exemplar pertence: ")
            inserir_exemplar(numero_prateleira, isbn)
        
        elif escolha == '2':
            listar_exemplares()

        elif escolha == '3':
            break
        
        else:
            print("Opção inválida. Por favor, tente novamente.")

def menu_usuarios():
    while True:
        print("\n--- Gerenciar Usuários ---")
        print("1. Inserir Novo Usuário")
        print("2. Atualizar Usuário Existente")
        print("3. Listar Todos os Usuários")
        print("4. Voltar ao Menu Principal")
        
        escolha = input("Escolha uma opção: ")

        if escolha == '1':
            email = input("Digite o email do usuário: ")
            nome = input("Digite o nome do usuário: ")
            idade = solicitar_inteiro("Digite a idade do usuário: ")
            data_nascimento = solicitar_data("Digite a data de nascimento (AAAA-MM-DD): ")
            inserir_usuario(email, nome, idade, data_nascimento)
        
        elif escolha == '2':
            email = input("Digite o email do usuário para atualizar: ")
            if not verificar_existencia("Usuario", "Email", email):
                print(f"Erro: Usuário com Email '{email}' não existe.")
                continue
            
            conexao_db = conectar()
            nome_atual = idade_atual = data_nascimento_atual = None
            if conexao_db:
                try:
                    cursor = conexao_db.cursor()
                    cursor.execute("SELECT Nome, Idade, Data_Nasc FROM Usuario WHERE Email = %s", (email,))
                    dados = cursor.fetchone()
                    if dados:
                        nome_atual, idade_atual, data_nascimento_atual = dados
                except Exception as e:
                    print(f"Erro ao buscar dados atuais do usuário: {e}")
                finally:
                    if cursor: cursor.close()
                    if conexao_db: conexao_db.close()

            nome = input(f"Digite o novo nome (atual: {nome_atual or 'N/A'}, deixe em branco para não alterar): ") or nome_atual
            
            str_idade = input(f"Digite a nova idade (atual: {idade_atual or 'N/A'}, deixe em branco para não alterar): ")
            idade = solicitar_inteiro("Digite a nova idade: ") if str_idade else idade_atual

            entrada_data_nascimento = solicitar_data(f"Digite a nova data de nascimento (atual: {data_nascimento_atual.strftime('%Y-%m-%d') if data_nascimento_atual else 'N/A'}, AAAA-MM-DD, deixe em branco para não alterar): ")
            data_nascimento = entrada_data_nascimento if entrada_data_nascimento is not None else data_nascimento_atual

            atualizar_usuario(email, nome, idade, data_nascimento)

        elif escolha == '3':
            listar_usuarios()

        elif escolha == '4':
            break
        
        else:
            print("Opção inválida. Por favor, tente novamente.")

def menu_emprestimos():
    while True:
        print("\n--- Gerenciar Empréstimos ---")
        print("1. Registrar Novo Empréstimo")
        print("2. Registrar Devolução")
        print("3. Listar Empréstimos Ativos")
        print("4. Listar Histórico de Empréstimos")
        print("5. Voltar ao Menu Principal")
        
        escolha = input("Escolha uma opção: ")

        if escolha == '1':
            listar_exemplares()
            numero_tombamento = solicitar_inteiro("Digite o número de tombamento do exemplar a ser emprestado: ")
            listar_usuarios()
            email_usuario = input("Digite o email do usuário que está pegando emprestado: ")
            
            data_emprestimo = date.today()
            print(f"Data de Empréstimo (padrão para hoje): {data_emprestimo.strftime('%Y-%m-%d')}")
            confirmar_data = input("Deseja usar outra data? (s/n): ").lower()
            if confirmar_data == 's':
                data_emprestimo = solicitar_data("Digite a data de empréstimo (AAAA-MM-DD): ") or data_emprestimo

            dias_emprestimo = solicitar_inteiro("Quantos dias de empréstimo? (ex: 14 para 14 dias): ")
            data_prevista_devolucao = data_emprestimo + timedelta(days=dias_emprestimo)
            print(f"Data Prevista de Devolução: {data_prevista_devolucao.strftime('%Y-%m-%d')}")

            registrar_emprestimo(numero_tombamento, email_usuario, data_emprestimo, data_prevista_devolucao)
        
        elif escolha == '2':
            listar_emprestimos(apenas_ativos=True)
            numero_tombamento = solicitar_inteiro("Digite o número de tombamento do exemplar a ser devolvido: ")
            email_usuario = input("Digite o email do usuário que devolveu: ")
            str_data_emprestimo_original = input("Digite a data original do empréstimo (AAAA-MM-DD) para identificação: ")
            data_emprestimo_original = date.fromisoformat(str_data_emprestimo_original)

            data_real_devolucao = date.today()
            print(f"Data Real de Devolução (padrão para hoje): {data_real_devolucao.strftime('%Y-%m-%d')}")
            confirmar_data = input("Deseja usar outra data? (s/n): ").lower()
            if confirmar_data == 's':
                data_real_devolucao = solicitar_data("Digite a data real de devolução (AAAA-MM-DD): ") or data_real_devolucao

            registrar_devolucao(numero_tombamento, email_usuario, data_emprestimo_original, data_real_devolucao)

        elif escolha == '3':
            listar_emprestimos(apenas_ativos=True)

        elif escolha == '4':
            listar_emprestimos(apenas_ativos=False)

        elif escolha == '5':
            break
        
        else:
            print("Opção inválida. Por favor, tente novamente.")

def menu_principal():
    while True:
        print("\n--- Sistema de Gerenciamento da Biblioteca ---")
        print("1. Gerenciar Autores")
        print("2. Gerenciar Editoras")
        print("3. Gerenciar Livros e Associações")
        print("4. Gerenciar Exemplares")
        print("5. Gerenciar Usuários")
        print("6. Gerenciar Empréstimos")
        print("7. Sair")
        
        escolha = input("Escolha uma opção: ")

        if escolha == '1':
            menu_autores()
        elif escolha == '2':
            menu_editoras()
        elif escolha == '3':
            menu_livros()
        elif escolha == '4':
            menu_exemplares()
        elif escolha == '5':
            menu_usuarios()
        elif escolha == '6':
            menu_emprestimos()
        elif escolha == '7':
            print("Saindo do programa. Até mais!")
            break
        else:
            print("Opção inválida. Por favor, tente novamente.")

if __name__ == "__main__":
    menu_principal()
