# -*- coding: utf-8 -*-
import psycopg2

try:
    conn = psycopg2.connect(
        dbname="biblioteca",
        user="postgres",
        password="sqltayllan",
        host="localhost",
        port="5432",
    )
    conn.set_client_encoding('UTF8')
except Exception as e:
    import traceback
    traceback.print_exc()

cur = conn.cursor()

# Auditoria: registrar alterações na data de devolução
cur.execute("""
    CREATE TABLE IF NOT EXISTS audit_devolucao (
        id_audit SERIAL PRIMARY KEY,
        Num_Tombamento INTEGER,
        Email VARCHAR(250),
        Data_Empre DATE,
        Devolucao_anterior DATE,
        Devolucao_nova DATE,
        Data_Alteracao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
""")

cur.execute("""
    CREATE OR REPLACE FUNCTION registrar_auditoria_devolucao()
    RETURNS TRIGGER AS $$
    BEGIN
        IF OLD.Data_Dev_Real IS DISTINCT FROM NEW.Data_Dev_Real THEN
            INSERT INTO audit_devolucao (
                Num_Tombamento, Email, Data_Empre,
                Devolucao_anterior, Devolucao_nova
            )
            VALUES (
                NEW.Num_Tombamento, NEW.Email, NEW.Data_Empre,
                OLD.Data_Dev_Real, NEW.Data_Dev_Real
            );
        END IF;
        RETURN NEW;
    END;
    $$ LANGUAGE plpgsql;
""")

cur.execute("""
    CREATE TRIGGER trg_auditoria_devolucao
    AFTER UPDATE ON Emprestimo
    FOR EACH ROW
    EXECUTE FUNCTION registrar_auditoria_devolucao();
""")

# Regras de negocio: impedir remoção de editora com livros
cur.execute("""
    CREATE OR REPLACE FUNCTION impedir_exclusao_editora_com_livros()
    RETURNS TRIGGER AS $$
    BEGIN
        IF EXISTS (
            SELECT 1 FROM Livro WHERE ID_Editora = OLD.ID_Editora
        ) THEN
            RAISE EXCEPTION 'Nao e possível remover editoras com livros cadastrados.';
        END IF;
        RETURN OLD;
    END;
    $$ LANGUAGE plpgsql;
""")

cur.execute("""
    CREATE TRIGGER trg_editora_com_livros
    BEFORE DELETE ON Editora
    FOR EACH ROW
    EXECUTE FUNCTION impedir_exclusao_editora_com_livros();
""")

# Atualizacao derivada: ajuste de quantidade de exemplares
cur.execute("""
    CREATE OR REPLACE FUNCTION ajustar_quantidade_livros()
    RETURNS TRIGGER AS $$
    BEGIN
        IF TG_OP = 'INSERT' THEN
            UPDATE Livro SET Quantidade = Quantidade + 1 WHERE ISBN = NEW.ISBN;
        ELSIF TG_OP = 'DELETE' THEN
            UPDATE Livro SET Quantidade = Quantidade - 1 WHERE ISBN = OLD.ISBN;
        END IF;
        RETURN NULL;
    END;
    $$ LANGUAGE plpgsql;
""")

cur.execute("""
    CREATE TRIGGER trg_ajuste_quantidade_exemplar
    AFTER INSERT OR DELETE ON Exemplar
    FOR EACH ROW
    EXECUTE FUNCTION ajustar_quantidade_livros();
""")




# Impedir empréstimo de exemplar já emprestado
cur.execute("""
    CREATE OR REPLACE FUNCTION fn_verifica_disponibilidade_exemplar()
    RETURNS TRIGGER AS $$
    BEGIN
        IF EXISTS (
            SELECT 1 FROM Emprestimo
            WHERE Num_Tombamento = NEW.Num_Tombamento
              AND Data_Dev_Real IS NULL
        ) THEN
            RAISE EXCEPTION 'Exemplar % ja esta emprestado e nao foi devolvido.', NEW.Num_Tombamento;
        END IF;
        RETURN NEW;
    END;
    $$ LANGUAGE plpgsql;
""")

cur.execute("""
    CREATE TRIGGER trg_verifica_exemplar_emprestado
    BEFORE INSERT ON Emprestimo
    FOR EACH ROW
    EXECUTE FUNCTION fn_verifica_disponibilidade_exemplar();
""")

# Impedir exclusão de Autor com livros cadastrados
cur.execute("""
    CREATE OR REPLACE FUNCTION fn_impedir_exclusao_autor()
    RETURNS TRIGGER AS $$
    BEGIN
        IF EXISTS (
            SELECT 1 FROM Escreve WHERE ID_Autor = OLD.ID
        ) THEN
            RAISE EXCEPTION 'Autor % possui livros vinculados e não pode ser excluído.', OLD.ID;
        END IF;
        RETURN OLD;
    END;
    $$ LANGUAGE plpgsql;
""")

cur.execute("""
    CREATE TRIGGER trg_impedir_exclusao_autor
    BEFORE DELETE ON Autor
    FOR EACH ROW
    EXECUTE FUNCTION fn_impedir_exclusao_autor();
""")


conn.commit()
cur.close()
conn.close()