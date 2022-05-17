# Imports
import itertools
import time
import sys


# Function Definitions
def assert_inputs(num_players, team_size):
    try:
        num_players = int(num_players)
    except ValueError:
        print('Your number of players is not a valid integer number.')
        print('Exiting...')
        sys.exit()
    try:
        team_size = int(team_size)
    except ValueError:
        print('Your team size is not a valid integer number.')
        print('Exiting...')
        sys.exit()
    players_leftover = num_players % team_size
    if players_leftover:
        print('You have ' + str(players_leftover) + ' players left over.')
    num_teams = int(num_players / team_size)

    return num_players, team_size, num_teams


def generate_teams(lst, n):
    if not lst:
        yield []
    else:
        for team in (((lst[0],) + xs) for xs in itertools.combinations(lst[1:], n - 1)):
            for teams in generate_teams([x for x in lst if x not in team], n):
                yield [team] + teams


def report_seeds(csv_file, num_players):
    f = open(csv_file, "r")
    lines = f.readlines()
    f.close()
    seeding_results = lines[1:]
    num_players_in_csv = len(seeding_results)
    if not(num_players_in_csv == num_players):
        print("The number of players in the CSV file is not equal to what you specified.")
        sys.exit()
    kills = [0] * num_players
    deaths = [0] * num_players
    kd_ratios = [0] * num_players
    for i in range(0, num_players):
        kills[i] = int(seeding_results[i].split(",")[1])
        deaths[i] = int(seeding_results[i].split(",")[2])
        kd_ratios[i] = kills[i] / float(deaths[i])
    return kills, deaths, kd_ratios

def calculate_kd_ratios(possible_teams, kills, deaths, num_teams):
    kds = [0] * len(possible_teams)

    possible_ratios = [[0] * num_teams for i in range(0, len(possible_teams))]

    for i in range(0, len(possible_teams)):
        for j in range(0, len(possible_teams[i])):
            k_tot = 0
            d_tot = 0
            for k in range(0, len(possible_teams[i][j])):
                player = possible_teams[i][j][k]
                k_tot += kills[player]
                d_tot += deaths[player]
            possible_ratios[i][j] = k_tot / float(d_tot)

    return possible_ratios


def calculate_most_even_teams(possible_teams, possible_kd_ratios):
    kd_diffs = [0] * len(possible_teams)
    for i in range(0, len(possible_teams)):
        for j in range(1, len(possible_teams[i])):
            kd_diffs[i] += abs(possible_kd_ratios[i][j] - possible_kd_ratios[i][j - 1])

    most_balanced_index = kd_diffs.index(min(kd_diffs))
    most_balanced_teams = possible_teams[most_balanced_index]
    most_balanced_ratios = possible_kd_ratios[most_balanced_index]

    return most_balanced_teams, most_balanced_ratios, most_balanced_index


def display_most_balanced_teams(most_balanced_teams, most_balanced_ratios, possible_kd_ratios, kills, deaths):
    print('\nTHESE ARE THE MOST BALANCED TEAMS:\n')
    for i in range(0, len(most_balanced_teams)):
        print('\tTeam #' + str(i + 1) + ':\n')
        for j in range(0, len(most_balanced_teams[i])):
            pnum = most_balanced_teams[i][j]
            print('\t\tPlayer #' + str(pnum + 1) + ' ' + str(kills[pnum]) + ' kills, ' + str(deaths[pnum]) + ' deaths.')
            print('\tOverall team K/D ratio: ' + str(most_balanced_ratios[i]) + '\n')


def main(num_players, team_size, seeding_csv):
    num_players, team_size, num_teams = assert_inputs(num_players, team_size)
    possible_teams = list(generate_teams(range(0, num_players), team_size))
    kills, deaths, kd_ratios = report_seeds(seeding_csv, num_players)
    possible_kd_ratios = calculate_kd_ratios(possible_teams, kills, deaths, num_teams)
    most_balanced_teams, most_balanced_ratios, most_balanced_index = calculate_most_even_teams(possible_teams,
                                                                                               possible_kd_ratios)
    display_most_balanced_teams(most_balanced_teams, most_balanced_ratios, possible_kd_ratios, kills, deaths)


if __name__ == '__main__':
    main(16, 4, "/data/halo_seeding_match.csv")