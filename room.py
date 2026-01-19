# Define the Room class.

class Room:
    """Représente un lieu dans le jeu d'aventure.

    Cette classe modélise une pièce ou un lieu contenant un nom, une description
    et des sorties menant vers d'autres lieux.

    Attributs
    ---------
    name : str
        Le nom du lieu.
    description : str
        La description du lieu.
    exits : dict
        Un dictionnaire associant une direction (str) à un autre objet Room.

    Méthodes
    --------
    get_exit(direction) -> Room | None
        Retourne la pièce située dans la direction donnée ou None si elle n'existe pas.
    get_exit_string() -> str
        Retourne une chaîne décrivant les sorties disponibles.
    get_long_description() -> str
        Retourne une description complète du lieu incluant les sorties."""

    # Define the constructor. 
    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.exits = {}
        self.items = []
        self.characters = []
    
    # Define the get_exit method.
    def get_exit(self, direction):

        # Return the room in the given direction if it exists.
        if direction in self.exits.keys():
            return self.exits[direction]
        else:
            return None
    
    # Return a string describing the room's exits.
    def get_exit_string(self):
        exit_string = "Sorties: " 
        for exit in self.exits.keys():
            if self.exits.get(exit) is not None:
                exit_string += exit + ", "
        exit_string = exit_string.strip(", ")
        return exit_string

    # Return a long description of this room including exits.
    def get_long_description(self):
        desc = f"\nVous êtes dans {self.description}\n"
        # Ne pas lister automatiquement les personnages ici :
        # ils seront affichés uniquement via la commande `look`.
        desc += f"\n{self.get_exit_string()}\n"
        return desc
