# Description: Game class

# Import modules

from room import Room
from player import Player
from command import Command
from actions import Actions

class Game:

    # Constructor
    def __init__(self):
        self.finished = False
        self.rooms = []
        self.commands = {}
        self.player = None
    
    # Setup the game
    def setup(self):

        # Setup commands

        help = Command("help", " : afficher cette aide", Actions.help, 0)
        self.commands["help"] = help
        quit = Command("quit", " : quitter le jeu", Actions.quit, 0)
        self.commands["quit"] = quit
        go = Command("go", " <direction> : se déplacer dans une direction cardinale (N, E, S, O, U, D ou nord, sud, est, ouest, haut, bas)", Actions.go, 1)
        self.commands["go"] = go
        
        # Setup rooms

        poste = Room("Poste de Police", "le hall du poste de police, rempli de dossiers et de cartes accrochées au mur.")
        self.rooms.append(poste)
        ruelle = Room("Ruelle du centre", "une ruelle étroite et sombre, encore marquée par des graffitis en forme de lys.")
        self.rooms.append(ruelle)
        hotel = Room("Hôtel abandonné", "le hall décrépit d'un ancien hôtel, condamné depuis une affaire jamais élucidée.")
        self.rooms.append(hotel)
        toit = Room("Toit de l'immeuble", "le toit de l'immeuble, balayé par le vent, avec vue sur la ville.")
        self.rooms.append(toit)
        chambre = Room("Chambre 407", "une chambre en désordre où un crime lié au LYS a été commis.")
        self.rooms.append(chambre)
        place = Room("Place du Lys", "une grande place dominée par une statue représentant un lys stylisé.")
        self.rooms.append(place)
        metro = Room("Métro désaffecté", "un quai de métro abandonné, plongé dans la pénombre.")
        self.rooms.append(metro)
        salle_secrete = Room("Salle secrète du LYS", "une salle cachée, remplie de dossiers brûlés et de symboles du LYS.")
        self.rooms.append(salle_secrete)

        # Create exits for rooms

        poste.exits = {"N" : ruelle}
        ruelle.exits = {"S" : poste, "E" : hotel, "N" : place}
        hotel.exits = {"O" : ruelle, "U" : chambre}
        chambre.exits = {"D" : hotel, "E" : toit}
        toit.exits = {"O" : chambre}
        place.exits = {"S" : ruelle, "E" : metro}
        metro.exits = {"O" : place, "D" : salle_secrete}
        salle_secrete.exits = {"U" : metro}
        # Setup player and starting room

        self.player = Player(input("\nEntrez votre nom: "))
        self.player.current_room = poste

    # Play the game
    def play(self):
        self.setup()
        self.print_welcome()
        # Loop until the game is finished
        while not self.finished:
            # Get the command from the player
            self.process_command(input("> "))
        return None

    # Process the command entered by the player
    def process_command(self, command_string) -> None:

        # Split the command string into a list of words
        list_of_words = command_string.split(" ")

        command_word = list_of_words[0]

        # If the command is not recognized, print an error message
        if command_string.strip() == "":
            return
        if command_word not in self.commands.keys(): 
            print(f"\nCommande '{command_word}' non reconnue. Entrez 'help' pour voir la liste des commandes disponibles.\n")
        # If the command is recognized, execute it
        else:
            command = self.commands[command_word]
            command.action(self, list_of_words, command.number_of_parameters)

    # Print the welcome message
    def print_welcome(self):
        print(f"\nBienvenue {self.player.name} dans ce jeu d'aventure !")
        print("Entrez 'help' si vous avez besoin d'aide.")
        #
        print(self.player.current_room.get_long_description())
    

def main():
    # Create a game object and play the game
    Game().play()
    

if __name__ == "__main__":
    main()
