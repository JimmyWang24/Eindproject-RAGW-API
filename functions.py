# Import the required modules
import requests
import os

# Allows the application to read and write files in the virtual enviroment
from dotenv import load_dotenv
load_dotenv()

# All static variables
BASE_URL = "https://api.rawg.io/api"
API_KEY = os.getenv("RAWG_API_KEY")
FAVORITE_FILE = "favorite_games.txt"
HIGHSCORE_FILE = "minigame_highscores.txt"

# Sends request to API to get data
def get_data(endpoint, params=None):
    if params is None: # Makes a dictionary to avoid syntax error in case of no parameter input
        params = {}
    params["key"] = API_KEY
    try: # Sends a request to the endpoint and parameters depending on user input
        response = requests.get(f"{BASE_URL}/{endpoint}", params=params)
        response.raise_for_status()
        games = response.json()
        return games
    except requests.exceptions.RequestException as error: # Shows error message incase request failed
        print(f"Er is een fout opgetreden bij het ophalen van de data: {error}")
        return None

# The main menu of the application
def main_menu():
    while True:
        print("""
        Main Menu
        1. Search a videogame
        2. Recommended videogames
        3. Your favourite videogames
        4. Quit application
        """)

        menu_choice = (input("Enter the corrosponding key to continue: "))
        if menu_choice == "1":
            search_menu()
        elif menu_choice == "2":
            top_games_menu()
        elif menu_choice == "3":
            favourite_menu()
        elif menu_choice == "4":
            quit_application()
        else:
            print("Invalid input, please enter a valid input")

# Allows the player to input a specific game title to search for
def search_menu():
    while True:
        game_name = input("Enter the name of the game you want to search: ")
        params = {"search": game_name,"key": API_KEY, "page_size": 1}
        games = get_data("games", params)

        if games and "results" in games and games["results"]: # Checks if the returned response isn't empty
            game = games["results"][0]
            print(f"""
            Titel: {game["name"]}
            Genre: {game["genres"][0]["name"]}
            Platform: {game["platforms"][0]["platform"]["name"]}
            Release date: {game["released"]}
            Rating: {game["rating"]}/5
            """)
            save_to_favorites(game["name"]) # See save_to_favorites function
            repeat() # See repeat function
        else:
            print("No games found.")

# Allows the user to search for the 10 highest rated games in a specific genre that they get to choose
def top_games_menu():
    while True:
        genres = get_data("genres")
        if genres and "results" in genres and genres["results"]: # Checks if the returned response isn't empty
            print("Available genres:")
            for index, genre in enumerate(genres["results"], 1):
                print(f"{index}. {genre["name"]}") # Makes and shows an ordered list of game genres
            try:
                choice = int(input("Enter the index number of the genre: ")) -1
                if 0 <= choice < len(genres["results"]):
                    genre_choice = genres["results"][choice]["id"]
                    params = {"genres": genre_choice, "page_size": 10, "ordering": "-rating"} # Orders the games from highest rating to lowest
                    games = get_data("games", params)
                    if games and "results" in games and games["results"]: # Checks if the returned response isn't empty
                        print(f"Top 10 games in {genres["results"][choice]["name"]}")
                        for index, game in enumerate(games["results"], 1):
                            print(f"{index}. {game["name"]} (rating: {game["rating"]}/5)") # Shows the user the list of top 10 rated games in that genre with their rating
                        repeat() # See repeat function
                    else:
                        print("No games found.")
                else:
                    print("Invalid input, please enter a valid input")
            except ValueError:
                print("Invalid input, please enter a valid input")
        else:
            print("No genres found.")

# Asks the player if they'd like to repeat the function that this function is nested in
def repeat():
    while True:
        repeat_input = input("Would you like to search again? (yes/no): ").lower()
        if repeat_input == "yes":
            break
        elif repeat_input == "no":
            main_menu()
        else:
            print("Invalid input, please enter a valid input")

# Asks if the player would like to save the searched game to their favorite list
def save_to_favorites(game):
    try:
        with open(FAVORITE_FILE, "r") as favorites:
            favorite_list = favorites.read().splitlines() # Reads the content of the file as a list with seperated items.
    except FileNotFoundError:
        favorite_list = [] # Creates the list if it isn't made yet.

    while True:
        add_to_favorites = input("Would like like to add this game to your favorite list? (yes/no) ").lower()
        if add_to_favorites == "yes":
            if game.strip() not in favorite_list: # Checks if the game isn't already added. Also .strip removes the empty lines and spaces to avoid confusion when reading the file
                with open(FAVORITE_FILE, "a") as favorites: # Appends (adds) the item to the list
                    favorites.write(f"{game.strip()}\n")
                    print(f"{game} has been added to your favorite list.")
                break
            else:
                print(f"{game} is already in your favorite list.")
                break
        elif add_to_favorites == "no":
            break
        else:
            print("Invalid input, please enter a valid input")

# Allows the user to see the game titles they've added to their favorite list
def favourite_menu():
    with open(FAVORITE_FILE, "r") as f: # Allows the application to read the file
        favorites = f.readlines()
    if favorites: # Checks if the list isn't empty
        print("Your favorite games:")
        for index,game in enumerate(favorites, 1):
            print(f"{index}. {game.strip()}")
    else:
        print("No favorite games found.")
    input("Enter any key to continue: ")

# Quits the application
def quit_application():
    print("Have a nice day!")
    exit()