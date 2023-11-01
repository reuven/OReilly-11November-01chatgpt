import pytest
import requests
from compare_weather import get_city_weather

def test_get_city_weather_success(mocker):
    # Mocking the requests.get() method to return a successful response
    mock_response = mocker.Mock()
    mock_response.json.return_value = {
        'main': {
            'temp': 25.5,
            'humidity': 60
        },
        'rain': {
            '1h': 5
        }
    }
    mock_response.raise_for_status.return_value = None
    mocker.patch('requests.get', return_value=mock_response)

    result = get_city_weather('TestCity')
    assert result == {'temp': 25.5, 'humidity': 60, 'precipitation': 5}

def test_get_city_weather_no_rain(mocker):
    # Mocking the requests.get() method to return a successful response with no rain
    mock_response = mocker.Mock()
    mock_response.json.return_value = {
        'main': {
            'temp': 25.5,
            'humidity': 60
        }
    }
    mock_response.raise_for_status.return_value = None
    mocker.patch('requests.get', return_value=mock_response)

    result = get_city_weather('TestCity')
    assert result == {'temp': 25.5, 'humidity': 60, 'precipitation': 0}

def test_get_city_weather_request_exception(mocker, capsys):
    # Mocking the requests.get() method to raise an exception
    mocker.patch('requests.get', side_effect=requests.RequestException("Test Error"))

    result = get_city_weather('TestCity')
    captured = capsys.readouterr()
    assert "Error fetching data from OpenWeatherMap: Test Error" in captured.out
    assert result is None

def test_get_city_weather_invalid_data(mocker, capsys):
    # Mocking the requests.get() method to return an invalid response without 'main' key
    mock_response = mocker.Mock()
    mock_response.json.return_value = {}
    mock_response.raise_for_status.return_value = None
    mocker.patch('requests.get', return_value=mock_response)

    result = get_city_weather('TestCity')
    captured = capsys.readouterr()
    assert "Error retrieving weather data." in captured.out
    assert result is None
