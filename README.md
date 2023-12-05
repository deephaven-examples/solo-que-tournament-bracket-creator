# Solo Queue Team Game Tournament Bracket Creator

This repository contains content for creating evenly matched tournament brackets for team games in which all participating players solo queue.

## Structure

This repository is split up into a few different folders. The files in this base folder are used for starting up the application in Deephaven.

- `Docs`: Contains further explanation of the math and other concepts required to understand the solutions.
- `data`: Contains scripts and a CSV file.

## Usage

This application is meant to be used to construct tournaments for team based games.
The brackets consist of teams that are mathematically evenly matched.
For guidance on how to use both of the scripts, refer to the file `/data/Usage.md`.

This repository has the same pre-requirements as those listed in [deephaven-core](https://github.com/deephaven/deephaven-core). To run it, from your shell:

```bash
docker compose pull
docker compose up
```

Then, navigate to `http://localhost:10000/ide` in your browser (preferably Chrome or Firefox).

The two scripts run using a pre-made CSV of seeding match results. Feel free to test out your own seeding results, provided they are in the same format as the provided CSV.

NOTE: The seeding results are made up. I actually had real seeding results at one point, but lost them. While I did well in the real seeding match, I didn't go 23-10. I'm not actually that good at Halo.

## Notes

There are two scripts that do basically the same team - split up a group of 16 players in to 4 teams of 4 that are evenly matched based on the results of a seeding match. The first, which splits the teams using a brute force technique, takes ~27 seconds to run on my Macbook Pro. The second, which splits teams using a more elegant solution, takes ~0.05 seconds on my Macbook pro. This is approximately a 540x speedup. For an explanation of each solution, which gives more insight into the reasons for the drastic speedup, see the `Docs` folder.

The code in this repository is built for Deephaven Community Core v0.19.1. No guarantee of forwards or backwards compatibility is given.
