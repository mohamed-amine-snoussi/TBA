# Description: Game class

# Import modules
DEBUG = False
from pathlib import Path
import sys

# Tkinter imports for GUI
import tkinter as tk
from tkinter import ttk, simpledialog

from room import Room
from player import Player
from command import Command
from actions import Actions
from item import Item
from character import Character, StaticCharacter
from quest import Quest, QuestManager

class Game:

    # Constructor
    def __init__(self):
        self.finished = False
        self.rooms = []
        self.commands = {}
        self.player = None
        self.history = []
        self.quest_manager = None
    
    # Setup the game
    def setup(self, player_name=None):

        # Setup commands

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
        quests = Command("quests", " : lister toutes les quêtes", Actions.quests, 0)
        self.commands["quests"] = quests
        quest = Command("quest", " <nom> : détails d'une quête", Actions.quest, 1)
        self.commands["quest"] = quest
        activate = Command("activate", " <nom> ou 'quests' : activer une quête spécifique ou toutes les quêtes disponibles", Actions.activate, 1)
        self.commands["activate"] = activate
        rewards = Command("rewards", " : lister vos récompenses", Actions.rewards, 0)
        self.commands["rewards"] = rewards

        

        
        # Setup rooms

        poste = Room("Poste de Police", "le hall du poste de police, rempli de dossiers et de cartes accrochées au mur.", "police.png")
        self.rooms.append(poste)
        ruelle = Room("Ruelle du centre", "une ruelle étroite et sombre, encore marquée par des graffitis en forme de lys.", "street.png")
        self.rooms.append(ruelle)
        hotel = Room("Hôtel abandonné", "le hall décrépit d'un ancien hôtel, condamné depuis une affaire jamais élucidée.", "hotel.png")
        self.rooms.append(hotel)
        toit = Room("Toit de l'immeuble", "le toit de l'immeuble, balayé par le vent, avec vue sur la ville.", "roof.png")
        self.rooms.append(toit)
        chambre = Room("Chambre 407", "une chambre en désordre où un crime lié au LYS a été commis.", "bedroom.png")
        self.rooms.append(chambre)
        place = Room("Place du Lys", "une grande place dominée par une statue représentant un lys stylisé.", "square.png")
        self.rooms.append(place)
        metro = Room("Métro désaffecté", "un quai de métro abandonné, plongé dans la pénombre.", "metro.png")
        self.rooms.append(metro)
        salle_secrete = Room("Salle secrète du LYS", "une salle cachée, remplie de dossiers brûlés et de symboles du LYS.", "secret.png")
        self.rooms.append(salle_secrete)
        interrogatoire = Room("Salle d'interrogatoire","une salle froide éclairée par un néon, avec une table métallique et un miroir sans tain.", "interrogation.png")
        self.rooms.append(interrogatoire)
        archives = Room("Archives municipales","une salle remplie d'étagères poussiéreuses contenant des dossiers très anciens.", "archives.png")
        self.rooms.append(archives)
        local_tech = Room("Local technique du métro","une pièce étroite remplie de câbles, de plans et de coffres métalliques.", "technical.png")
        self.rooms.append(local_tech)

        temoin = Character("Témoin","Un homme nerveux qui semble cacher quelque chose.",interrogatoire,[
        "J'ai vu des gens avec un symbole de lys entrer dans l'hôtel tard le soir...",
        "Ils avaient l'air pressés. Comme s'ils fuyaient quelqu'un.",
        "Je ne veux pas d'ennuis... mais la Place du Lys cache quelque chose."])
        interrogatoire.characters.append(temoin)

        archiviste = Character("Archiviste","Une employée fatiguée mais curieuse.",archives,[
        "Ces dossiers... le LYS revient dans les archives depuis des décennies.",
        "On a déjà essayé d'enterrer cette affaire. Plusieurs fois.",
        "Si vous cherchez une entrée, regardez du côté du métro désaffecté."])
        archives.characters.append(archiviste)

        technicien = Character("Technicien","Un ancien agent du métro au regard méfiant.",local_tech,[
        "Le local technique ? Il est verrouillé pour une bonne raison.",
        "Sans plan d'accès, impossible d'entrer. La carte est essentielle.",
        "Une clé lourde ouvre une grille... mais je ne dis pas laquelle."])
        local_tech.characters.append(technicien)

        homme_mysterieux = StaticCharacter("Homme_Mysterieux","Un homme en long manteau noir, le visage dissimulé dans l'ombre. Son regard vous glace le sang.",ruelle,[
        "Vous n'auriez pas dû me parler...",
        "La curiosité tue, n'est-ce pas ?",
        "Adieu, détective."], is_static=True)


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

        if player_name is None:
            player_name = input("\nEntrez votre nom: ")
        self.player = Player(player_name)
        self.player.current_room = poste
        self.history.append(self.player.current_room)

        self.quest_manager = QuestManager(self.player)

        # Setup quests
        quest1 = Quest("collecter_preuves", "Rassembler les 8 indices sur l'affaire du LYS : badge, dossier, photo, carte, dictaphone, cle_lourde, temoignage, dossier_archives.", ["badge", "dossier", "photo", "carte", "dictaphone", "cle_lourde", "temoignage", "dossier_archives"], ["Indices rassemblés"], self.quest_manager)
        self.quest_manager.add_quest(quest1)
        quest2 = Quest("interroger_suspects", "Parler aux 3 personnages clés : Témoin, Archiviste, Technicien.", ["temoin", "archiviste", "technicien"], ["Informations cruciales"], self.quest_manager)
        self.quest_manager.add_quest(quest2)
        quest3 = Quest("acces_salle_secrete", "Accéder à la salle secrète du LYS.", ["salle_secrete"], ["Accès aux zones secrètes"], self.quest_manager, ["collecter_preuves", "interroger_suspects"])
        self.quest_manager.add_quest(quest3)
        quest4 = Quest("recuperer_disque_dur", "Récupérer le disque dur chiffré dans la salle secrète.", ["disque_dur"], ["Victoire sur l'affaire du LYS"], self.quest_manager, ["acces_salle_secrete"])
        self.quest_manager.add_quest(quest4)

        # Activer les quêtes sans prérequis
        self.quest_manager.check_and_activate_quests()


    # Play the game
    def play(self):
        self.setup()
        self.print_welcome()
        # Loop until the game is finished
        while not self.finished:
            # Get the command from the player
            self.process_command(input("> "))
            if self.win():
                print(f"\nFélicitations {self.player.name}, vous avez résolu l'affaire du LYS !")
                self.finished = True
            elif self.loose():
                print(f"\n💀 GAME OVER 💀")
                print(f"\nL'homme mystérieux vous a tué, {self.player.name}. Vous êtes mort dans la ruelle sombre...")
                print(f"Peut-être auriez-vous dû éviter de lui parler...\n")
                self.finished = True
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
        if command_word not in ["look", "talk"]:
            for room in self.rooms:
                for character in room.characters[:]:
                    character.move(debug=DEBUG)

    def win(self):
        """Vérifie si le joueur a gagné."""
        quest = self.quest_manager.get_quest("recuperer_disque_dur")
        return quest and quest.is_completed()

    def loose(self):
        """Vérifie si le joueur a perdu."""
        # Vérifier si le joueur a été tué par l'homme mystérieux
        return hasattr(self.player, 'is_dead') and self.player.is_dead

    # Print the welcome message
    def print_welcome(self):
        print(f"\nBienvenue {self.player.name} dans ce jeu d'aventure !")
        print("Entrez 'help' si vous avez besoin d'aide.")
        #
        print(self.player.current_room.get_long_description())
    

class _StdoutRedirector:
    """Redirect stdout to a Tkinter Text widget."""

    def __init__(self, text_widget):
        self.text_widget = text_widget
        self.original_stdout = sys.stdout

    def write(self, string):
        """Write to the text widget instead of stdout."""
        self.text_widget.insert(tk.END, string)
        self.text_widget.see(tk.END)  # Auto-scroll to end

    def flush(self):
        """Required for file-like objects."""
        pass


class GameGUI(tk.Tk):
    """Main GUI class for the game."""

    IMAGE_WIDTH = 500
    IMAGE_HEIGHT = 350

    def __init__(self):
        super().__init__()
        self.title("Jeu d'Aventure - L'Affaire du LYS")
        self.geometry("900x700")
        self.resizable(True, True)
        # Style moderne
        self.configure(bg='#2C3E50')
        style = ttk.Style()
        style.configure('TFrame', background='#2C3E50')
        style.configure('TButton', font=('Helvetica', 10), padding=5)
        style.configure('TLabel', background='#2C3E50', foreground='white')

        # Initialize game
        player_name = simpledialog.askstring("Nom du joueur", "Entrez votre nom:")
        if not player_name:
            player_name = "Joueur"
        self.game = Game()
        self.game.setup(player_name)

        # Redirect stdout to GUI
        self.original_stdout = sys.stdout
        sys.stdout = _StdoutRedirector(self._create_output_area())

        # Setup GUI
        self._setup_gui()

        # Print welcome message
        self.game.print_welcome()

    def _create_output_area(self):
        """Create and return the output text area."""
        # L0 Output area
        output_frame = ttk.Frame(self)
        output_frame.grid(row=0, column=0, sticky="nsew", padx=6, pady=(6,3))
        output_frame.grid_rowconfigure(1, weight=1)
        output_frame.grid_columnconfigure(0, weight=1)

        # Title for output area
        output_title = ttk.Label(output_frame, text="Messages du jeu", font=('Helvetica', 12, 'bold'))
        output_title.grid(row=0, column=0, pady=(0,5), sticky="w")

        text = tk.Text(output_frame, wrap=tk.WORD, state=tk.NORMAL, bg='#1a1a1a', fg='white', 
                      font=('Consolas', 10), relief="sunken", borderwidth=2)
        text.grid(row=1, column=0, sticky="nsew")

        # Add scrollbar
        scrollbar = ttk.Scrollbar(output_frame, orient=tk.VERTICAL, command=text.yview)
        scrollbar.grid(row=1, column=1, sticky="ns")
        text.config(yscrollcommand=scrollbar.set)

        return text

    def _setup_gui(self):
        """Setup the GUI layout."""
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # L0 Output area (already created in _create_output_area)

        # L1 Image and buttons area
        image_buttons_frame = ttk.Frame(self)
        image_buttons_frame.grid(row=1, column=0, sticky="ew", padx=6, pady=3)
        image_buttons_frame.grid_columnconfigure(0, weight=1)

        # Image canvas with title
        image_frame = ttk.Frame(image_buttons_frame)
        image_frame.grid(row=0, column=0, pady=(0,10))
        
        # Title for the image area
        title_label = ttk.Label(image_frame, text="Environnement actuel", font=('Helvetica', 14, 'bold'))
        title_label.grid(row=0, column=0, pady=(0,5))
        
        self.canvas = tk.Canvas(image_frame, width=self.IMAGE_WIDTH, height=self.IMAGE_HEIGHT, bg="black", relief="sunken", borderwidth=2)
        self.canvas.grid(row=1, column=0)

        # Buttons frame with title
        buttons_frame = ttk.Frame(image_buttons_frame)
        buttons_frame.grid(row=1, column=0, sticky="ew", pady=(6,0))

        # Title for buttons area
        buttons_title = ttk.Label(buttons_frame, text="Actions disponibles", font=('Helvetica', 12, 'bold'))
        buttons_title.grid(row=0, column=0, columnspan=6, pady=(0,10), sticky="w")

        # Create buttons for common commands
        self._create_buttons(buttons_frame)

        # L2 Entry area
        entry_frame = ttk.Frame(self)
        entry_frame.grid(row=2, column=0, sticky="ew", padx=6, pady=(3,6))
        entry_frame.grid_columnconfigure(0, weight=1)

        self.entry_var = tk.StringVar()
        self.entry = ttk.Entry(entry_frame, textvariable=self.entry_var)
        self.entry.grid(row=0, column=0, sticky="ew")
        self.entry.bind("<Return>", self._on_enter)
        self.entry.focus_set()

        # Update initial room image
        self._update_room_image()

    def _create_buttons(self, parent):
        """Create buttons for common commands."""
        assets_dir = Path(__file__).parent / 'assets'

        # Row 0: Help, Quit, Inventory, Look, Take, Drop
        buttons_row0 = [
            ('help-50.png', 'help', "Help"),
            ('quit-50.png', 'quit', "Quit"),
            ('take-50.png', 'take', "Take"),
            ('drop-50.png', 'drop', "Drop"),
            (None, 'inventory', "Inventory"),
            (None, 'look', "Look")
        ]

        for i, (img_name, cmd, text) in enumerate(buttons_row0):
            try:
                if img_name:
                    img = tk.PhotoImage(file=str(assets_dir / img_name))
                    btn = ttk.Button(parent, image=img, command=lambda c=cmd: self._send_command(c))
                    btn.image = img  # Keep reference
                else:
                    btn = ttk.Button(parent, text=text, command=lambda c=cmd: self._send_command(c))
                btn.grid(row=1, column=i, padx=2)
            except (FileNotFoundError, tk.TclError):
                btn = ttk.Button(parent, text=text, command=lambda c=cmd: self._send_command(c))
                btn.grid(row=1, column=i, padx=2)

        # Row 2-3: Direction buttons
        directions = [
            ('up-arrow-50.png', 'go n', 2, 3),
            ('right-arrow-50.png', 'go e', 3, 4),
            ('down-arrow-50.png', 'go s', 4, 3),
            ('left-arrow-50.png', 'go o', 3, 2)
        ]

        for img_name, cmd, row, col in directions:
            try:
                img = tk.PhotoImage(file=str(assets_dir / img_name))
                btn = ttk.Button(parent, image=img, command=lambda c=cmd: self._send_command(c))
                btn.image = img  # Keep reference
                btn.grid(row=row, column=col, padx=2)
            except (FileNotFoundError, tk.TclError):
                direction_name = cmd.split()[-1].upper()
                btn = ttk.Button(parent, text=direction_name, command=lambda c=cmd: self._send_command(c))
                btn.grid(row=row, column=col, padx=2)

        # Row 5: Talk, Quests, Rewards, Check
        other_commands = [
            (None, 'talk', "Talk"),
            (None, 'quests', "Quests"),
            (None, 'rewards', "Rewards"),
            (None, 'check', "Check")
        ]

        for i, (img_name, cmd, text) in enumerate(other_commands):
            btn = ttk.Button(parent, text=text, command=lambda c=cmd: self._send_command(c))
            btn.grid(row=5, column=i, padx=2)

    def _update_room_image(self):
        """Update the canvas image based on the current room."""
        if not self.game.player or not self.game.player.current_room:
            return

        room = self.game.player.current_room
        assets_dir = Path(__file__).parent / 'assets'

        # Use room-specific image if available, otherwise fallback
        if room.image:
            image_path = assets_dir / room.image
        else:
            image_path = assets_dir / 'scene.png'

        try:
            # Load new image
            self._image_ref = tk.PhotoImage(file=str(image_path))
            # Clear canvas and redraw image
            self.canvas.delete("all")
            self.canvas.create_image(
                self.IMAGE_WIDTH/2,
                self.IMAGE_HEIGHT/2,
                image=self._image_ref
            )
        except (FileNotFoundError, tk.TclError):
            # Fallback to text if image not found or cannot be loaded
            self.canvas.delete("all")
            self.canvas.create_text(
                self.IMAGE_WIDTH/2,
                self.IMAGE_HEIGHT/2,
                text=f"{room.name}\n\n{room.description[:100]}...",
                fill="white",
                font=("Helvetica", 12),
                justify="center",
                width=self.IMAGE_WIDTH-20
            )

    def _on_enter(self, _event=None):
        """Handle Enter key press in the entry field."""
        value = self.entry_var.get().strip()
        if value:
            self._send_command(value)
        self.entry_var.set("")

    def _send_command(self, command):
        if self.game.finished:
            return
        # Echo the command in output area
        print(f"> {command}\n")
        self.game.process_command(command)
        # Update room image after command (in case player moved)
        self._update_room_image()
        
        # Check win/lose conditions
        if self.game.win():
            print(f"\nFélicitations {self.game.player.name}, vous avez résolu l'affaire du LYS !")
            self.game.finished = True
        elif self.game.loose():
            print(f"\n💀 GAME OVER 💀")
            print(f"\nL'homme mystérieux vous a tué, {self.game.player.name}. Vous êtes mort dans la ruelle sombre...")
            print(f"Peut-être auriez-vous dû éviter de lui parler...\n")
            self.game.finished = True
        
        if self.game.finished:
            # Disable further input and schedule close (brief delay to show farewell)
            self.entry.configure(state="disabled")
            self.after(600, self._on_close)

    def _on_close(self):
        # Restore stdout and destroy window
        sys.stdout = self.original_stdout
        self.destroy()


def main():
    # Create a game object and play the game
    args = sys.argv[1:]
    if '--cli' in args:
        Game().play()
        return
    
    # Try to use the enhanced GUI first
    try:
        from game_gui_enhanced import GameGUIEnhanced
        app = GameGUIEnhanced()
        app.mainloop()
    except (ImportError, tk.TclError) as e:
        # Fallback to standard GUI
        try:
            app = GameGUI()
            app.mainloop()
        except tk.TclError as e:
            # Fallback to CLI if GUI fails (e.g., no DISPLAY, Tkinter not available)
            print(f"GUI indisponible ({e}). Passage en mode console.")
            Game().play()
    

if __name__ == "__main__":
    main()
