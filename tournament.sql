-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

-- Create database
CREATE DATABASE tournament;
-- Connect to database
\c tournament;

-- Create tables
-- Create players table
-- id : the serial id of players and name : the name of each player
CREATE TABLE players (
    player_id serial primary key,
    player_name text
);

-- Create tournaments table
CREATE TABLE tournaments(
    tournament_id serial primary key,
    tournament_name text
);

-- Create matches table
CREATE TABLE matches(
    match_id serial primary key,
    winner_id int,
    loser_id int,
    tournament_id int,
    foreign key(winner_id) references players(player_id),
    foreign key(loser_id) references players(player_id),
    foreign key(tournament_id) references tournaments(tournament_id)
);

-- Create a table to old relations between players and tournaments
CREATE TABLE players_in_tournaments(
    player_id int references players(player_id),
    tournament_id int references tournaments(tournament_id),
    primary key(player_id, tournament_id)
);