#!/usr/bin/env python
#
# Test cases for tournament.py

import math
import random
from tournament import *

# Add contestant to compete in a tournament
contestant = (
    "Superman",
    "Batman",
    "Wonder Woman",
    "Flash",
    "Green Lantern",
    "Aquaman",
    "Atom",
    "Cycborg",
    "Shazman"
)
# Find how many ounds a tournament will last
findLog = math.log(len(contestant), 2)

totalRounds = math.ceil(findLog)


def addContestants(contestants, tournament):
    '''
    Create table for registered contestants
    '''
    if tournament is None or contestants is None:
        raise TypeError("Must have tournament name and contestants")
    for players in contestants:
        registerPlayer(players, tournament)
    playerStandings(tournament)
    print "Tournament %s with %s players will lasted %d rounds." % \
        (tournament, len(contestants), totalRounds)


def simtournament(contestants, tournament):
    '''
    This function is use to simulate a swiss pairing tournament.
    Take two arguments contestants which is a list of players and
    tournament which is the name of the tournament

    Returns: Tournament results listing first to last place
    '''
    addContestants(contestants, tournament)
    for x in range(0, int(totalRounds)):
        pairings = swissPairings(tournament)
        shuffle = ['w', 'l', 't']
        for pairs in pairings:
            random.shuffle(shuffle)
            reportMatch(pairs[0], pairs[2], shuffle[0])
    final = findtournament(tournament)
    print "Final Results"
    for position, standings in enumerate(final):
        print "%r. %s with %s pionts and record of %s - %s - %s omw %s" % \
         (position + 1, standings[1], standings[6], standings[2],
          standings[3], standings[4], standings[7],)

'''
Will simulate a tournament, change range number to change tournaments
simulated.
Will you wish to delete tournament after they are complete uncomment
deleteTournament().
'''
for tournament in ["Fake_Tournament_" + str(i) for i in range(1)]:
    simtournament(contestant, tournament)
    # deleteTournament(tournament)
