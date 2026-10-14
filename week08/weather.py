import argparse
import importlib.util
import os
import sys
from pathlib import Path

if __package__:
    from week08.favorites import FavoritesManager
    from week08.weather_api import WeatherAPI, format_current_weather, format_forecast
else:
    from favorites import FavoritesManager
    from weather_api import WeatherAPI, format_current_weather, format_forecast


FAVORITES_FILE = Path(__file__).with_name("favorites.json")


def load_api_key():
    api_key = os.environ.get("WEATHER_API_KEY")
    if api_key:
        return api_key

    config_path = Path(__file__).with_name("config.py")
    if not config_path.is_file():
        return None

    spec = importlib.util.spec_from_file_location("week08_local_config", config_path)
    if spec is None or spec.loader is None:
        return None

    config = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(config)
    api_key = getattr(config, "WEATHER_API_KEY", None)
    if not isinstance(api_key, str) or not api_key or api_key == "YOUR_API_KEY_HERE":
        return None
    return api_key


def build_parser():
    parser = argparse.ArgumentParser(description="Get weather and manage favorite locations.")
    commands = parser.add_subparsers(dest="command", required=True)

    current_parser = commands.add_parser("current", help="Show current weather.")
    current_parser.add_argument("location", help="A location or saved favorite name.")

    forecast_parser = commands.add_parser("forecast", help="Show a weather forecast.")
    forecast_parser.add_argument("location", help="A location or saved favorite name.")
    forecast_parser.add_argument("--days", type=int, default=3)

    favorites_parser = commands.add_parser("favorites", help="Manage favorite locations.")
    favorite_commands = favorites_parser.add_subparsers(
        dest="favorites_command", required=True
    )

    add_parser = favorite_commands.add_parser("add", help="Add a favorite.")
    add_parser.add_argument("name")
    add_parser.add_argument("location")

    favorite_commands.add_parser("list", help="List saved favorites.")

    remove_parser = favorite_commands.add_parser("remove", help="Remove a favorite.")
    remove_parser.add_argument("name")
    return parser


def main(argv=None) -> int:
    args = build_parser().parse_args(argv)
    favorites = FavoritesManager(FAVORITES_FILE)

    if args.command == "favorites":
        if args.favorites_command == "add":
            if not favorites.add(args.name, args.location):
                print(f"Favorite already exists: {args.name}", file=sys.stderr)
                return 1
            return 0

        if args.favorites_command == "list":
            for name, location in favorites.list_all().items():
                print(f"{name}: {location}")
            return 0

        if not favorites.remove(args.name):
            print(f"Favorite not found: {args.name}", file=sys.stderr)
            return 1
        return 0

    api_key = load_api_key()
    if not api_key:
        print("Error: missing WeatherAPI API key.", file=sys.stderr)
        return 1

    location = favorites.get_location(args.location) or args.location
    client = WeatherAPI(api_key)

    try:
        if args.command == "current":
            data = client.get_current_weather(location)
            formatter = format_current_weather
        else:
            data = client.get_forecast(location, days=args.days)
            formatter = format_forecast
    except ValueError as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1

    if data is None:
        print("Error: weather request failed.", file=sys.stderr)
        return 1

    print(formatter(data))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
