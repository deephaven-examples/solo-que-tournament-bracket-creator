---
title: Even team bracket creator
author: jjbrosnan
---

## Standard player ranking systems in online gaming

Online video games use matchmaking systems that attempt to optimize the quality of the matches for the players involved. Ranking systems usually use an MMR (matchmaking rating) system that assigns you a score in points based on the following:

- Wins
- Losses
- Performance relative to other players
- Difference in MMR relative to other players

Every player who plays a game has an MMR.  These MMRs are usually bracketed into leagues, which further enhance the matchmaking quality.

These matchmaking systems collect players in a que, then assign them to matches and sorts players into teams that minimize the MMR difference between the two.  This is a simple task for organizing individual games.

## A new solo que team game format appears

The same can not be said about creating tournaments with teams of solo que players easily.  Thus drives the need for a tournament maker for solo que players to play in team games in a tournament format.

Many games could benefit from an online matchmaking experience dedicated to a tournament format for solo que players.  Games such as:

- Counter Strike: Global Offensive
- League of Legends
- Call of Duty
- Rocket League
- Many, many others

This tournament format would be as follows:

Solo que players can que up for a tournament mode, which will place them into a lobby with $n - 1$ other players.  The MMR of each player will be analyzed, and $r$ teams will be created such that each team's cumulative MMR is as close as possible with all other teams.  The mode would place players into $m$ evenly matched teams, then seed them by the MMR of the highest ranked player on each team.  The teams and their respective rankings would then be used to create a standard tournament style bracket, where teams would be eliminated until only one remains and is crowned victorious.

Games often have this type of mode for 1v1 game formats.  It's easy to make a bracket with seeding based off a single MMR value.  It's much more difficult when to do for team-based games, when the team's aren't set ahead of time.

## The original motivation

Back in September 2019, I decided to host a LAN tournament for the game `Halo: Master Chief Collection`.  I was able to muster up 16 people, 4 consoles, 16 controllers, and 4 tvs in different rooms to play in a little tournament.  It was _awesome_.  In the week leading up to the tournament, I realized I had a problem.  I didn't know over half of the people coming to play, nor did I know basically anyone's skill level.  So, I decided I'd write some code to ensure that we could have a LAN tournament where the teams are evenly matched.

This code would depend on me inputting each player's name, and the results of a seeding match (a rough equivalent to an MMR rating).  The seeding match was a single 16 player free for all game, where everyone's results were the number of kills and deaths at the end of the match.  Those results can be used to create even teams.

## Combinatorics and tournaments

### Combinations

Given a player pool of $n$ players, how many ways can they be split up into $r$ unique teams?

The answer is as follows:

$_{n}C_{r} = \frac{n!}{r!(n - r)!}$

This is known as a combination, for which the mathematical definition is:

- The number of ways to choose a sample of $r$ distinct objects from a pool of $n$ distinct objects.
  - Order does not matter
    - The team `[1, 2, 3, 4]` is the same as `[4, 3, 2, 1]`
  - Replacements are not allowed
    - No single player can play on more than one team

Let's calculate the total number of possible teams for a tournament with 16 players and teams of 4 players each:

$_{16}C_{4} = \frac{16!}{4!12!} = \frac{(16)(15)(14)(13)}{(4)(3)(2)} = 1820$

There are 1820 possible teams of 4 from a pool of 16 players.  If the players are numbered 1 through 16, this set of all possible teams of 4 looks something like this in memory:

```python
[(1, 2, 3, 4), 
 (1, 2, 3, 5), 
 (1, 2, 3, 6), 
 ..., 
 (11, 14, 15, 16)
 (12, 14, 15 ,16)
 (13, 14, 15, 16)]
```

This is straightforward.  Now consider the question of how many combinations of combinations can we create?  That's to say, how many different ways can we organize the 16 players into 4 teams of 4?

### Combinations of combinations

Given $n$ unique objects and $r$ groups, how many unique combinations of $r$ groups of $m$ objects can you create?

The answer is as follows:

$_{n}CC_{r} = \frac{\prod_{k=1}^{n/r} \frac{(kr)!}{r!(kr - r)!}}{\lfloor n/r \rfloor !}$

For 16 players and 4 teams, this looks like:

$_{16}CC_{4} = \frac{\prod_{k=1}^{4} \frac{(4k)!}{r!(4k - 4)!}}{4!}$

$_{16}CC_{4} = \frac{(\frac{4!}{4!0!})(\frac{8!}{4!4!})(\frac{12!}{8!4!})(\frac{16!}{12!4!})}{4!}$

$_{16}CC_{4} = 2,627,625$

There are a _LOT_ more ways to split 16 players up into 4 teams of 4 than there are into a single team of 4.  There are well over 1,000 times as many ways.  In fact, this discrepancy becomes a real problem as $n$ gets large, regardless of $r$.

### 64 players and 16 teams

A single example can show just how futile it would be to check every possible combination of teams for a tournament.  Let's take $n$ = 64 and $r$ = 4 for example.  Here's some Python code we can use to to calculate:

- How many unique teams of 4 people we can create
- How many ways we can organize 16 teams of 4 players

```python
from math import factorial

def calc_combinations(n, r):
    return factorial(n) / (factorial(r) * factorial(n - r))

def calc_combinations_of_combinations(n, r):
    m = math.floor(n / r)
    k = n
    product = 1
    while k <= n:
        product *= calc_combinations(k, r)
        k += r
    product /= factorial(m)
    return product
```

You can verify that this code works for $n$ = 16 and $r$ = 4 yourself.  For now, let's do $n$ = 64 and $r$ = 16:

```python
c = calc_combinations(64, 4)
cc = calc_combinations_of_combinations(64, 4)

print(c)
print(cc)
```

```shell
635376
4.363407645282884e+65 b
```

That is a ridiculous number of unique combinations of teams.  Obviously, that's a problem.  We cannot possibly hope to store all of those combinations, nor can we process that many.  Thus, for sufficiently sized tournaments, an efficient way to find evenly matched teams must be used.

## The brute force method

For sufficiently small $n$, a brute force method can be used.  The brute force method follows these steps:

- Gather player names and MMR
- Store all possible teams with the given $n$ players and $r$ teams
- Create all possible combination of teams
- Calculate every possible team's average MMR
- Order all possible combinations of teams by the smallest difference in average MMR between teams
- Take the first team in the ordered list as the solution

The code for this can be found in the file `../Python/Brute_Force_Even_Team_Maker.py`.

## A more elegant method

As $n$ gets large, so does the need to avoid the problem of an exponentially increasing number of combinations of teams you can create.  This is not an easy problem to solve.  There are two approaches to consider:

- Use the overall rank of each player to generate even teams.
- Use the MMR of each player to generate even teams.

### Overall rank

Using the overall rank of each player is straight forward.  Take MMRs, place them in descending order, and use the rankings to create teams.  These teams should have an average overall rank equal to the average rank of all players.  For sixteen players ranked 1 through 16, this average is 8.5.  For 64 players, the average is 32.5. 

While this approach is sensible, it does have a major drawback.  Uneven MMR distributions in a player pool could cause teams of uneven skill to be created.  For instance, if all players but one in a tournament have an MMR rating of around 2500, and one single player has an MMR of 5000, that won't make for even teams.  This is a perfectly acceptable approach if the MMRs are split in a relatively uniform manner.

### MMR

The other option is to use player's MMR.  Using MMR is required when creating teams with a single player way above the rest.  Otherwise, one team will be at a significant advantage.  This method is a more generalizable solution, as it will work for uneven MMR distributions in a player pool.

### Being smart about choosing teams

The "smarter" method of choosing teams can be broken down into the following steps:

- Gather player names and MMR
- Generate a list of all possible teams
- Calculate the average MMR of each team
- Rank the teams based on proximity to the average MMR of everyone in the lobby
- Discard the teams outside of the top N% of this criteria
- For each team in the remaining list
  - Attempt to make more teams until all players have been placed on a team

The code for this can be found in the file `../Python/Smarter_Even_Team_Maker.py`

## Performance difference

Test out the scripts yourself with different numbers of players.  On my local machine, when using the file `/data/halo_seeding_match.csv` with 16 players and teams of 4, I show about a 340x speedup when going from the brute force method to the "smarter" one.
