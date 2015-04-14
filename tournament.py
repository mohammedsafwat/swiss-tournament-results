#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    db = psycopg2.connect("dbname=tournament")
    cursor = db.cursor()
    cursor.execute("DELETE * FROM matches")
    db.close()

def deletePlayers():
    """Remove all the player records from the database."""
    db = psycopg2.connect("dbname=tournament")
    cursor = db.cursor()
    cursor.execute("DELETE * FROM players")
    db.close()

def countPlayers():
    """Returns the number of players currently registered."""
    db = psycopg2.connect("dbname=tournament")
    cursor = db.cursor()
    cursor.execute("SELECT count(*) FROM players")
    result = cursor.fetchone()
    number_of_players = result[0]
    db.close()
    return number_of_players

def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    db = psycopg2.connect("dbname=tournament")
    cursor = db.cursor()
    cursor.execute("INSERT INTO players(player_name) values(%s)", (name,))
    db.commit()
    db.close()

def playerStandings():
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
    db = psycopg2.connect("dbname=tournament")
    cursor = db.cursor()
    #number of wins
    cursor.execute("SELECT count(*) as wins from players, matches WHERE players.player_id == matches.winner_id")
    #number of matches
    cursor.execute("SELECT count(*) as matches from players, matches WHERE players.player_id == matches.player1_id or players.player_id == matches.player2_id")

def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    db = psycopg2.connect("dbname=tournament")
    cursor = db.cursor()
    cursor.execute("INSERT INTO matches values(%s,%s,%s)", (winner, loser, winner))
    db.commit()
    db.close()
 
def swissPairings():
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

