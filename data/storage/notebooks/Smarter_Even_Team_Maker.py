# Imports
from itertools import combinations, compress
import collections
import numpy as np
import copy
import sys
import os

# Function Definitions
# This function checks user input
def check_user_input(team_size, csv_file):

    if not(csv_file[-4:] == ".csv"):
        print("Please specify a CSV file.")
        sys.exit()

    if not(os.path.isfile(csv_file)):
        print("Please specify a CSV file that exists.")
        sys.exit()

    try:
        team_size = int(team_size)
    except ValueError:
        print("The team size you specified is not an integer.")
        sys.exit()

    return team_size, csv_file

# This function reads a CSV containing seeding match data and sorts it by by W/L ratio
def read_seeding_csv(csv_file, team_size):
    f = open(csv_file, "r")
    lines = f.readlines()
    f.close()

    num_players = len(lines) - 1
    num_teams = int(num_players / team_size)
    if num_players % team_size:
        print("The number of players must be an integer multiple of the team size.")
        sys.exit()
    players = [""] * num_players
    seeding_results = np.zeros((num_players, 2), dtype = np.intc)

    for idx, line in enumerate(lines[1:]):
        lg = line.split(",")
        players[idx] = lg[0]
        seeding_results[idx, 0] = int(lg[1])
        seeding_results[idx, 1] = int(lg[2])

    ratios = np.zeros((num_players), dtype = np.single)

    for idx in range(num_players):
        ratios[idx] = seeding_results[idx, 0] / seeding_results[idx, 1]

    rankings = np.argsort(ratios)[::-1]

    return num_players, num_teams, players, seeding_results, rankings

# This function returns an object (generator) containing all combinations of player numbers given a team size
def calculate_team_combinations(n, m):
    team_combinations = combinations(list(range(n)), m)
    team_combinations_list = np.array(list(team_combinations))
    return len(team_combinations_list), team_combinations, team_combinations_list

# This function returns an ordered list of team combinations; the ordering is based off proximity to the mean team W/L ratio
def rank_teams_based_on_wl(team_combinations_list, seeding_results, n, m):
    # Initialize team w/l ratios
    team_wl_ratios = np.array([0] * n, dtype = np.single)
    # Cycle through team combinations
    for i in range(n):
        current_team_cumulative_wins = 0
        current_team_cumulative_losses = 0
        # Cycle through team members
        for j in range(m):
            # Sum the W/L ratios
            current_team_cumulative_wins += seeding_results[team_combinations_list[i][j]][0]
            current_team_cumulative_losses += seeding_results[team_combinations_list[i][j]][1]
        team_wl_ratios[i] = current_team_cumulative_wins / current_team_cumulative_losses

    # Calculate the average W/L ratio
    average_team_wl_ratio = np.mean(team_wl_ratios)
    # Calculate deviations from the mean for each team
    team_wl_deviations = np.array([0] * n, dtype = np.single)
    for i in range(n):
        team_wl_deviations[i] = np.abs(team_wl_ratios[i] - average_team_wl_ratio)
    # Get the rank of each team (ascending) based on deviation from the mean
    team_wl_rankings = np.argsort(team_wl_deviations)
    # Order team combinations based off W/L deviation from the mean
    ranked_team_combinations_list = team_combinations_list[team_wl_rankings]
    ranked_team_wl_ratios = team_wl_ratios[team_wl_rankings]

    return ranked_team_combinations_list, ranked_team_wl_ratios, average_team_wl_ratio

def create_matchup_combinations(ranked_team_combinations, l, n, percent_to_consider):
    idx = int(n * (percent_to_consider / 100))
    top_team_combinations = ranked_team_combinations[:idx]

    all_possible_top_team_combinations = []

    possible_teams_list = top_team_combinations.tolist()

    for i in range(idx):
        temp_team_list = possible_teams_list[i:]
        possible_team_combination = []
        for j in range(l):
            if not(len(temp_team_list)):
                continue
            # The next team to be added to the bracket is the first in the list
            current_team = temp_team_list.pop(0)
            possible_team_combination.append(current_team)
            # Filter out remaining teams based on intersection of ANY team members
            num_teams_left = len(temp_team_list)
            intersect_flags = [False] * num_teams_left
            for k1 in range(num_teams_left):
                possible_next_team = temp_team_list[k1]
                num_curr_teams = len(possible_team_combination)
                for k2 in range(num_curr_teams):
                    curr_team = possible_team_combination[k2]
                    if any(item in curr_team for item in possible_next_team):
                        intersect_flags[k1] = True
                        continue
            intersect_flags = [not(item) for item in intersect_flags]
            temp_team_list = list(compress(temp_team_list, intersect_flags))
        if len(possible_team_combination) == l:
            all_possible_top_team_combinations.append(possible_team_combination)

    return all_possible_top_team_combinations

def display_results(team_comps, players, seeding_results):
    for comp_idx, team_comp in enumerate(team_comps):
        print(f"POSSIBLE SETUP #{comp_idx + 1}:")
        for team_idx, team in enumerate(team_comp):
            team_wins = 0
            team_losses = 0
            for player in team:
                team_wins += seeding_results[player][0]
                team_losses += seeding_results[player][1]
            print(f"\tTeam #{team_idx}: {[players[item] for item in team]} ({team_wins} wins, {team_losses} losses)")

# The Main Function
def main(team_size, seeding_csv_file):
    # Check user inputs
    team_size, seeding_csv_file = check_user_input(team_size, seeding_csv_file)
    # Get the results of the seeding match into memory
    num_players, num_teams, players, seeding_results, player_rankings = read_seeding_csv(seeding_csv_file, team_size)
    # Calculate combinations for this player set
    num_team_combinations, team_combinations, team_combinations_list = calculate_team_combinations(num_players, team_size)
    # Rank teams based off cumulative W/L ratio
    ranked_team_combinations, ranked_team_wl_ratios, average_team_wl_ratio = \
        rank_teams_based_on_wl(team_combinations_list, seeding_results, num_team_combinations, team_size)
    # Create matchup combinations from the ranked team combinations
    even_team_combinations = create_matchup_combinations(ranked_team_combinations, num_teams, num_team_combinations, 10)
    # Display/print/write even team combinations
    display_results(even_team_combinations, players, seeding_results)

if __name__ == "__main__":
    start = time.time()
    main(4, "/data/csv/halo_seeding_match.csv")
    end = time.time()
    print(f"\nSmarter even team making took {end - start} seconds.")
