-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

-- Create database
CREATE DATABASE tournament;
\c tournament;
-- Create tables
-- Create players table
-- id : the serial id of players and name : the name of each player
CREATE TABLE players (player_id serial primary key, player_name text);
-- Create matches table
CREATE TABLE matches(match_id serial, player1_id serial, player2_id serial, winner_id serial references players(player_id));
