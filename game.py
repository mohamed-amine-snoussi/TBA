# Description: Game class

# Import modules
DEBUG = False


from room import Room
from player import Player
from command import Command
from actions import Actions
from item import Item
from character import Character

class Game:

    # Constructor
    def __init__(self):
        self.finished = False
        self.rooms = []
        self.commands = {}
        self.player = None
        self.history = []   
    
    # Setup the game
    def setup(self):

        # Setup commands

        help = Command("help", " : afficher cette aide", Actions.help, 0)
        self.commands["help"] = help
        quit = Command("quit", " : quitter le jeu", Actions.quit, 0)
        self.commands["quit"] = quit
        go = Command("go", " <direction> : se déplacer dans une direction cardinale (N, E, S, O, U, D ou nord, sud, est, ouest, haut, bas)", Actions.go, 1)
        self.commands["go"] = go
        history = Command("history", " : afficher l'historique des salles visitées", Actions.history, 0)
        self.commands["history"] = history
        back = Command("back", " : revenir à la salle précédente", Actions.back, 0)
        self.commands["back"] = back
        take = Command("take", " <objet> : ramasser un objet", Actions.take, 1)
        self.commands["take"] = take
        drop = Command("drop", " <objet> : déposer un objet", Actions.drop, 1)
        self.commands["drop"] = drop
        inventory = Command("inventory", " : afficher votre inventaire", Actions.inventory, 0)
        self.commands["inventory"] = inventory
        look = Command("look", " : observer les objets présents", Actions.look, 0)
        self.commands["look"] = look
        check = Command("check", " : afficher l'inventaire", Actions.check, 0)
        self.commands["check"] = check
        talk = Command("talk", " <personne> : parler à un personnage", Actions.talk, 1)
        self.commands["talk"] = talk

        

        
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
        interrogatoire = Room("Salle d'interrogatoire","une salle froide éclairée par un néon, avec une table métallique et un miroir sans tain.")
        self.rooms.append(interrogatoire)
        archives = Room("Archives municipales","une salle remplie d'étagères poussiéreuses contenant des dossiers très anciens.")
        self.rooms.append(archives)
        local_tech = Room("Local technique du métro","une pièce étroite remplie de câbles, de plans et de coffres métalliques.")
        self.rooms.append(local_tech)

        temoin = Character("Témoin","Un homme nerveux qui semble cacher quelque chose.",interrogatoire,[
        "J'ai vu des gens avec un symbole de lys entrer dans l'hôtel tard le soir...",
        "Ils avaient l'air pressés. Comme s'ils fuyaient quelqu'un.",
        "Je ne veux pas d'ennuis... mais la Place du Lys cache quelque chose."])

        archiviste = Character("Archiviste","Une employée fatiguée mais curieuse.",archives,[
        "Ces dossiers... le LYS revient dans les archives depuis des décennies.",
        "On a déjà essayé d'enterrer cette affaire. Plusieurs fois.",
        "Si vous cherchez une entrée, regardez du côté du métro désaffecté."])

        technicien = Character("Technicien","Un ancien agent du métro au regard méfiant.",local_tech,[
        "Le local technique ? Il est verrouillé pour une bonne raison.",
        "Sans plan d'accès, impossible d'entrer. La carte est essentielle.",
        "Une clé lourde ouvre une grille... mais je ne dis pas laquelle."])


        #setup items
        badge = Item("badge", "Badge d'accès réservé au personnel du poste", 0.05)
        dossier = Item("dossier", "Dossier secret portant le sceau du LYS", 0.30)
        photo = Item("photo", "Photographie montrant une réunion secrète du LYS", 0.02)
        carte = Item("carte", "Carte indiquant un passage scellé sous la place", 0.05)
        dictaphone = Item("dictaphone", "Dictaphone contenant un message chiffré", 0.25)
        cle_lourde = Item("cle_lourde", "Clé massive permettant d'ouvrir une grille sécurisée", 0.80)
        temoignage = Item("temoignage","Compte rendu d'un témoin évoquant des réunions secrètes du LYS",0.05)
        dossier_archives = Item("dossier_archives","Dossiers anciens reliant le LYS à des affaires passées",0.40)
        disque_dur = Item("disque_dur","Disque dur chiffré contenant des preuves compromettantes",0.50)




        # Placement des objets dans les salles
        poste.items.append(badge)
        hotel.items.append(dossier)
        chambre.items.append(photo)
        toit.items.append(dictaphone)
        place.items.append(carte)
        interrogatoire.items.append(temoignage)
        archives.items.append(dossier_archives)
        local_tech.items.append(cle_lourde)
        salle_secrete.items.append(disque_dur)



        # Create exits for rooms

        poste.exits = {"N" : ruelle, "D" : interrogatoire}
        ruelle.exits = {"S" : poste, "E" : hotel, "N" : place}
        hotel.exits = {"O" : ruelle, "U" : chambre}
        chambre.exits = {"D" : hotel, "E" : toit}
        toit.exits = {"O" : chambre}
        place.exits = {"S" : ruelle, "E" : metro, "N" : archives}
        metro.exits = {"O" : place, "D" : salle_secrete, "E" : local_tech}
        salle_secrete.exits = {"U" : metro}
        local_tech.exits = {"O" : metro}
        interrogatoire.exits = {"U": poste}
        archives.exits = {"S": place}


        # Setup player and starting room

        self.player = Player(input("\nEntrez votre nom: "))
        self.player.current_room = poste
        self.history.append(self.player.current_room)


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
        for room in self.rooms:
            for character in room.characters[:]:
                character.move(debug=DEBUG)

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
