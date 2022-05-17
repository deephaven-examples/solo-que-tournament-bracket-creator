# Using the Even Team Makers

There are two Python scripts that will create even teams given three arguments.
These arguments are specified all the way at the bottom of the scripts.

## Brute force method

The script `../Python/Brute_Force_Even_Team_Maker.py` requires three input arguments.
They are as follows:

- Total number of players (integer)
- Team size (integer)
- Seeding CSV file (filename with path)

These arguments are specified on line 108 of the script.

## Smarter method

The script `../Python/Smarter_Even_Team_Maker.py` requires two input arguments.
They are as follows:

- Team size (integer)
- Seeding CSV file (filename with path)

These arguments are specified on line 156 of the script.

## Creating a new seeding CSV file

Creating and using a new seeding CSV file is simple.
The CSV should have a header, and three columns.
The header can say whatever you want it to.
The leftmost column is the player name.
The middle column is the number of "wins" per player.
The rightmost column is the number of "losses" per player.
Wins/losses can be whatever you want them to be. For example:

- wins = wins, losses = losses
- wins = kills, losses = deaths
- wins = goals for, losses = goals against

It's recommended to place the CSV into the `/data` directory.
