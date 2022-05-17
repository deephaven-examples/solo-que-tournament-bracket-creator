# The brute force method of creating even teams

This document serves as the explanation for how the brute force even team maker works.

Both this script and the "smarter" one attempt to solve the following problem:

- Given $n$ players, teams of size $r$, and ranking criteria (seeding results), how can the players be split into $m$ teams such that the teams are as mathematically evenly matched as possible?

## Validating user inputs

The first thing the script does is validate user inputs. It simply validates that the number of players and team size are integers. Additionally, if there are players left over ($n/r$ is not an integer), it asks if you're ok with that.

## Generating all possible combinations of teams

The next thing the script does is generate a list of lists. This list of lists contains all possible combinations of teams.
For 9 players, teams of 3, and players numbered 1 through 9, this looks like:

```python
[[1, 2, 3], [1, 2, 4], [1, 2, 5], ..., [6, 8, 9], [7, 8, 9]]
```

The method that generates this, `generate_teams`, actually creates a generator object. It is converted to a list in the function call on line 99.

## Record seeding results

Next, the script records seeding results from the seeding CSV file.

## Calculate K/D ratios of possible teams

For every possible team combination, the script calculates the cumulative kill/death (K/D) ratio.

## Find the most balanced combination of teams

With that information now available, the most even team is that which the difference between all four teams in seeding results is the smallest.

## Print the results

Lastly, the script prints results.

## A note about this script

I wrote this script in September 2019 with the intention of using it for a LAN party. I didn't originally write it to be consumed by others. The only change I made is how inputs are specified. The "smarter" team maker more accurately reflects my style of coding nowadays.
