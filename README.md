# Projeto Biblioteca - Sistema de Gerenciamento de Banco de Dados

## Descrição

Este projeto é um sistema simples para gerenciamento de dados de uma biblioteca, desenvolvido em Python com banco de dados PostgreSQL.  
Ele permite inserir, atualizar, remover e listar livros, conectando-se ao banco via `psycopg2`.

---

## Estrutura do projeto

- `src/conexao.py` - código para conexão com o banco PostgreSQL  
- `src/testeconexao.py` - script de teste para validar conexão  
- `.venv/` - ambiente virtual Python  
- `requirements.txt` - dependências do projeto  
- Outros arquivos do sistema (a serem desenvolvidos)

---

## Pré-requisitos

- Python 3.11 ou superior instalado  
- PostgreSQL instalado e configurado (com banco `biblioteca` criado)  
- Git instalado (para controle de versão e colaboração)

---

## Configuração inicial para colaboradores

### 1. Clonar o repositório

```
git clone https://github.com/seu-usuario/trabalho-final-bd.git
cd trabalho-final-bd
```

### 2. Criar e ativar ambiente virtual

No Windows (PowerShell):

```
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

```
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Instalar dependências

```
pip install -r requirements.txt
```

### 4. Configurar conexão com banco

No arquivo `src/conexao.py`, alterar os parâmetros:

```python
dbname="biblioteca"
user="postgres"
password="sua_senha_aqui"
host="localhost"
port="5432"
```

---

## Como executar

Para testar a conexão com o banco de dados, rode:

```
python src/testeconexao.py
```

Se a conexão for bem-sucedida, verá mensagens de sucesso.

---

## Fluxo de trabalho colaborativo

- Cada membro deve criar uma branch para desenvolver suas funcionalidades  
- Fazer commits frequentes e criar pull requests para a branch principal `main`  
- Revisar código e fazer merge após aprovação  

---

## Licença

Este projeto é para fins acadêmicos no curso de Fundamentos de Banco de Dados (2025.1).
