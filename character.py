import random

class Character:
    """
    Représente un personnage non joueur (PNJ).
    """

    def __init__(self, name, description, room, dialogues):
        self.name = name
        self.description = description
        self.dialogues = dialogues
        self.current_dialogue = 0
        self.room = room

        # On place automatiquement le personnage dans la salle
        room.characters.append(self)

    def talk(self):
        message = self.dialogues[self.current_dialogue]
        self.current_dialogue = (self.current_dialogue + 1) % len(self.dialogues)
        return message

    def move(self, debug=False):
        """
        Déplace le PNJ avec une probabilité de 1/2.
        Va dans une pièce adjacente au hasard.
        Retourne True si déplacement, False sinon.
        """

        # 1 chance sur 2 de rester
        if random.choice([True, False]) is False:
            if debug:
                print(f"DEBUG: {self.name} reste dans {self.room.name}")
            return False

        # sorties possibles (non None)
        possible_rooms = [r for r in self.room.exits.values() if r is not None]
        if not possible_rooms:
            return False

        new_room = random.choice(possible_rooms)

        # bouger
        if self in self.room.characters:
            self.room.characters.remove(self)
        new_room.characters.append(self)
        self.room = new_room

        if debug:
            print(f"DEBUG: {self.name} se déplace vers {new_room.name}")

        return True
