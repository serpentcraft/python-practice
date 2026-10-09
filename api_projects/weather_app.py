import requests
from prettytable import PrettyTable
from colorama import Fore, Style, init

init()

class CityWeather:
    def __init__(self, city, temp, humidity, wind_speed):
        self.city = city
        self.temp = temp
        self.humidity = humidity
        self.wind_speed = wind_speed

    def to_row(self):
        """Returns a row to add to a table."""
        return [self.city, self.temp, self.humidity, self.wind_speed]

def get_json(url):
    """Making a request and returns JSON or None if not available."""
    try:
        response = requests.get(url)
        return response.json()
    except requests.RequestException:
        print(f"Network error for URL: {url}")
        return None

def color_temp(temp):
    """Returns temperature colored according to degrees info."""
    if temp < 0:
        color = Fore.BLUE + Style.BRIGHT
    elif temp < 10:
        color = Fore.CYAN
    elif temp < 20:
        color = Fore.GREEN
    elif temp < 30:
        color = Fore.YELLOW
    else:
        color = Fore.RED + Style.BRIGHT

    return f"{color}{temp}{Style.RESET_ALL}"

def color_humidity(humidity):
    """Returns humidity colored according to the info."""
    if humidity > 80:
        return f"{Fore.CYAN}{humidity}{Style.RESET_ALL}"
    elif humidity < 30:
        return f"{Fore.YELLOW}{humidity}{Style.RESET_ALL}"
    else:
        return f"{Fore.GREEN}{humidity}{Style.RESET_ALL}"


def color_wind(wind_speed):
    """Returns wind speed colored according to the info."""
    if wind_speed > 20:
        return f"{Fore.RED}{wind_speed}{Style.RESET_ALL}"
    elif wind_speed < 5:
        return f"{Fore.GREEN}{wind_speed}{Style.RESET_ALL}"
    else:
        return f"{Fore.YELLOW}{wind_speed}{Style.RESET_ALL}"

# Asking for cities
cities_input = input("Enter cities (comma-separated): ")
cities = [c.strip() for c in cities_input.split(",")]
print(f"City Weather Information is being processed...")

# Creating a table
table = PrettyTable()
table.title = "Weather Information"
table.field_names = ["City", "Temperature °C", "Humidity %", "Wind speed km/h"]

# Cities loop
for city in cities:
    # 1. Geocoding
    geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1&language=en"
    geo_data = get_json(geo_url)

    if geo_data is None or "results" not in geo_data:
        print(f"City '{city}' not found.")
        continue

    city_info = geo_data["results"][0]
    latitude = city_info["latitude"]
    longitude = city_info["longitude"]

    # 2. Forecast
    meteo_url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current=temperature_2m,relative_humidity_2m,wind_speed_10m"
    weather_data = get_json(meteo_url)

    if weather_data is None:
        print(f"Weather data not available for {city}.")
        continue

    current = weather_data["current"]
    temp = current["temperature_2m"]
    humidity = current["relative_humidity_2m"]
    wind_speed = current["wind_speed_10m"]

    # 3. Adding row(s) to a table
    city_weather = CityWeather(city, temp, humidity, wind_speed)
    table.add_row([
        city,
        color_temp(temp),
        color_humidity(humidity),
        color_wind(wind_speed)
    ])

# 4. Printing a table and legends for it 
print(f"\n{table}")

print(f"\nTemperature: "
      f"{Fore.BLUE}■{Style.RESET_ALL} < 0°C  "
      f"{Fore.CYAN}■{Style.RESET_ALL} 0–10°C  "
      f"{Fore.GREEN}■{Style.RESET_ALL} 10–20°C  "
      f"{Fore.YELLOW}■{Style.RESET_ALL} 20–30°C  "
      f"{Fore.RED}■{Style.RESET_ALL} > 30°C")

print(f"Humidity:    "
      f"{Fore.YELLOW}■{Style.RESET_ALL} < 30%  "
      f"{Fore.GREEN}■{Style.RESET_ALL} 30–80%  "
      f"{Fore.CYAN}■{Style.RESET_ALL} > 80%")

print(f"Wind:        "
      f"{Fore.GREEN}■{Style.RESET_ALL} < 5 km/h  "
      f"{Fore.YELLOW}■{Style.RESET_ALL} 5–20 km/h  "
      f"{Fore.RED}■{Style.RESET_ALL} > 20 km/h")

count = len(cities)
word = "city" if count == 1 else "cities"
print(f"\nProcessed {count} {word}.")
