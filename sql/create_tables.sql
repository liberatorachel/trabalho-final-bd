-- Criação da tabela Editora
CREATE TABLE IF NOT EXISTS Editora (
    ID_Editora SERIAL PRIMARY KEY,
    Nome VARCHAR(255) NOT NULL,
    Endereco VARCHAR(255),
    Telefone VARCHAR(20),
    Email VARCHAR(255) UNIQUE,
    CNPJ VARCHAR(18) UNIQUE
);

-- Criação da tabela Autor
CREATE TABLE IF NOT EXISTS Autor (
    ID SERIAL PRIMARY KEY,
    Nome VARCHAR(255) NOT NULL,
    Nacionalidade VARCHAR(100),
    Data_Nascimento DATE
);

-- Criação da tabela Livro
CREATE TABLE IF NOT EXISTS Livro (
    ISBN VARCHAR(20) PRIMARY KEY,
    Titulo VARCHAR(255) NOT NULL,
    Ano_Publi INTEGER,
    Quantidade INTEGER DEFAULT 0, -- Quantidade de exemplares, será atualizada por trigger
    ID_Editora INTEGER REFERENCES Editora(ID_Editora) ON DELETE RESTRICT
);

-- Tabela associativa entre Livro e Autor (Muitos para Muitos)
CREATE TABLE IF NOT EXISTS Escreve (
    ID_Autor INTEGER REFERENCES Autor(ID) ON DELETE CASCADE,
    ISBN VARCHAR(20) REFERENCES Livro(ISBN) ON DELETE CASCADE,
    PRIMARY KEY (ID_Autor, ISBN)
);

-- Criação da tabela Exemplar
CREATE TABLE IF NOT EXISTS Exemplar (
    Num_Tombamento SERIAL PRIMARY KEY,
    Num_Prateleira VARCHAR(50),
    ISBN VARCHAR(20) REFERENCES Livro(ISBN) ON DELETE CASCADE
);

-- Criação da tabela Usuario
CREATE TABLE IF NOT EXISTS Usuario (
    Email VARCHAR(255) PRIMARY KEY,
    Nome VARCHAR(255) NOT NULL,
    Idade INTEGER,
    Data_Nasc DATE
);

-- Criação da tabela Emprestimo
CREATE TABLE IF NOT EXISTS Emprestimo (
    Num_Tombamento INTEGER REFERENCES Exemplar(Num_Tombamento) ON DELETE RESTRICT,
    Email VARCHAR(255) REFERENCES Usuario(Email) ON DELETE RESTRICT,
    Data_Empre DATE NOT NULL DEFAULT CURRENT_DATE,
    Data_Prev_Dev DATE NOT NULL,
    Data_Dev_Real DATE, -- Pode ser NULL se ainda não foi devolvido
    PRIMARY KEY (Num_Tombamento, Email, Data_Empre) -- Chave composta para empréstimos únicos
);

-- Criação da tabela de Auditoria de Devolução
CREATE TABLE IF NOT EXISTS audit_devolucao (
    id_audit SERIAL PRIMARY KEY,
    Num_Tombamento INTEGER,
    Email VARCHAR(255),
    Data_Empre DATE,
    Devolucao_anterior DATE,
    Devolucao_nova DATE,
    Data_Alteracao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


