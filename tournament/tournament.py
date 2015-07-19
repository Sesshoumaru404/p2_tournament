#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2
import math

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
    c.execute("INSERT INTO players (name, tournament) VALUES (%s, %s)",
              (name, tournament,))
    conn.commit()
    conn.close()


def playerStandings(tournament):
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a
    player tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    x = "CREATE VIEW %s AS SELECT * FROM standings WHERE tournament = '%s';"
    tableCreate = x % (tournament, tournament,)
    loadTable = "SELECT * FROM %s;" % tournament
    conn = connect()
    c = conn.cursor()
    c.execute(tableCreate)
    c.execute(loadTable)
    table = c.fetchall()
    conn.commit()
    conn.close()
    return table


def findtournament(tournament):
    test2 = "SELECT * FROM %s;" % tournament
    conn = connect()
    c = conn.cursor()
    c.execute(test2)
    posts = c.fetchall()
    conn.close()
    return posts


def checkrematch(id1, id2):
    """
    Use to check if players have already played if other
    """
    if id2 == "bye":
        findMatch = "SELECT * FROM matches where contestant = %s " \
            " and opponent IS NULL;" % (id1,)
    else:
        findMatch = "SELECT * FROM matches where contestant = %s " \
            " and opponent = %s;" % (id1, id2,)
    conn = connect()
    c = conn.cursor()
    c.execute(findMatch)
    match = c.fetchall()
    conn.close()
    return len(match) == 1


def reportMatch(contestant, opponent, result):
    """
    Records the outcome of a single match between two players.
    Reads as contestant faced opponent and result was

    Args:
      contestant:  the id number of the player who won
      opponent:  the id number of the player who lost
      result: result of the match
    """
    if result == 'w':
        contestantPoints = 3
        contestantResult = 'w'
        opponentResult = 'l'
        opponentPoints = 0
    if result == 'l':
        contestantResult = 'l'
        contestantPoints = 0
        opponentResult = 'w'
        opponentPoints = 3
    if result == 't':
        contestantResult = 't'
        contestantPoints = 1
        opponentResult = 't'
        opponentPoints = 1
    conn = connect()
    c = conn.cursor()
    # Set opponent to null value if in bye round
    if opponent == "bye":
        c.execute("INSERT INTO matches VALUES (%s,%s,%s,%s);", (contestant,
                                                                None,
                                                                result, 1),)
    else:
        c.execute("INSERT INTO matches VALUES (%s,%s,%s,%s);", (contestant,
                                                                opponent,
                                                                contestantResult,
                                                                contestantPoints),)
        c.execute("INSERT INTO matches VALUES (%s,%s,%s,%s);", (opponent,
                                                                contestant,
                                                                opponentResult,
                                                                opponentPoints),)
    conn.commit()
    conn.close()


def swissPairings(tournament):
    """
    Returns a list of pairs of players for the next round of a match.

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
    played = "SELECT opponent FROM matches where contestant = %s ;" % tournament
    tuples = ()
    playerPool = []
    conn = connect()
    c = conn.cursor()
    c.execute(test2)
    playerPool = c.fetchall()
    rounds = math.ceil(len(playerPool)/float(2))
    for x in range(0, int(rounds)):
        i = 1
        # Check for bye rematches
        #
        # if  not checkrematch(playerPool[lastPlayer][0], "bye"):
        #     print "played bye"
        #     player  = playerPool[playerPool[lastPlayer]]
        #     player2  = playerPool[playerPool[lastPlayer]-1]
        if checkrematch(playerPool[-1][0], "bye"):
            player = playerPool[-1]
            player2 = playerPool[-2]
            tuples = tuples + ((player[0], player[1], player2[0], player2[1],),)
            del playerPool[-1]
            del playerPool[-1]
        else:
            if len(playerPool) == 1:
                player  = playerPool[0]
                player2 = ("bye", "bye",)
                tuples = tuples + ((player[0], player[1], player2[0], player2[1],),)
                break
            else:
                player = playerPool[0]
                del playerPool[0]
                # print player
                player2 = playerPool[0]
                while checkrematch(player[0], player2[0]):
                    for index, player in enumerate(playerPool):
                        player2 = playerPool[index + 1]
                playerPool.remove(player2)
                tuples = tuples + ((player[0], player[1], player2[0], player2[1],),)

    conn.close()
    return tuples



def clearTournament(tournament):
    """
    Use to remove a tournament  and player in that specfic tournament
    from database
    """
    delTournament = "DROP VIEW IF EXISTS %s CASCADE;" % tournament
    delP = "DELETE FROM players CASCADE WHERE tournament = '%s';" % tournament
    conn = connect()
    c = conn.cursor()
    c.execute(delTournament)
    c.execute(delP)
    conn.commit()
    conn.close()
