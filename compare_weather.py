import requests
import os
import argparse

from rich import print
from rich.table import Table
from rich.console import Console


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


def print_differences(current_weather, destination_weather, differences):
    console = Console()

    # Creating tables for each city's weather and differences
    current_table = Table(title=f"[bold magenta]Weather in {current_weather['city']}[/bold magenta]")
    destination_table = Table(title=f"[bold cyan]Weather in {destination_weather['city']}[/bold cyan]")
    differences_table = Table(title="[bold yellow]Differences[/bold yellow]")

    # Adding columns to each table
    for table in [current_table, destination_table, differences_table]:
        table.add_column("Attribute", style="dim", width=12)
        table.add_column("Value")

    # Adding rows to each table
    for attribute, value in current_weather.items():
        if attribute != 'city':
            current_table.add_row(attribute, str(value))
    for attribute, value in destination_weather.items():
        if attribute != 'city':
            destination_table.add_row(attribute, str(value))
    for attribute, value in differences.items():
        differences_table.add_row(attribute, str(value))

    # Printing tables
    console.print(current_table)
    console.print(destination_table)
    console.print(differences_table)

def main():
    # Gets the current and destination cities from the user.
    parser = argparse.ArgumentParser(description="Compare weather between two cities.")
    parser.add_argument('-c', '--current', type=str, required=True, help="Name of the current city.")
    parser.add_argument('-d', '--destination', type=str, required=True, help="Name of the destination city.")
    args = parser.parse_args()

    current_city = args.current
    destination_city = args.destination
    
    # Now you can use args.current and args.destination in your code
    current_weather = get_city_weather(current_city)
    destination_weather = get_city_weather(destination_city)
    
    # Using the function with your code
    differences = get_differences(current_weather, destination_weather)
    
    # Sample usage
    differences = get_differences(current_weather, destination_weather)
    print_differences(current_weather, destination_weather, differences)

if __name__ == '__main__':
    main()