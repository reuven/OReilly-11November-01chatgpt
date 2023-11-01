import requests
import os
import argparse

def get_city_weather(city_name):

    base_url = "http://api.openweathermap.org/data/2.5/weather"
    api_key = os.environ.get("OPENWEATHER_API_KEY")
    
    params = {
        'q': city_name,
        'appid': api_key,
        'units': 'metric'
    }
    
    try:
        r = requests.get(base_url, params=params)
        r.raise_for_status()  # Raise an error for bad responses
        
        data = r.json()
        if 'main' in data:
            temperature = data['main']['temp']
            humidity = data['main']['humidity']
            precipitation = data["rain"]["1h"] if "rain" in data else 0  # Assumes rain data is in mm/h
            
            return {'temp':temperature, 'humidity':humidity, 'precipitation':precipitation}
        else:
            print("Error retrieving weather data.")
    
    except requests.RequestException as e:
        print(f"Error fetching data from OpenWeatherMap: {e}")


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

def main():
    # Gets the current and destination cities from the user.
    parser = argparse.ArgumentParser(description="Compare weather between two cities.")
    parser.add_argument('-c', '--current', type=str, required=True, help="Name of the current city.")
    parser.add_argument('-d', '--destination', type=str, required=True, help="Name of the destination city.")
    args = parser.parse_args()
    
    # Now you can use args.current and args.destination in your code
    current_weather = get_city_weather(args.current)
    destination_weather = get_city_weather(args.destination)
    
    # Using the function with your code
    differences = get_differences(current_weather, destination_weather)
    
    # Sample usage
    differences = get_differences(current_weather, destination_weather)
    print_differences(current_city, current_weather, destination_city, destination_weather, differences)