CREATE USER USERREP with replication encrypted password 'PASSREP';
SELECT pg_create_physical_replication_slot('replication_slot');

CREATE TABLE IF NOT EXISTS emails (
    id SERIAL PRIMARY KEY,
    email VARCHAR(100) NOT NULL
);
CREATE TABLE IF NOT EXISTS numbersphone (
    id SERIAL PRIMARY KEY,
    number VARCHAR(20) NOT NULL
);
INSERT INTO emails (email) VALUES ('RT@ta.ru');
INSERT INTO numbersphone (number) VALUES ('+78005557556');