#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2
from itertools import chain

DBNAME = 'tournament'

def connect(dbname=DBNAME):
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect('dbname=' + dbname)


def deleteMatches():
    """Remove all the match records from the database."""
    db = connect()
    cursor = db.cursor()
    cursor.execute("DELETE FROM matches")
    db.commit()
    db.close()


def deletePlayers():
    """Remove all the player records from the database."""
    db = connect()
    cursor = db.cursor()
    cursor.execute("DELETE FROM players")
    db.commit()
    db.close()


def countPlayers():
    """Returns the number of players currently registered."""
    db = connect()
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
    db = connect()
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
    db = connect()
    cursor = db.cursor()
    # number of wins
    number_of_wins_query = """
    CREATE VIEW winners as SELECT players.player_id, players.player_name, count(matches.match_id) AS number_of_wins FROM
    players LEFT JOIN matches ON players.player_id = matches.winner_id GROUP BY players.player_id
    ORDER BY number_of_wins DESC
    """
    cursor.execute(number_of_wins_query)

    # number of losses
    number_of_losses_query = """
    CREATE VIEW losers as SELECT players.player_id, players.player_name, count(matches.match_id) AS number_of_losses
    FROM players LEFT JOIN matches ON players.player_id = matches.loser_id GROUP BY players.player_id
    ORDER BY number_of_losses DESC
    """
    cursor.execute(number_of_losses_query)

    # player standings
    player_standings_query = """
    SELECT winners.player_id AS id, winners.player_name AS name, winners.number_of_wins AS wins,
    number_of_wins+number_of_losses AS matches FROM winners LEFT JOIN losers ON winners.player_id = losers.player_id
    """
    cursor.execute(player_standings_query)
    player_standings = cursor.fetchall()
    db.close()
    return player_standings


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    db = connect()
    cursor = db.cursor()
    cursor.execute("INSERT INTO matches(winner_id, loser_id) values(%s,%s)", (winner, loser))
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
    standings = [(record[0], record[1]) for record in playerStandings()]

    if len(standings) < 2:
        raise ValueError("Not Enough Players")
    left = standings[0::2]
    right = standings[1::2]
    pairings = zip(left, right)
    results = []
    for pairing in pairings:
        pairing = chain(*pairing)
        results.append(pairing)
    return results


