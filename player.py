# Define the Player class.
class Player():
    """Représente le joueur dans le jeu.

    Cette classe contient le nom du joueur et la pièce dans laquelle il se trouve.

    Attributs
    ---------
    name : str
        Le nom du joueur.
    current_room : Room | None
        La pièce actuelle dans laquelle se trouve le joueur.

    Méthodes
    --------
    move(direction) -> bool
        Déplace le joueur dans la direction donnée si une sortie existe.
        Retourne True si le déplacement est possible, False sinon."""

    # Define the constructor.
    def __init__(self, name):
        self.name = name
        self.current_room = None
        self.inventory = []
    
    # Define the move method.
    def move(self, direction):
        # Get the next room from the exits dictionary of the current room.
        next_room = self.current_room.get_exit(direction)

        # If the next room is None, print an error message and return False.
        if next_room is None:
            print("\nAucune porte dans cette direction !\n")
            return False
        
        # Set the current room to the next room.
        self.current_room = next_room
        print(self.current_room.get_long_description())
        return True

    