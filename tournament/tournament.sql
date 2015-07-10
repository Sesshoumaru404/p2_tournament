-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

-- use in psql to \i tournament.sql of read file

-- DROP DATABASE IF EXISTS p2_tournament;
CREATE DATABASE p2_tournament;

\c p2_tournament;

CREATE TABLE players (
    name text,
    id serial PRIMARY KEY
);

-- Setup table for all matches
-- id1, name1, id2, name2
CREATE TABLE matches (
    id1 integer REFERENCES players (id),
    id2 integer REFERENCES players (id),
    match_id serial PRIMARY KEY,
		UNIQUE   (id1, id2)
);

CREATE VIEW standings AS (
  SELECT ID, NAME
  FROM PLAYERS
);

SELECT * from standings;
