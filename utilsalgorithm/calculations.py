def calculate_trips_left(distance: float, deliveries_count: int, durability_in_km: int):
    one_trip_distance = 2 * distance
    
    component_km_left = durability_in_km - one_trip_distance * deliveries_count
    component_trips_left = component_km_left // one_trip_distance

    return component_km_left, component_trips_left