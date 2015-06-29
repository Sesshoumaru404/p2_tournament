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


  conn = connect()
  c = conn.cursor()
  c.execute("SELECT * FROM players;")
  # print c.rowcount
  posts = c.rowcount
  conn.close()
  return posts

SELECT * from players;
