# A smarter way to make even teams

The brute force even team maker will return the most mathematically even teams possible. The problem is that it exhaustively searches all possible combinations of teams, which is problematic.

## Exponentially increasing ways to sort players

As the number of objects in a pool increases, so does the number of ways to arrange them. The same can be said about combinations.
Combinations of combinations is another story entirely. That number goes up so fast it makes the brute force method far too slow to handle.
Thus is born the need to more efficiently pick team combinations.

## Steps

### Validate user input

This script takes two inputs. They are specified on line 156.

- The team size
- The seeding results in CSV format

This script does not take a number of players. That would be redundant. Originally, the brute force approach used user input on the command line, and thus, the need to specify the number of players was required at the time.

If the first argument is an integer, and the second is a file, then this step is complete.

### Read the seeding CSV file

The script then reads and parses the seeding CSV file. It returns the number of players, teams, the player names, seeding results, and player rankings.

### Create all possible teams

This is the first place this script truly differs from the brute force one.

Instead of creating all possible combinations of teams, it simply calculates all possible teams.
The method `calculate_team_combinations` returns both a generator and list of the possible teams, as well as how many there are.

### Rank potential teams

The teams are then ranked based off their cumulative win/loss ratios. Wins and losses can be whatever you want them to be.
The ranking is done based off deviation from the average win/loss ratio. The closer the team's W/L ratio to the average, the higher ranked it is.

### Create even team combinations

This is the other place this script and the brute force script differ greatly.

With the potential teams ranked, it's time to create combinations of teams. Since all teams must be even, teams of disproportionately high or low skill level can be discarded.
Thus, the bottom 90% of potential teams (ranked) are discarded, and only the top 10% are used.

With the top 10% of potential teams remaining, it's time to check if there's a combination of four of them where there is no player overlap between any team.

This is how that's done:

- For every potential team in the top 10% of most evenly matched potential teams:
  - For every team in the combination of teams:
    - Add the first team in the list to the team combination
    - Remove all subsequent potential teams that have any overlap in team membership with
  - If there are the correct number of teams
    - Add this combination of teams to the possibilities
    
See for yourself how this is done in the code, as this is a very basic explanation.


### Display all of the top combination

This prints all of the combinations just created in the previous step.

## A note

It's worth noting that this "smarter" approach won't always find the #1 evenly matched combination of teams.
This approach is not exhaustive in its search. It will find at most only one team combination for every team in the top 10% of evenly matched teams.
Despite these drawbacks, the performance increase is worthwhile.
Even though the team combinations given may not be the #1 most even, they are all very evenly matched regardless.
