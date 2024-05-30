# import json
# from datetime import datetime, timedelta
#
# # Load the data
# with open('daneV3.json') as f:
#     data = json.load(f)
#
# start_date_str = "2024-04-01"  # Example start date
#
# # Initialize variables and divide all values by 2
# ulg95 = {k: v / 2 for k, v in data['ulg95'].items()}
# dk = {k: v / 2 for k, v in data['dk'].items()}
# ultsu = {k: v / 2 for k, v in data['ultsu'].items()}
# ultdk = {k: v / 2 for k, v in data['ultdk'].items()}
#
# # Tank capacities
# tanks = [7400, 6100, 4000, 8500, 10000]
#
#
# # Function to check if values can fit into the tanks without mixing and return the assignments
# def can_fit_in_tanks(values, tanks):
#     remaining = tanks[:]
#     assignments = {i: [] for i in range(len(tanks))}
#
#     def backtrack(values, index):
#         if index == len(values):
#             return True
#         value, var_name = values[index]
#         for i in range(len(remaining)):
#             if remaining[i] >= value and (not assignments[i] or assignments[i][0][0] == var_name):
#                 remaining[i] -= value
#                 assignments[i].append((var_name, value))
#                 if backtrack(values, index + 1):
#                     return True
#                 remaining[i] += value
#                 assignments[i].pop()
#             elif remaining[i] > 0 and (not assignments[i] or assignments[i][0][0] == var_name):
#                 part_value = remaining[i]
#                 remaining[i] = 0
#                 assignments[i].append((var_name, part_value))
#                 if backtrack([(value - part_value, var_name)] + values[index + 1:], 0):
#                     return True
#                 remaining[i] = part_value
#                 assignments[i].pop()
#         return False
#
#     if backtrack(values, 0):
#         formatted_assignments = {}
#         for tank, vars_in_tank in assignments.items():
#             if vars_in_tank:
#                 formatted_assignments[tank] = ' + '.join(f"{var} ({val})" for var, val in vars_in_tank)
#         return formatted_assignments
#     else:
#         return None
#
#
# # Function to sum values safely
# def safe_sum(values, start_day, end_day):
#     return sum(values.get(str(day), 0) for day in range(start_day, end_day + 1))
#
#
# # Manually set start date
#
# start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
#
# # Initialize the cumulative values with zeros
# cumulative_values = {
#     "ulg95": 0,
#     "dk": 0,
#     "ultsu": 0,
#     "ultdk": 0,
# }
# total_sum = 0
#
# # Find the first day in the data
# first_day_in_data = min(int(day) for day in ulg95.keys())
#
# # Initialize the variable to store the last valid day
# last_valid_day = None
# last_valid_values = None
# last_valid_assignments = None
#
# # Iterate over the days in the data starting from the first day in the data
# for day_key in sorted(ulg95.keys(), key=int):
#     day_offset = int(day_key) - first_day_in_data
#     current_date = start_date + timedelta(days=day_offset)
#
#     # Add values for the current day
#     cumulative_values["ulg95"] += ulg95.get(day_key, 0)
#     cumulative_values["dk"] += dk.get(day_key, 0)
#     cumulative_values["ultsu"] += ultsu.get(day_key, 0)
#     cumulative_values["ultdk"] += ultdk.get(day_key, 0)
#
#     # Calculate the total sum
#     total_sum = cumulative_values["ulg95"] + cumulative_values["dk"] + cumulative_values["ultsu"] + cumulative_values[
#         "ultdk"]
#
#     # Check if the total sum is less than 32000
#     if total_sum < 32000:
#         # Check if the values can fit into the tanks
#         assignments = can_fit_in_tanks([(cumulative_values["ulg95"], "ulg95"),
#                                         (cumulative_values["dk"], "dk"),
#                                         (cumulative_values["ultsu"], "ultsu"),
#                                         (cumulative_values["ultdk"], "ultdk")], tanks)
#         if assignments:
#             # Store the valid state with the current date
#             last_valid_day = current_date
#             last_valid_values = cumulative_values.copy()
#             last_valid_assignments = assignments
#     else:
#         # If the sum exceeds 32000, stop processing
#         break
#
# # Print the results for the last valid day
# if last_valid_day:
#     print(f"Last valid day: {last_valid_day.strftime('%Y-%m-%d')}")
#     print("Values:", last_valid_values)
#     print("Assignments:")
#     for tank_index, assignment in last_valid_assignments.items():
#         print(f"  Tank {tank_index + 1} (Capacity {tanks[tank_index]}): {assignment}")
# else:
#     print("No valid day found that meets the conditions.")

# Na dole algorytm wpisany w funkcję

import json
from datetime import datetime, timedelta


def process_tank_data(data, start_date_str):
    # Initialize variables and divide all values by 2
    ulg95 = {k: v / 2 for k, v in data['ulg95'].items()}
    dk = {k: v / 2 for k, v in data['dk'].items()}
    ultsu = {k: v / 2 for k, v in data['ultsu'].items()}
    ultdk = {k: v / 2 for k, v in data['ultdk'].items()}

    # Tank capacities
    tanks = [7400, 6100, 4000, 8500, 10000]

    # Function to check if values can fit into the tanks without mixing and return the assignments
    def can_fit_in_tanks(values, tanks):
        remaining = tanks[:]
        assignments = {i: [] for i in range(len(tanks))}

        def backtrack(values, index):
            if index == len(values):
                return True
            value, var_name = values[index]
            for i in range(len(remaining)):
                if remaining[i] >= value and (not assignments[i] or assignments[i][0][0] == var_name):
                    remaining[i] -= value
                    assignments[i].append((var_name, value))
                    if backtrack(values, index + 1):
                        return True
                    remaining[i] += value
                    assignments[i].pop()
                elif remaining[i] > 0 and (not assignments[i] or assignments[i][0][0] == var_name):
                    part_value = remaining[i]
                    remaining[i] = 0
                    assignments[i].append((var_name, part_value))
                    if backtrack([(value - part_value, var_name)] + values[index + 1:], 0):
                        return True
                    remaining[i] = part_value
                    assignments[i].pop()
            return False

        if backtrack(values, 0):
            formatted_assignments = {}
            for tank, vars_in_tank in assignments.items():
                if vars_in_tank:
                    formatted_assignments[tank] = ' + '.join(f"{var} ({val})" for var, val in vars_in_tank)
            return formatted_assignments
        else:
            return None

    # Function to sum values safely
    def safe_sum(values, start_day, end_day):
        return sum(values.get(str(day), 0) for day in range(start_day, end_day + 1))

    # Convert start date string to datetime object
    start_date = datetime.strptime(start_date_str, '%Y-%m-%d')

    # Initialize the cumulative values with zeros
    cumulative_values = {
        "ulg95": 0,
        "dk": 0,
        "ultsu": 0,
        "ultdk": 0,
    }
    total_sum = 0

    # Find the first day in the data
    first_day_in_data = min(int(day) for day in ulg95.keys())

    # Initialize the variable to store the last valid day
    last_valid_day = None
    last_valid_values = None
    last_valid_assignments = None

    # Iterate over the days in the data starting from the first day in the data
    for day_key in sorted(ulg95.keys(), key=int):
        day_offset = int(day_key) - first_day_in_data
        current_date = start_date + timedelta(days=day_offset)

        # Add values for the current day
        cumulative_values["ulg95"] += ulg95.get(day_key, 0)
        cumulative_values["dk"] += dk.get(day_key, 0)
        cumulative_values["ultsu"] += ultsu.get(day_key, 0)
        cumulative_values["ultdk"] += ultdk.get(day_key, 0)

        # Calculate the total sum
        total_sum = cumulative_values["ulg95"] + cumulative_values["dk"] + cumulative_values["ultsu"] + \
                    cumulative_values["ultdk"]

        # Check if the total sum is less than 32000
        if total_sum < 32000:
            # Check if the values can fit into the tanks
            assignments = can_fit_in_tanks([(cumulative_values["ulg95"], "ulg95"),
                                            (cumulative_values["dk"], "dk"),
                                            (cumulative_values["ultsu"], "ultsu"),
                                            (cumulative_values["ultdk"], "ultdk")], tanks)
            if assignments:
                # Store the valid state with the current date
                last_valid_day = current_date
                last_valid_values = cumulative_values.copy()
                last_valid_assignments = assignments
        else:
            # If the sum exceeds 32000, stop processing
            break

    # Print the results for the last valid day
    if last_valid_day:
        print(f"Last valid day: {last_valid_day.strftime('%Y-%m-%d')}")
        print("Values:", last_valid_values)
        print("Assignments:")
        for tank_index, assignment in last_valid_assignments.items():
            print(f"  Tank {tank_index + 1} (Capacity {tanks[tank_index]}): {assignment}")
    else:
        print("No valid day found that meets the conditions.")


# Przykład użycia
# data = {
#     "ulg95": {
#         "1": 1000, "2": 2000, "3": 3000, "4": 4000, "5": 5000,
#         "6": 6000, "7": 7000, "8": 8000, "9": 9000, "10": 10000
#     },
#     "dk": {
#         "1": 1000, "2": 2000, "3": 3000, "4": 4000, "5": 5000,
#         "6": 6000, "7": 7000, "8": 8000, "9": 9000, "10": 10000
#     },
#     "ultsu": {
#         "1": 1000, "2": 2000, "3": 3000, "4": 4000, "5": 5000,
#         "6": 6000, "7": 7000, "8": 8000, "9": 9000, "10": 10000
#     },
#     "ultdk": {
#         "1": 1000, "2": 2000, "3": 3000, "4": 4000, "5": 5000,
#         "6": 6000, "7": 7000, "8": 8000, "9": 9000, "10": 10000
#     }
# }
# start_date_str = "2024-01-01"
#
# process_tank_data(data, start_date_str)
