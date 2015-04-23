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

def deleteTournaments():
    """Delete all tournaments from database."""
    db = connect()
    cursor = db.cursor()
    cursor.execute("DELETE FROM tournaments")
    db.commit()
    db.close()

def deleteMatches(tournament=None):
    """
    If a tournament id is passed, delete that tournament's matches,
    else, remove all the match records from the database.
    """
    db = connect()
    cursor = db.cursor()
    if tournament:
        cursor.execute("DELETE FROM matches WHERE tournament_id=(%s)", (tournament,))
    else:
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

def createTournament(name):
    """Create a new tournament"""
    db = connect()
    cursor = db.cursor()
    cursor.execute("INSERT INTO tournaments(tournament_name) VALUES(%s) RETURNING tournament_id", (name,))
    row_id = cursor.fetchone()[0]
    db.commit()
    db.close()
    return row_id

def addPlayerToTournament(player_id, tournament):
    """Add a player to a specific tournament"""
    db = connect()
    cursor = db.cursor()
    cursor.execute("INSERT INTO players_in_tournament(player_id, tournament_id) VALUES(%s, %s)",
                   (player_id, tournament))
    db.commit()
    db.close()

def countPlayers(tournament=None):
    """
    if a tournament id is passed, count the number of players added to this tournament,
    else return the all number of players currently registered.
    """
    db = connect()
    cursor = db.cursor()
    if tournament:
        # Create a view to get the number of players in each tournament
        number_of_players_for_all_tournaments_query = """
        CREATE VIEW players_per_tournament AS SELECT tournaments.tournament_id AS tournament_id,
        COUNT(players_in_tournaments.player_id) AS players_number
        FROM tournaments LEFT JOIN players_in_tournaments
        ON tournaments.tournament_id = players_in_tournaments.tournament_id
        GROUP BY tournaments.tournament_id
        """
        cursor.execute(number_of_players_for_all_tournaments_query)
        # Get number of players from this specific tournament
        number_of_players_for_specific_tournament_query = """
        SELECT players_number FROM players_per_tournament WHERE tournament_id=(%s)"
        """
        cursor.execute(number_of_players_for_specific_tournament_query, (tournament,))
    else:
        cursor.execute("SELECT COUNT(*) FROM players")
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
    cursor.execute("INSERT INTO players(player_name) VALUES(%s) RETURNING player_id", (name,))
    row_id = cursor.fetchone()[0]
    db.commit()
    db.close()
    return row_id


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
    db = connect()
    cursor = db.cursor()
    # number of wins
    number_of_wins_query = """
    CREATE VIEW winners AS
    SELECT players.player_id, players.player_name, COUNT(matches.match_id) AS number_of_wins,
    players_in_tournaments.tournament_id AS tournament_id
    FROM players
    LEFT JOIN players_in_tournaments ON players.player_id = players_in_tournaments.player_id
    LEFT JOIN matches ON players.player_id = matches.winner_id
    AND
    players_in_tournaments.tournament_id = matches.tournament_id
    GROUP BY players.player_id, players_in_tournaments.tournament_id
    ORDER BY number_of_wins DESC
    """
    cursor.execute(number_of_wins_query)

    # number of losses
    number_of_losses_query = """
    CREATE VIEW losers AS
    SELECT players.player_id, players.player_name, COUNT(matches.match_id) AS number_of_losses,
    players_in_tournaments.tournament_id AS tournament_id
    FROM players
    LEFT JOIN players_in_tournaments ON players.player_id = players_in_tournaments.player_id
    LEFT JOIN matches ON players.player_id = matches.loser_id
    AND
    players_in_tournaments.tournament_id = matches.tournament_id
    GROUP BY players.player_id, players_in_tournaments.tournament_id
    ORDER BY number_of_losses DESC
    """
    cursor.execute(number_of_losses_query)

    # player standings
    player_standings_query = """
    SELECT winners.player_id AS id, winners.player_name AS name, winners.number_of_wins AS wins,
    number_of_wins+number_of_losses AS matches
    FROM winners LEFT JOIN losers ON winners.player_id = losers.player_id AND winners.tournament_id=losers.tournament_id
    WHERE winners.tournament_id=(%s)
    """
    cursor.execute(player_standings_query, tournament)
    player_standings = cursor.fetchall()
    db.close()
    return player_standings


def reportMatch(winner, loser, tournament):
    """Records the  outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
      tournament: the id number of the match's tournament
    """
    db = connect()
    cursor = db.cursor()
    cursor.execute("INSERT INTO matches(winner_id, loser_id, tournament_id) VALUES(%s,%s, %s)", (winner, loser, tournament))
    db.commit()
    db.close()

def getPlayedMatches(tournament):
    """
    Returns the list of matches played in a specific tournament.
    :param tournament:the id number of the tournament
    :return:list of played matches
    """
    db = connect()
    cursor = db.cursor()
    cursor.execute("SELECT winner_id, loser_id FROM matches WHERE tournament_id=(%s)", (tournament,))
    matches = cursor.fetchall()
    db.close()
    return  matches

def swissPairings(tournament):
    """Returns a list of pairs of players for the next round of a match for a specific tournament.
  
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
    # Get list of matches played
    matches = getPlayedMatches(tournament)
    standings = [(record[0], record[1]) for record in playerStandings(tournament)]

    if len(standings) < 2:
        raise ValueError("Not Enough Players")
    left = standings[0::2]
    right = standings[1::2]
    pairings = zip(left, right)
    results = []
    for pairing in pairings:
        if set(pairing) not in matches:
            pairing = chain(*pairing)
            results.append(pairing)
    return results


