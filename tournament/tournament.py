#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=p2_tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    conn = connect()
    c = conn.cursor()
    c.execute("DELETE FROM matches;")
    conn.commit()
    conn.close()


def deletePlayers(tournament):
    """Remove all the player records from the database."""
    conn = connect()
    c = conn.cursor()
    c.execute("DELETE FROM players WHERE tournament = %s;", (tournament,))
    conn.commit()
    conn.close()

def countPlayers():
    """Returns the number of players currently registered."""
    conn = connect()
    c = conn.cursor()
    c.execute("SELECT * FROM players;")
    # print c.rowcount
    posts = c.rowcount
    print 'Total player count %s' % posts
    conn.close()
    return posts


def registerPlayer(name, tournament):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name: the player's full name (need not be unique).
    """
    conn = connect()
    c = conn.cursor()
    c.execute("INSERT INTO players (name, tournament) VALUES (%s, %s)" , (name,tournament,))
    conn.commit()
    conn.close()


def playerStandings(tournament):
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    createT = "CREATE VIEW %s AS SELECT * FROM standings WHERE tournament = '%s';" % (tournament, tournament,)
    test2 = "SELECT * FROM %s;" % tournament
    conn = connect()
    c = conn.cursor()
    c.execute(createT)
    c.execute(test2)
    posts = c.fetchall()
    conn.commit()
    conn.close()
    return posts

def findtournament(tournament):
    test2 = "SELECT * FROM %s;" % tournament
    conn = connect()
    c = conn.cursor()
    c.execute(test2)
    posts = c.fetchall()
    conn.close()
    return posts

def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    # Set opponent to null value if in bye round
    if loser == "bye":
        loser = None
    conn = connect()
    c = conn.cursor()
    c.execute("INSERT INTO matches VALUES (%s,%s,%s);", (winner,loser,winner))
    conn.commit()
    conn.close()

# reportMatch(2, 1)
# UPDATE standings SET wins = wins + 1 WHERE standings.id = (%s);

def swissPairings(tournament):
    """Returns a list of pairs of players for the next round of a match.

    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.

    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    test2 = "SELECT * FROM %s;" % tournament
    tuples = ()
    conn = connect()
    c = conn.cursor()
    c.execute(test2)
    standings = c.fetchall()
    for x in range(0, len(standings)):
        if (x % 2 != 0):
            continue
        player = standings[x]
        if (x % 2 == 0):
            if (x+1) < len(standings):
                player2 = standings[x+1]
            else:
                player2 = ("bye", "bye",)
        tuples = tuples + ((player[0], player[1],player2[0], player2[1],),)
    conn.close()
    return tuples

def clearTournament(tournament):
    """Use to remove a tournament from database"""
    delStatemant = "DROP VIEW IF EXISTS %s CASCADE;" %tournament
    delPlayer = "DELETE FROM players CASCADE WHERE tournament = '%s';" %tournament
    conn = connect()
    c = conn.cursor()
    c.execute(delStatemant)
    c.execute(delPlayer)
    conn.commit()
    conn.close()
