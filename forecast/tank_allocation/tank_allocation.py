from datetime import datetime, timedelta


def process_tank_data(data, start_date_str, station_id):
    # Initialize variables and divide all values by 2
    ulg95 = {k: v for k, v in data['ulg95'].items()}
    dk = {k: v for k, v in data['dk'].items()}
    ultsu = {k: v for k, v in data['ultsu'].items()}
    ultdk = {k: v for k, v in data['ultdk'].items()}

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
                    formatted_assignments[tank] = dict((var, val) for var, val in vars_in_tank)
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
        response = []
        for tank_index, assignment in last_valid_assignments.items():
            response_tank = {
                    "station_id": station_id,
                    "date": last_valid_day.strftime('%Y-%m-%d'),
                    "capacity": tanks[tank_index],
                    "tank_id": tank_index + 1,
                }
            for fuel_type in ["ulg95", "dk", "ultsu", "ultdk"]:
                value = assignment.get(fuel_type) if assignment.get(fuel_type) else 0
                response_tank[fuel_type] = value
            response.append(response_tank)
        return response
    else:
        raise Exception("No valid day found that meets the conditions.")
