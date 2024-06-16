def calculate_trips_left(distance: float, brake_pads_km_left: int, oil_change_km_left: int):
    if distance <= 0:
        raise ValueError("Distance must be greater than zero.")
    
    one_trip_distance = 2 * distance
    
    brake_pads_trips_left = brake_pads_km_left // one_trip_distance
    
    oil_change_trips_left = oil_change_km_left // one_trip_distance
    
    return {"brake_pads_trips_left": brake_pads_trips_left, "oil_change_trips_left":oil_change_trips_left}