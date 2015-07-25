-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

-- use "\i tournament.sql" in psql terminal to read file

CREATE DATABASE p2_tournament;

\c p2_tournament;

DROP TABLE IF EXISTS players CASCADE;
DROP TABLE IF EXISTS matches CASCADE;

-- Create table for players includes name and tournament name

CREATE TABLE PLAYERS (
    name text NOT NULL,
    tournament text,
    id serial PRIMARY KEY
);


-- Create a Matches table to track games played includes
-- contestant their opponent and the result of match and points earns

CREATE TABLE MATCHES (
    contestant integer REFERENCES players (id) ON DELETE CASCADE,
    opponent integer REFERENCES players (id) ON DELETE CASCADE,
    result text CHECK (result IN ('w', 'l', 't')),
    points integer DEFAULT 0,
    match_id serial PRIMARY KEY,
		UNIQUE (contestant, opponent)
);

-- Games table find having it seperate is easier to read

CREATE VIEW GAMES AS (
  SELECT id,
    count(case when results = 'w' then 1 end) as wins,
    count(case when results = 't' then 1 end) as ties,
    count(case when results = 'l' then 1 end) as loses,
    sum(pionts) as points,
    count(results) as played
  FROM (
    SELECT players.id,
      matches.result as results,
      matches.contestant,
      matches.points as pionts
    FROM PLAYERS LEFT JOIN MATCHES
    ON players.id = matches.contestant
  ) s GROUP BY id
);

-- View that first gets a table of opponent wins, then that table is
-- grouped by contestants to get there opponent matches wins(OMW)

CREATE VIEW OMW AS (
  SELECT
    contestant as id,
    sum(wins) as wins
  FROM (
    SELECT
      matches.opponent,
      matches.contestant,
      games.wins
    FROM MATCHES LEFT JOIN GAMES
    ON matches.opponent = games.id
  ) s GROUP BY contestant
);

-- Standings of all players in all tournament sorted by points then omw

CREATE VIEW standings AS (
  SELECT
    players.id,
    players.name,
    games.wins,
    games.ties,
    games.loses,
    games.played,
    games.points,
    omw.wins as omw,
    players.tournament
  FROM PLAYERS
    INNER JOIN GAMES USING (id)
    LEFT JOIN OMW using (id)
  ORDER BY points DESC, omw DESC
);
