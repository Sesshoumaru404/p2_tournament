-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

-- use in psql to \i tournament.sql of read file

CREATE DATABASE p2_tournament;

\c p2_tournament;

CREATE TABLE players (
    name text,
    id serial PRIMARY KEY
);

-- Setup table for all matches
CREATE TABLE matches (
    name text,
    match_id serial PRIMARY KEY
);

-- Setup table for all standings
CREATE TABLE standings (
    id serial REFERENCES players (id),
    name text,
    wins int DEFAULT 0,
    matches int DEFAULT 0
);

CREATE OR REPLACE FUNCTION process_standings() RETURNS TRIGGER AS $standings$
    BEGIN
        --
        -- Create a row in emp_audit to reflect the operation performed on emp,
        -- make use of the special variable TG_OP to work out the operation.
        --
        IF (TG_OP = 'INSERT') THEN
            INSERT INTO standings SELECT NEW.id, NEW.name;
            RETURN NEW;
        END IF;
        RETURN NULL; -- result is ignored since this is an AFTER trigger
    END;
$standings$ LANGUAGE plpgsql;

CREATE TRIGGER standings
AFTER INSERT ON players
    FOR EACH ROW EXECUTE PROCEDURE process_standings();

SELECT * from standings;
