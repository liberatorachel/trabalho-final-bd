# Projeto Biblioteca - Sistema de Gerenciamento de Banco de Dados

## Descrição

Este projeto é um sistema para o gerenciamento completo de uma biblioteca, desenvolvido em Python com um robusto banco de dados PostgreSQL. Ele permite automatizar operações como o cadastro e a manutenção de autores, editoras, livros, exemplares e usuários, além de controlar o fluxo de empréstimos e devoluções.

O sistema foi concebido com foco na integridade dos dados, utilizando chaves primárias e estrangeiras, e aplicando triggers avançadas no PostgreSQL para reforçar regras de negócio (ex: impedir a remoção de editoras com livros vinculados, ou o empréstimo de exemplares já em uso). A conexão com o banco de dados é feita através da biblioteca psycopg2

---

## Estrutura do Projeto

A estrutura do projeto está organizada para facilitar a compreensão e a colaboração:

### Documentacao/
- `Relatorio_Sistema_Biblioteca.pdf` - Relatório detalhado do projeto.
- `Trabalho_Final___Banco_de_Dados.pdf` - Instruções originais do trabalho (opcional).

### Modelagem/
- `Diagrama_ER.png` - Diagrama Entidade-Relacionamento (ERD) do sistema.
- `Modelo_Relacional.jpg` - Imagem do Modelo Relacional do banco de dados.

### Scripts_SQL/
- `create_tables.sql` - Script SQL para criar o esquema do banco de dados e todas as tabelas.
- `create_triggers.sql` - Script SQL para criar as triggers e funções PL/pgSQL.

### Codigo_Fonte/
- `main.py` - Ponto de entrada principal da aplicação Python, com o menu de interação.
- `database/`
    - `connection.py` - Módulo para configuração e gestão da conexão com o PostgreSQL.
- `src/`
    - `models/` - Contém os módulos com as operações CRUD para cada entidade (autor, editora, livro, exemplar, usuário, empréstimo).
        - `autor_model.py`
        - `editora_model.py`
        - `livro_model.py`
        - `exemplar_model.py`
        - `usuario_model.py`
        - `emprestimo_model.py`
    - `menus.py` - Contém as funções para os menus de interação do usuário.
- `.venv/` - Ambiente virtual Python (gerado localmente).
- `requirements.txt` - Lista de dependências Python do projeto.


---

## Pré-requisitos

- Python 3.11 ou superior instalado  
- PostgreSQL instalado e configurado (com banco `biblioteca` criado)  
- Git instalado (para controle de versão e colaboração)

---

## Licença

Este projeto é para fins acadêmicos no curso de Fundamentos de Banco de Dados (2025.1).
