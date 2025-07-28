-- Função para Auditoria de Devolução (trg_auditoria_devolucao_func)
CREATE OR REPLACE FUNCTION trg_auditoria_devolucao_func()
RETURNS TRIGGER AS $$
BEGIN
    -- Verifica se a Data_Dev_Real mudou de NULL para um valor
    IF OLD.Data_Dev_Real IS NULL AND NEW.Data_Dev_Real IS NOT NULL THEN
        INSERT INTO audit_devolucao (Num_Tombamento, Email, Data_Empre, Devolucao_anterior, Devolucao_nova)
        VALUES (OLD.Num_Tombamento, OLD.Email, OLD.Data_Empre, OLD.Data_Prev_Dev, NEW.Data_Dev_Real);
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger para Auditoria de Devolução
CREATE OR REPLACE TRIGGER trg_auditoria_devolucao
AFTER UPDATE OF Data_Dev_Real ON Emprestimo
FOR EACH ROW
EXECUTE FUNCTION trg_auditoria_devolucao_func();


-- Função para impedir a remoção de editoras com livros (trg_editora_com_livros_func)
CREATE OR REPLACE FUNCTION trg_editora_com_livros_func()
RETURNS TRIGGER AS $$
BEGIN
    IF EXISTS (SELECT 1 FROM Livro WHERE ID_Editora = OLD.ID_Editora) THEN
        RAISE EXCEPTION 'Não é possível remover editoras com livros cadastrados.';
    END IF;
    RETURN OLD;
END;
$$ LANGUAGE plpgsql;

-- Trigger para impedir a remoção de editoras com livros
CREATE OR REPLACE TRIGGER trg_editora_com_livros
BEFORE DELETE ON Editora
FOR EACH ROW
EXECUTE FUNCTION trg_editora_com_livros_func();


-- Função para ajustar a quantidade de exemplares do livro (trg_ajuste_quantidade_exemplar_func)
CREATE OR REPLACE FUNCTION trg_ajuste_quantidade_exemplar_func()
RETURNS TRIGGER AS $$
BEGIN
    -- Se um exemplar foi inserido
    IF TG_OP = 'INSERT' THEN
        UPDATE Livro
        SET Quantidade = Quantidade + 1
        WHERE ISBN = NEW.ISBN;
        RETURN NEW;
    -- Se um exemplar foi excluído
    ELSIF TG_OP = 'DELETE' THEN
        UPDATE Livro
        SET Quantidade = Quantidade - 1
        WHERE ISBN = OLD.ISBN;
        RETURN OLD;
    END IF;
    RETURN NULL; -- Não deveria chegar aqui
END;
$$ LANGUAGE plpgsql;

-- Trigger para ajustar a quantidade de exemplares após INSERT em Exemplar
CREATE OR REPLACE TRIGGER trg_ajuste_quantidade_exemplar_insert
AFTER INSERT ON Exemplar
FOR EACH ROW
EXECUTE FUNCTION trg_ajuste_quantidade_exemplar_func();

-- Trigger para ajustar a quantidade de exemplares após DELETE em Exemplar
CREATE OR REPLACE TRIGGER trg_ajuste_quantidade_exemplar_delete
AFTER DELETE ON Exemplar
FOR EACH ROW
EXECUTE FUNCTION trg_ajuste_quantidade_exemplar_func();


-- Função para verificar se o exemplar já está emprestado (trg_verifica_exemplar_emprestado_func)
CREATE OR REPLACE FUNCTION trg_verifica_exemplar_emprestado_func()
RETURNS TRIGGER AS $$
BEGIN
    -- Verifica se o exemplar que está sendo emprestado já possui um empréstimo ativo (Data_Dev_Real é NULL)
    IF EXISTS (SELECT 1 FROM Emprestimo WHERE Num_Tombamento = NEW.Num_Tombamento AND Data_Dev_Real IS NULL) THEN
        RAISE EXCEPTION 'Exemplar já está emprestado e não foi devolvido.';
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger para verificar se o exemplar já está emprestado antes de um novo empréstimo
CREATE OR REPLACE TRIGGER trg_verifica_exemplar_emprestado
BEFORE INSERT ON Emprestimo
FOR EACH ROW
EXECUTE FUNCTION trg_verifica_exemplar_emprestado_func();


-- Função para impedir a exclusão de um autor que possui livros (trg_impedir_exclusao_autor_func)
CREATE OR REPLACE FUNCTION trg_impedir_exclusao_autor_func()
RETURNS TRIGGER AS $$
BEGIN
    -- Verifica se o autor a ser excluído está associado a algum livro na tabela Escreve
    IF EXISTS (SELECT 1 FROM Escreve WHERE ID_Autor = OLD.ID) THEN
        RAISE EXCEPTION 'Autor possui livros vinculados e não pode ser excluído.';
    END IF;
    RETURN OLD;
END;
$$ LANGUAGE plpgsql;

-- Trigger para impedir a exclusão de um autor que possui livros
CREATE OR REPLACE TRIGGER trg_impedir_exclusao_autor
BEFORE DELETE ON Autor
FOR EACH ROW
EXECUTE FUNCTION trg_impedir_exclusao_autor_func();