# Gets the current and destination cities from the user.
current_city = input('Enter current city: ').strip()
destination_city = input('Enter destination city: ').strip()

# Get the weather for my current city, and put into a data structure.
current_weather = get_city_weather(current_city)

# Get the weather for the destination city, and put into a data structure.
destination_weather = get_city_weather(destination_city)

# Compare the two weather reports, and put into a third data structure.
def get_differences(current_weather, destination_weather):
    # Check if there are errors in either of the weather data
    if 'error' in current_weather:
        return {'error': f"Error in current city data: {current_weather['error']}"}
    if 'error' in destination_weather:
        return {'error': f"Error in destination city data: {destination_weather['error']}"}

    # Calculate differences
    temp_difference = destination_weather['temp'] - current_weather['temp']
    humidity_difference = destination_weather['humidity'] - current_weather['humidity']
    precipitation_difference = destination_weather['precipitation'] - current_weather['precipitation']

    # Return the differences as a dictionary
    return {
        'temp_diff': temp_difference,
        'humidity_diff': humidity_difference,
        'precipitation_diff': precipitation_difference
    }

# Using the function with your code
differences = get_differences(current_weather, destination_weather)


# Pass all three data structures to a function that displays them nicely for the user.
def print_differences(current_city, current_weather, destination_city, destination_weather, differences):
    print(f"Weather for {current_city}:")
    print(f"Temperature: {current_weather['temp']}°C")
    print(f"Humidity: {current_weather['humidity']}%")
    print(f"Precipitation: {current_weather['precipitation']}mm/h\n")

    print(f"Weather for {destination_city}:")
    print(f"Temperature: {destination_weather['temp']}°C")
    print(f"Humidity: {destination_weather['humidity']}%")
    print(f"Precipitation: {destination_weather['precipitation']}mm/h\n")

    print("Differences between the two cities:")
    print(f"Temperature Difference: {differences['temp_diff']}°C")
    print(f"Humidity Difference: {differences['humidity_diff']}%")
    print(f"Precipitation Difference: {differences['precipitation_diff']}mm/h")

# Sample usage
differences = get_differences(current_weather, destination_weather)
print_differences(current_city, current_weather, destination_city, destination_weather, differences)