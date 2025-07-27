import psycopg2

conn = psycopg2.connect(
    dbname="seu_banco",
    user="seu_usuario",
    password="sua_senha",
    host="localhost",
    port="5432"
)
cur = conn.cursor()

# Auditoria: registrar notas alteradas
cur.execute("""
    CREATE TABLE IF NOT EXISTS audit_nota (
        id_audit SERIAL PRIMARY KEY,
        ISBN VARCHAR(17),
        Email VARCHAR(250),
        Num_Tombamento INTEGER,
        Data_Empre DATE,
        Nota_anterior DECIMAL(3,1),
        Nota_nova DECIMAL(3,1),
        Data_Alteracao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
""")

cur.execute("""
    CREATE OR REPLACE FUNCTION registrar_auditoria_nota()
    RETURNS TRIGGER AS $$
    BEGIN
        IF OLD.Data_Dev_Real IS NOT DISTINCT FROM NEW.Data_Dev_Real THEN
            RETURN NEW;
        END IF;

        INSERT INTO audit_nota (
            ISBN, Email, Num_Tombamento, Data_Empre,
            Nota_anterior, Nota_nova
        )
        VALUES (
            NEW.Num_Tombamento, NEW.Email, NEW.Num_Tombamento, NEW.Data_Empre,
            OLD.Data_Dev_Real, NEW.Data_Dev_Real
        );
        RETURN NEW;
    END;
    $$ LANGUAGE plpgsql;
""")

cur.execute("""
    CREATE TRIGGER trg_auditoria_nota
    AFTER UPDATE ON Emprestimo
    FOR EACH ROW
    EXECUTE FUNCTION registrar_auditoria_nota();
""")

# Regras de negócio: impedir que uma editora seja removida se tiver livros
cur.execute("""
    CREATE OR REPLACE FUNCTION impedir_exclusao_editora_com_livros()
    RETURNS TRIGGER AS $$
    BEGIN
        IF EXISTS (
            SELECT 1 FROM Livro WHERE ID_Editora = OLD.ID_Editora
        ) THEN
            RAISE EXCEPTION 'Não é possível remover editoras com livros cadastrados.';
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

# Atualização derivada: ajustar quantidade de exemplares ao inserir ou deletar
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

conn.commit()
cur.close()
conn.close()