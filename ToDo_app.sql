CREATE DATABASE IF NOT EXISTS ToDo_app;
USE ToDo_app;

CREATE TABLE tasks (
	id int auto_increment primary key,
    nome varchar(100) not null,
    descricao text,
    prioridade enum('baixa', 'media', 'alta'),
    prazo date,
    status enum('pendente','andamento', 'concluida') default	'pendente'
);


INSERT INTO tasks (nome, descricao, prioridade, prazo, status)
VALUES ('Estudar Flask', 'Aprender rotas, banco de dados e API', 'alta', '2026-01-15', 'pendente');

select * from tasks;