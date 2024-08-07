import time


global generations,expansions
def calculate_possibilities_with_stations(coins):
    possibilities = []
    sheriff_station_cost = 4
    deputy_costs = [0, 1, 5, 13]  # Possible deputies configurations
    deputy_to_radius = {0: 1, 1: 2, 5: 3, 13: 4}  # Mapping deputies to radii

    max_stations = coins // sheriff_station_cost

    # Helper function to generate unique combinations of deputies
    def find_combinations(current_stations, current_coins, station_deputies):
        if current_stations == 0:
            total_deputies = sum(station_deputies)
            total_cost = len(station_deputies) * sheriff_station_cost + total_deputies
            if total_cost <= coins:
                possibilities.append({
                    'stations': len(station_deputies),
                    'deputies': total_deputies,
                    'total_cost': total_cost,
                    'remaining_coins': coins - total_cost,
                    'station_radii': [deputy_to_radius[d] for d in station_deputies]  # Calculate radius for each station
                })
        else:
            # Only add combinations that are sorted or equal to the last element to avoid duplicates
            last_deputy = station_deputies[-1] if station_deputies else -1
            for cost in deputy_costs:
                if current_coins >= sheriff_station_cost + cost and (not station_deputies or cost >= last_deputy):
                    find_combinations(current_stations - 1, current_coins - (sheriff_station_cost + cost), station_deputies + [cost])

    # Start the recursive combination finding
    for num_stations in range(1, max_stations + 1):
        find_combinations(num_stations, coins, [])

    return possibilities

def dfs_for_family_protection(map, target_families, station_radii):
    generations = 0
    expansions = 0
    start_time = time.time()
    map_height = len(map)
    map_width = len(map[0])
    firstGen=False;
    
    if (firstGen==False):
        print("First generation: Empty map")
        firstGen=True;
        generations=1;

    def dfs_from_point(covered_cells, areas, total_families, depth):
        
        nonlocal generations, expansions
        expansions+=1
        
        
        if depth == len(station_radii) or total_families >= target_families:
          #  print("a ver se entra")
            return areas, total_families_covered_with_station, generations, expansions, time.time() - start_time

        best_solution = (areas, total_families, generations, expansions, time.time() - start_time)
        for i in range(len(map)):
            for j in range(len(map[0])):
                generations+=1
                
                
                
                if 0 <= depth - 1 < len(areas):
                    if areas[depth - 1] != (i, j):
                        print("Previous area at depth", depth, ":", areas[depth - 1], "current coordinate", j, i, "generations:", generations, "expansions:", expansions)
                        
                    else:generations -= 1

                else:
                    print("Previous area at depth: None", "current coordinate", j, i, "generations:", generations, "expansions:", expansions)
                

                                    
                
                
                radius = station_radii[depth]
                new_covered = {(x, y) for x in range(i - radius, i + radius + 1)
                               for y in range(j - radius, j + radius + 1)
                               if 0 <= x < len(map) and 0 <= y < len(map[0])}

                total_families_covered_with_station = total_families + sum(map[k][l] for k, l in new_covered if (k, l) not in covered_cells and 0 <= k < len(map) and 0 <= l < len(map[0]))

                if total_families_covered_with_station >= target_families:
                    
                    #print(depth)
                    #this way stops the algorithm rigt away
                    return areas + [(i, j)], total_families_covered_with_station, generations, expansions, time.time() - start_time

                if total_families_covered_with_station > best_solution[1]:
                    #print("entra na 87")
                    best_solution = (areas + [(i, j)], total_families_covered_with_station, generations, expansions, time.time() - start_time)

                if depth + 1 < len(station_radii):
                    #expansions += 1
                    #print("agora aqui 92...novo nivel=1")
                    #generations+=1
                    if (generations==1):
                        print("Previous area at depth 0 : None current coordinate 0 0 generations: 1 expansions: 1")
                    next_level_solution = dfs_from_point(covered_cells.union(new_covered), areas + [(i, j)], total_families_covered_with_station, depth + 1)

                    if next_level_solution[1] > best_solution[1]:
                        best_solution = next_level_solution

                    if next_level_solution[1] >= target_families:
                        return next_level_solution
#(len(areas) >= depth and
                if all(area == (map_height - 1, map_width - 1) for area in areas[-depth:]) and i == map_height - 1 and j == map_width - 1:
                    print("Stop condition reached. All possibilities tested for depth:", depth + 1)
                    if depth == 0:
                        print("Best solution:")
                    
                    elapsed_time = time.time() - start_time
                    return (best_solution[0], best_solution[1], generations, expansions, elapsed_time)
                    

        return best_solution

    
    return dfs_from_point(set(), [], 0, 0)



def print_map_with_stations(map, station_positions, station_radii):
    covered_cells = set()
   
    for (x, y), radius in zip(station_positions, station_radii):
        for i in range(x - radius, x + radius + 1):
            for j in range(y - radius, y + radius + 1):
                if 0 <= i < len(map) and 0 <= j < len(map[0]):
                    covered_cells.add((i, j))
    
   
    for i in range(len(map)):
        for j in range(len(map[i])):
            cell = map[i][j]
            if (i, j) in station_positions:
                # Se a célula é uma posição de estação, adiciona o asterisco sem parênteses
                cell_str = f"{cell}*".rjust(4)
            elif (i, j) in covered_cells:
                # Se a célula está coberta e não é uma posição de estação, adiciona parênteses
                cell_str = f"({cell})".rjust(4)
            else:
                # Se não está coberta nem é uma posição de estação, imprime normalmente
                cell_str = f"{cell}".rjust(4)
            print(cell_str, end=' ')
        print()  # Nova linha após imprimir cada linha do mapa

def main():
    tables = [
        [[0, 7, 0, 0, 4], [0, 0, 0, 4, 0], [1, 0, 0, 0, 0], [4, 4, 1, 0, 0], [6, 0, 3, 4, 4]],
        [[4, 0, 0, 10, 1], [1, 0, 0, 0, 0], [0, 0, 1, 6, 3], [0, 4, 0, 0, 2], [8, 0, 6, 3, 0]],
        [[0, 8, 0, 4, 5, 10, 0], [0, 4, 0, 7, 0, 4, 0], [0, 2, 4, 2, 0, 0, 2], [0, 7, 0, 1, 2, 0, 0], [2, 4, 0, 0, 3, 0, 2], [0, 4, 0, 0, 3, 0, 0], [2, 0, 0, 0, 0, 0, 0]],
        [[0, 0, 1, 0, 7, 0, 1], [0, 1, 4, 0, 0, 0, 4], [0, 0, 0, 0, 2, 0, 0], [3, 1, 0, 8, 5, 7, 7], [0, 4, 0, 3, 0, 0, 0], [0, 0, 0, 3, 2, 4, 2], [0, 8, 3, 6, 3, 0, 0]],
        [[6, 7, 2, 0, 0, 0, 0, 0, 0], [3, 3, 6, 0, 8, 4, 3, 1, 0], [0, 0, 8, 0, 0, 0, 2, 4, 0], [0, 0, 0, 1, 0, 3, 2, 0, 0], [0, 0, 0, 7, 4, 0, 1, 0, 0], [12, 8, 0, 5, 4, 1, 4, 3, 4], [8, 0, 1, 2, 4, 3, 3, 0, 0], [1, 1, 0, 0, 0, 0, 5, 0, 0], [4, 0, 0, 0, 4, 6, 0, 13, 2]],
        [[0, 0, 0, 0, 0, 0, 0, 0, 0], [4, 0, 8, 4, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 3, 0, 0, 1, 0], [0, 3, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 1, 1, 0, 0, 3, 0], [0, 0, 2, 4, 0, 0, 0, 1, 0], [0, 2, 0, 0, 8, 0, 4, 3, 10], [0, 0, 3, 0, 0, 4, 0, 0, 0]],
        [[0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0], [0, 0, 11, 2, 0, 0, 9, 3, 0, 0, 3], [0, 0, 0, 3, 1, 0, 2, 0, 0, 0, 0], [4, 1, 2, 3, 0, 4, 0, 0, 4, 0, 0], [5, 0, 0, 0, 4, 0, 1, 0, 4, 3, 0], [0, 0, 0, 7, 4, 0, 1, 0, 0, 7, 0], [0, 8, 0, 0, 0, 0, 3, 0, 1, 0, 3], [0, 3, 0, 0, 5, 2, 3, 0, 0, 0, 2], [0, 0, 0, 3, 1, 0, 2, 8, 0, 0, 0], [0, 3, 4, 0, 7, 0, 0, 7, 0, 0, 0], [4, 2, 0, 4, 0, 3, 0, 0, 5, 7, 0]],
        [[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 10, 10, 0, 0, 0, 4, 5, 0, 0], [0, 4, 1, 0, 8, 0, 0, 0, 0, 0, 5], [8, 0, 0, 0, 0, 0, 6, 0, 0, 0, 0], [0, 0, 0, 0, 13, 0, 0, 0, 2, 0, 3], [0, 0, 0, 0, 4, 0, 0, 0, 0, 1, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 4, 0, 0, 0, 0, 3, 0, 0, 0], [4, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]],
        [[2, 4, 0, 0, 6, 7, 3, 4, 0, 0, 3, 0, 1], [0, 0, 2, 0, 3, 0, 0, 6, 0, 0, 8, 11, 3], [0, 3, 0, 8, 0, 0, 2, 0, 0, 0, 0, 0, 4], [2, 0, 0, 0, 0, 0, 0, 0, 0, 3, 2, 0, 0], [0, 6, 0, 8, 0, 3, 0, 0, 0, 0, 0, 0, 1], [0, 3, 0, 2, 0, 0, 9, 0, 0, 0, 0, 5, 6], [1, 9, 4, 0, 0, 2, 4, 0, 0, 0, 3, 2, 0], [2, 3, 0, 4, 0, 0, 0, 6, 2, 0, 1, 0, 3], [0, 0, 0, 0, 0, 6, 0, 0, 0, 2, 2, 0, 8], [7, 2, 4, 2, 0, 0, 6, 4, 1, 0, 0, 0, 7], [0, 0, 0, 11, 0, 0, 0, 0, 3, 4, 0, 9, 0], [0, 0, 0, 0, 1, 4, 3, 4, 0, 0, 0, 3, 11], [0, 0, 4, 7, 7, 0, 0, 2, 0, 2, 5, 0, 1]],
        [[0, 0, 1, 4, 0, 0, 9, 0, 0, 0, 12, 0, 1], [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0], [1, 0, 0, 0, 0, 0, 2, 0, 0, 2, 0, 0, 0], [0, 0, 0, 0, 0, 9, 4, 0, 0, 0, 6, 0, 0], [0, 6, 9, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 1, 6, 10, 0, 1, 4], [0, 3, 0, 0, 0, 1, 0, 0, 0, 0, 0, 2, 0], [0, 0, 0, 1, 3, 0, 0, 0, 0, 9, 0, 0, 0], [9, 0, 0, 3, 3, 0, 0, 0, 0, 3, 4, 0, 0], [0, 1, 4, 0, 0, 0, 0, 0, 0, 5, 0, 1, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [2, 0, 0, 0, 0, 3, 3, 0, 0, 0, 0, 0, 10], [0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0]]
    ]
    
    


    while True:
        print("\nMENU:")
        print("1 - Calculate possibilities for station and deputy distribution")
        print("2 - Choose a map and present a solution")

        choice = input("Choose an option (1/2): ")

        if choice == '1':
            coins = int(input("Enter the number of coins available: "))
            possibilities = calculate_possibilities_with_stations(coins)
            print("\nPossibilities:")
            for possibility in possibilities:
                print(possibility)
        elif choice == '2':
            map_choice = int(input(f"Which map would you like to use (1-{len(tables)}): ")) - 1
            if map_choice < 0 or map_choice >= len(tables):
                print("Invalid choice. Please choose a number between 1 and 10.")
            else:
                coins = int(input("How many coins do you have: "))
                possibilities = calculate_possibilities_with_stations(coins)
                print("Available options based on coins:")
                for idx, option in enumerate(possibilities, start=1):
                    print(f"{idx}. Stations: {option['stations']}, Deputies: {option['deputies']}, Total cost: {option['total_cost']}, Remaining coins: {option['remaining_coins']}")

                option_choice = int(input(f"Choose one of the options (1-{len(possibilities)}): ")) - 1
                if option_choice < 0 or option_choice >= len(possibilities):
                    print("Invalid choice. Please select one of the listed options.")
                else:
                    selected_option = possibilities[option_choice]
                    print(f"You chose the option with {selected_option['stations']} sheriff stations and {selected_option['deputies']} deputies.")
                    print(f"Radius configuration for each station: {selected_option['station_radii']}")
                    target_families = int(input("How many families do you want to protect? "))
                    result = dfs_for_family_protection(tables[map_choice], target_families, selected_option['station_radii'])
                    
                    station_positions, total_families_covered, generations, expansions, time = result
                    print("Families protected:", total_families_covered)
                    print_map_with_stations(tables[map_choice], station_positions, selected_option['station_radii'])
                    print("Generations:", generations, "Expansions:", expansions, "Execution time:", time)

                    


        
        
        
        
if __name__ == "__main__":
    main()
