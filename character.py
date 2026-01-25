import random

class Character:
    """
    Représente un personnage non joueur (PNJ).
    """

    def __init__(self, name, description, room, dialogues, is_static=False):
        self.name = name
        self.description = description
        self.dialogues = dialogues
        self.current_dialogue = 0
        self.room = room
        self.is_static = is_static

        # On place automatiquement le personnage dans la salle
        room.characters.append(self)

    def talk(self):
        # Utiliser get_msg() pour récupérer le message suivant
        return self.get_msg()

    def get_msg(self):
        """
        Retourne le message suivant du PNJ.

        Comportement: on prend le premier message de la liste `dialogues`, on
        le supprime et on le remet en fin de liste pour obtenir un affichage
        cyclique des répliques lors des appels successifs.
        """
        if not self.dialogues:
            return ""

        msg = self.dialogues.pop(0)
        # remettre le message à la fin pour garder un cycle
        self.dialogues.append(msg)
        return msg

    def move(self, debug=False):
        """
        Déplace le PNJ avec une probabilité de 1/2.
        Va dans une pièce adjacente au hasard.
        Retourne True si déplacement, False sinon.
        """
        if self.is_static:
            if debug:
                print(f"DEBUG: {self.name} est statique et reste dans {self.room.name}")
            return False

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


class StaticCharacter(Character):
    """
    Personnage qui ne se déplace jamais.
    """
    def move(self, debug=False):
        """Ce personnage ne bouge jamais."""
        if debug:
            print(f"DEBUG: {self.name} est statique et ne se déplace pas")
        return False
