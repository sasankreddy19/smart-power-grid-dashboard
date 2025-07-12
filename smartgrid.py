def estimate_demand(temp, humidity):
    base_load = 100  # kW
    if temp > 30:
        base_load += (temp - 30) * 5
    if humidity > 70:
        base_load += 10
    return round(base_load, 2)

def estimate_solar_output(radiation):
    max_capacity = 500  # kW
    output = (radiation / 1000) * max_capacity
    return round(output, 2)