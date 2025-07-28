from schemas import criar_estrutura_banco # Para criar tabelas e triggers
from utils import solicitar_data, solicitar_inteiro # Funções auxiliares

# Importa as funções CRUD de cada módulo de modelo
from models.autor_model import (
    inserir_autor, listar_autores, atualizar_autor, remover_autor
)
from models.editora_model import (
    inserir_editora, listar_editoras, atualizar_editora, remover_editora
)
from models.livro_model import (
    inserir_livro, listar_livros, atualizar_livro, remover_livro,
    associar_autor_livro, desassociar_autor_livro, listar_livros_por_autor,
    listar_autores_por_livro
)
from models.exemplar_model import (
    inserir_exemplar, listar_exemplares, atualizar_exemplar, remover_exemplar
)
from models.usuario_model import (
    inserir_usuario, listar_usuarios, atualizar_usuario, remover_usuario
)
from models.emprestimo_model import (
    registrar_emprestimo, registrar_devolucao, listar_emprestimos,
    listar_emprestimos_atrasados, contar_exemplares_disponiveis,
    listar_exemplares_disponiveis_por_livro
)

def menu_autores():
    while True:
        print("\n--- Gerenciar Autores ---")
        print("1. Inserir Autor")
        print("2. Listar Autores")
        print("3. Atualizar Autor")
        print("4. Remover Autor")
        print("5. Voltar ao Menu Principal")
        
        escolha = input("Escolha uma opção: ")

        if escolha == '1':
            nome = input("Nome do autor: ")
            nacionalidade = input("Nacionalidade: ")
            data_nascimento = solicitar_data("Data de Nascimento (AAAA-MM-DD): ")
            if data_nascimento:
                inserir_autor(nome, nacionalidade, data_nascimento)
        elif escolha == '2':
            listar_autores()
        elif escolha == '3':
            id_autor = solicitar_inteiro("ID do autor a ser atualizado: ")
            if id_autor is not None:
                novo_nome = input("Novo Nome: ")
                nova_nacionalidade = input("Nova Nacionalidade: ")
                nova_data_nascimento = solicitar_data("Nova Data de Nascimento (AAAA-MM-DD): ")
                if nova_data_nascimento:
                    atualizar_autor(id_autor, novo_nome, nova_nacionalidade, nova_data_nascimento)
        elif escolha == '4':
            id_autor = solicitar_inteiro("ID do autor a ser removido: ")
            if id_autor is not None:
                remover_autor(id_autor)
        elif escolha == '5':
            break
        else:
            print("Opção inválida. Por favor, tente novamente.")

def menu_editoras():
    while True:
        print("\n--- Gerenciar Editoras ---")
        print("1. Inserir Editora")
        print("2. Listar Editoras")
        print("3. Atualizar Editora")
        print("4. Remover Editora")
        print("5. Voltar ao Menu Principal")
        
        escolha = input("Escolha uma opção: ")

        if escolha == '1':
            nome = input("Nome da editora: ")
            endereco = input("Endereço: ")
            telefone = input("Telefone: ")
            email = input("Email: ")
            cnpj = input("CNPJ: ")
            inserir_editora(nome, endereco, telefone, email, cnpj)
        elif escolha == '2':
            listar_editoras()
        elif escolha == '3':
            id_editora = solicitar_inteiro("ID da editora a ser atualizada: ")
            if id_editora is not None:
                novo_nome = input("Novo Nome: ")
                novo_endereco = input("Novo Endereço: ")
                novo_telefone = input("Novo Telefone: ")
                novo_email = input("Novo Email: ")
                novo_cnpj = input("Novo CNPJ: ")
                atualizar_editora(id_editora, novo_nome, novo_endereco, novo_telefone, novo_email, novo_cnpj)
        elif escolha == '4':
            id_editora = solicitar_inteiro("ID da editora a ser removida: ")
            if id_editora is not None:
                remover_editora(id_editora)
        elif escolha == '5':
            break
        else:
            print("Opção inválida. Por favor, tente novamente.")

def menu_livros():
    while True:
        print("\n--- Gerenciar Livros e Associações ---")
        print("1. Inserir Livro")
        print("2. Listar Livros")
        print("3. Atualizar Livro")
        print("4. Remover Livro")
        print("5. Associar Autor a Livro")
        print("6. Desassociar Autor de Livro")
        print("7. Listar Livros por Autor")
        print("8. Listar Autores por Livro")
        print("9. Voltar ao Menu Principal")
        
        escolha = input("Escolha uma opção: ")

        if escolha == '1':
            isbn = input("ISBN do livro: ")
            titulo = input("Título: ")
            ano_publi = solicitar_inteiro("Ano de Publicação: ")
            id_editora = solicitar_inteiro("ID da Editora: ")
            if ano_publi is not None and id_editora is not None:
                inserir_livro(isbn, titulo, ano_publi, id_editora)
        elif escolha == '2':
            listar_livros()
        elif escolha == '3':
            isbn = input("ISBN do livro a ser atualizado: ")
            novo_titulo = input("Novo Título: ")
            novo_ano_publi = solicitar_inteiro("Novo Ano de Publicação: ")
            novo_id_editora = solicitar_inteiro("Novo ID da Editora: ")
            if novo_ano_publi is not None and novo_id_editora is not None:
                atualizar_livro(isbn, novo_titulo, novo_ano_publi, novo_id_editora)
        elif escolha == '4':
            isbn = input("ISBN do livro a ser removido: ")
            remover_livro(isbn)
        elif escolha == '5':
            id_autor = solicitar_inteiro("ID do Autor a associar: ")
            isbn = input("ISBN do Livro: ")
            if id_autor is not None:
                associar_autor_livro(id_autor, isbn)
        elif escolha == '6':
            id_autor = solicitar_inteiro("ID do Autor a desassociar: ")
            isbn = input("ISBN do Livro: ")
            if id_autor is not None:
                desassociar_autor_livro(id_autor, isbn)
        elif escolha == '7':
            id_autor = solicitar_inteiro("ID do Autor para listar livros: ")
            if id_autor is not None:
                listar_livros_por_autor(id_autor)
        elif escolha == '8':
            isbn = input("ISBN do Livro para listar autores: ")
            listar_autores_por_livro(isbn)
        elif escolha == '9':
            break
        else:
            print("Opção inválida. Por favor, tente novamente.")

def menu_exemplares():
    while True:
        print("\n--- Gerenciar Exemplares ---")
        print("1. Inserir Exemplar")
        print("2. Listar Exemplares")
        print("3. Atualizar Exemplar")
        print("4. Remover Exemplar")
        print("5. Contar Exemplares Disponíveis por Livro")
        print("6. Listar Exemplares Disponíveis por Livro")
        print("7. Voltar ao Menu Principal")
        
        escolha = input("Escolha uma opção: ")

        if escolha == '1':
            isbn = input("ISBN do Livro ao qual o exemplar pertence: ")
            num_prateleira = input("Número da Prateleira: ")
            inserir_exemplar(isbn, num_prateleira)
        elif escolha == '2':
            listar_exemplares()
        elif escolha == '3':
            num_tombamento = solicitar_inteiro("Número de Tombamento do exemplar a ser atualizado: ")
            if num_tombamento is not None:
                novo_num_prateleira = input("Novo Número da Prateleira: ")
                novo_isbn = input("Novo ISBN do Livro: ")
                atualizar_exemplar(num_tombamento, novo_num_prateleira, novo_isbn)
        elif escolha == '4':
            num_tombamento = solicitar_inteiro("Número de Tombamento do exemplar a ser removido: ")
            if num_tombamento is not None:
                remover_exemplar(num_tombamento)
        elif escolha == '5':
            isbn = input("ISBN do Livro para contar exemplares disponíveis: ")
            contar_exemplares_disponiveis(isbn)
        elif escolha == '6':
            isbn = input("ISBN do Livro para listar exemplares disponíveis: ")
            listar_exemplares_disponiveis_por_livro(isbn)
        elif escolha == '7':
            break
        else:
            print("Opção inválida. Por favor, tente novamente.")

def menu_usuarios():
    while True:
        print("\n--- Gerenciar Usuários ---")
        print("1. Inserir Usuário")
        print("2. Listar Usuários")
        print("3. Atualizar Usuário")
        print("4. Remover Usuário")
        print("5. Voltar ao Menu Principal")
        
        escolha = input("Escolha uma opção: ")

        if escolha == '1':
            email = input("Email do usuário: ")
            nome = input("Nome completo: ")
            idade = solicitar_inteiro("Idade: ")
            data_nasc = solicitar_data("Data de Nascimento (AAAA-MM-DD): ")
            if idade is not None and data_nasc:
                inserir_usuario(email, nome, idade, data_nasc)
        elif escolha == '2':
            listar_usuarios()
        elif escolha == '3':
            email = input("Email do usuário a ser atualizado: ")
            novo_nome = input("Novo Nome completo: ")
            nova_idade = solicitar_inteiro("Nova Idade: ")
            nova_data_nasc = solicitar_data("Nova Data de Nascimento (AAAA-MM-DD): ")
            if nova_idade is not None and nova_data_nasc:
                atualizar_usuario(email, novo_nome, nova_idade, nova_data_nasc)
        elif escolha == '4':
            email = input("Email do usuário a ser removido: ")
            remover_usuario(email)
        elif escolha == '5':
            break
        else:
            print("Opção inválida. Por favor, tente novamente.")

def menu_emprestimos():
    while True:
        print("\n--- Gerenciar Empréstimos ---")
        print("1. Registrar Novo Empréstimo")
        print("2. Registrar Devolução")
        print("3. Listar Empréstimos Ativos")
        print("4. Listar Todos os Empréstimos")
        print("5. Listar Empréstimos Atrasados")
        print("6. Listar Empréstimos por Usuário")
        print("7. Listar Empréstimos por Exemplar")
        print("8. Voltar ao Menu Principal")
        
        escolha = input("Escolha uma opção: ")

        if escolha == '1':
            num_tombamento = solicitar_inteiro("Número de Tombamento do exemplar: ")
            email_usuario = input("Email do usuário: ")
            data_prev_dev = solicitar_data("Data Prevista de Devolução (AAAA-MM-DD): ")
            if num_tombamento is not None and data_prev_dev:
                registrar_emprestimo(num_tombamento, email_usuario, data_prev_dev)
        elif escolha == '2':
            num_tombamento = solicitar_inteiro("Número de Tombamento do exemplar: ")
            email_usuario = input("Email do usuário: ")
            data_emprestimo_original = solicitar_data("Data do Empréstimo Original (AAAA-MM-DD): ")
            data_real_devolucao = solicitar_data("Data Real de Devolução (AAAA-MM-DD, deixe em branco para data atual): ")
            if num_tombamento is not None and data_emprestimo_original:
                registrar_devolucao(num_tombamento, email_usuario, data_emprestimo_original, data_real_devolucao)
        elif escolha == '3':
            listar_emprestimos(apenas_ativos=True)
        elif escolha == '4':
            listar_emprestimos(apenas_ativos=False)
        elif escolha == '5':
            listar_emprestimos_atrasados()
        elif escolha == '6':
            email_usuario = input("Email do usuário para listar empréstimos: ")
            listar_emprestimos(email_usuario=email_usuario)
        elif escolha == '7':
            num_tombamento = solicitar_inteiro("Número de Tombamento do exemplar para listar empréstimos: ")
            if num_tombamento is not None:
                listar_emprestimos(num_tombamento=num_tombamento)
        elif escolha == '8':
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
    # Garante que as tabelas e triggers sejam criadas/verificadas ao iniciar o sistema
    criar_estrutura_banco()
    # Inicia o menu principal
    menu_principal()