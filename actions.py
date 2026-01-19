# Description: The actions module.

# The actions module contains the functions that are called when a command is executed.
# Each function takes 3 parameters:
# - game: the game object
# - list_of_words: the list of words in the command
# - number_of_parameters: the number of parameters expected by the command
# The functions return True if the command was executed successfully, False otherwise.
# The functions print an error message if the number of parameters is incorrect.
# The error message is different depending on the number of parameters expected by the command.


# The error message is stored in the MSG0 and MSG1 variables and formatted with the command_word variable, the first word in the command.
# The MSG0 variable is used when the command does not take any parameter.
MSG0 = "\nLa commande '{command_word}' ne prend pas de paramètre.\n"
# The MSG1 variable is used when the command takes 1 parameter.
MSG1 = "\nLa commande '{command_word}' prend 1 seul paramètre.\n"

class Actions:

    def go(game, list_of_words, number_of_parameters):
        """
        Move the player in the direction specified by the parameter.
        The parameter must be a cardinal direction (N, E, S, O).

        Args:
            game (Game): The game object.
            list_of_words (list): The list of words in the command.
            number_of_parameters (int): The number of parameters expected by the command.

        Returns:
            bool: True if the command was executed successfully, False otherwise.

        Examples:
        
        >>> from game import Game
        >>> game = Game()
        >>> game.setup()
        >>> go(game, ["go", "N"], 1)
        True
        >>> go(game, ["go", "N", "E"], 1)
        False
        >>> go(game, ["go"], 1)
        False

        """
        
        player = game.player
        l = len(list_of_words)
        # If the number of parameters is incorrect, print an error message and return False.
        if l != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG1.format(command_word=command_word))
            return False

        # Get the raw direction from the list of words.
        raw_direction = list_of_words[1]
        direction_key = raw_direction.lower()

        # Dictionnaire de synonymes -> direction canonique
        direction_aliases = {
            "n": "N",
            "nord": "N",

            "s": "S",
            "sud": "S",

            "e": "E",
            "est": "E",

            "o": "O",
            "ouest": "O",

            "u": "U",
            "up": "U",
            "haut": "U",

            "d": "D",
            "down": "D",
            "bas": "D",
        }

        # Vérifier si la direction entrée est reconnue (synonyme ou lettre)
        if direction_key not in direction_aliases:
            print(f"\nDirection '{raw_direction}' non reconnue.\n")
            # On réaffiche la salle actuelle
            print(player.current_room.get_long_description())
            return False

        # Direction canonique (N, E, S, O, U, D)
        direction = direction_aliases[direction_key]

        # Construire automatiquement l'ensemble des directions utilisées dans la map
        valid_directions = set()
        for room in game.rooms:
            valid_directions.update(room.exits.keys())

        # Si la direction canonique n'existe dans aucune salle de la map,
        # on la considère comme non reconnue.
        if direction not in valid_directions:
            print(f"\nDirection '{raw_direction}' non reconnue.\n")
            print(player.current_room.get_long_description())
            return False

        # Accès au local technique verrouillé sans la carte
        if player.current_room.name == "Métro désaffecté" and direction == "E":
            if not any(item.name == "carte" for item in player.inventory):
                print("\nLe local technique est verrouillé. Il vous faut un plan d'accès.\n")
                return False
        
        if player.current_room.name == "Métro désaffecté" and direction == "D":
            if not any(item.name == "cle_lourde" for item in player.inventory):
                print("\nLa salle est verrouillé. Il vous faut une clé d'accès.\n")
                return False
            # Vérifier que les quêtes prérequises sont complétées
            quest1 = game.quest_manager.get_quest("collecter_preuves")
            quest2 = game.quest_manager.get_quest("interroger_suspects")
            if not (quest1 and quest1.is_completed()) or not (quest2 and quest2.is_completed()):
                print("\nVous n'avez pas rassemblé assez d'informations. Vous devez d'abord collecter toutes les preuves et interroger tous les suspects.\n")
                return False

        if player.current_room.name == "Salle secrète du LYS":
            print("\nVous découvrez la vérité sur l'affaire du LYS. L'enquête est terminée.\n")


        # Move the player in the direction specified by the parameter.
        if player.move(direction):
            # AJOUTER LA NOUVELLE SALLE DANS L'HISTORIQUE
            game.history.append(player.current_room)
            # Check quest objectives
            if player.current_room.name == "Salle secrète du LYS":
                game.quest_manager.complete_objective("resoudre_enigme", "salle_secrete")
            return True
        return False

    def quit(game, list_of_words, number_of_parameters):
        """
        Quit the game.

        Args:
            game (Game): The game object.
            list_of_words (list): The list of words in the command.
            number_of_parameters (int): The number of parameters expected by the command.

        Returns:
            bool: True if the command was executed successfully, False otherwise.

        Examples:

        >>> from game import Game
        >>> game = Game()
        >>> game.setup()
        >>> quit(game, ["quit"], 0)
        True
        >>> quit(game, ["quit", "N"], 0)
        False
        >>> quit(game, ["quit", "N", "E"], 0)
        False

        """
        l = len(list_of_words)
        # If the number of parameters is incorrect, print an error message and return False.
        if l != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG0.format(command_word=command_word))
            return False
        
        # Set the finished attribute of the game object to True.
        player = game.player
        msg = f"\nMerci {player.name} d'avoir joué. Au revoir.\n"
        print(msg)
        game.finished = True
        return True

    def help(game, list_of_words, number_of_parameters):
        """
        Print the list of available commands.
        
        Args:
            game (Game): The game object.
            list_of_words (list): The list of words in the command.
            number_of_parameters (int): The number of parameters expected by the command.

        Returns:
            bool: True if the command was executed successfully, False otherwise.

        Examples:

        >>> from game import Game
        >>> game = Game()
        >>> game.setup()
        >>> help(game, ["help"], 0)
        True
        >>> help(game, ["help", "N"], 0)
        False
        >>> help(game, ["help", "N", "E"], 0)
        False

        """

        # If the number of parameters is incorrect, print an error message and return False.
        l = len(list_of_words)
        if l != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG0.format(command_word=command_word))
            return False
        
        # Print the list of available commands.
        print("\nVoici les commandes disponibles:")
        for command in game.commands.values():
            print("\t- " + str(command))
        print()
        return True
    
    def history(game, list_of_words, number_of_parameters):
        """
        Print the list of previously visited rooms.
        Vérification du nombre de paramètres
        """

        if len(list_of_words) != 1:
            command_word = list_of_words[0]
            print(MSG0.format(command_word=command_word))
            return False
        
        print("\nHistorique des salles visitées :")
        for room in game.history:
            print(f"\t- {room.name}")
        print()

        return True

    def back(game, list_of_words, number_of_parameters):
        """
        Return to the previous room if possible.
        """
        # Vérification du nombre de paramètres
        if len(list_of_words) != 1:
            command_word = list_of_words[0]
            print(MSG0.format(command_word=command_word))
            return False
        
        # On ne peut pas revenir en arrière si on n’a qu’une seule salle
        if len(game.history) < 2:
            print("\nImpossible de revenir en arrière.\n")
            return False
        
        # Supprimer la salle actuelle
        game.history.pop()

        # Nouvelle salle = dernière salle de la liste
        previous_room = game.history[-1]
        game.player.current_room = previous_room

        # Afficher la nouvelle salle
        print(previous_room.get_long_description())
        Actions.history(game, ["history"], 0)
        return True

    def take(game, list_of_words, number_of_parameters):
        if len(list_of_words) != 2:
            print(MSG1.format(command_word="take"))
            return False

        item_name = list_of_words[1]
        room = game.player.current_room

        for item in room.items:
            if item.name == item_name:
                game.player.inventory.append(item)
                room.items.remove(item)
                print(f"\nVous avez ramassé : {item.name}\n")
                # Check quest objectives
                game.quest_manager.complete_objective("collecter_preuves", item_name)
                return True

        print(f"\nL'objet '{item_name}' n'est pas dans la pièce.\n")
        return False


    def drop(game, list_of_words, number_of_parameters):
        if len(list_of_words) != 2:
            print(MSG1.format(command_word="drop"))
            return False

        item_name = list_of_words[1]
        inventory = game.player.inventory

        for item in inventory:
            if item.name == item_name:
                inventory.remove(item)
                game.player.current_room.items.append(item)
                print(f"\nVous avez déposé : {item.name}\n")
                return True

        print(f"\nL'objet '{item_name}' n'est pas dans l'inventaire.\n")
        return False


    def inventory(game, list_of_words, number_of_parameters):
        if len(list_of_words) != 1:
            print(MSG0.format(command_word="inventory"))
            return False

        if not game.player.inventory:
            print("\nVotre inventaire est vide.\n")
            return True

        print("\nVotre inventaire contient :")
        for item in game.player.inventory:
            print(f" - {item.name}")
        print()
        return True

    def look(game, list_of_words, number_of_parameters):
        if len(list_of_words) != 1:
            command_word = list_of_words[0]
            print(MSG0.format(command_word=command_word))
            return False

        room = game.player.current_room

        if not room.items and not room.characters:
            print("\nIl n'y a rien ici.\n")
            return True

        print("\nOn voit:")

        # Affichage des objets
        if room.items:
            print("\nObjets présents :")
            for item in room.items:
                print(f"\t- {item}")

        # Affichage des personnages
        if room.characters:
            print("\nPersonnes présentes :")
            for character in room.characters:
                print(f"\t- {character.name} : {character.description}")

        print()
        return True

    
    def check(game, list_of_words, number_of_parameters):
        if len(list_of_words) != 1:
            print(MSG0.format(command_word="check"))
            return False

        inventory = game.player.inventory

        if not inventory:
            print("\nVotre inventaire est vide.\n")
            return True

        print("\nVous disposez des items suivants:")
        for item in inventory:
            print(f"\t- {item}")
        print()
        return True
    
    def talk(game, list_of_words, number_of_parameters):
        if len(list_of_words) != 2:
            command_word = list_of_words[0]
            print(MSG1.format(command_word=command_word))
            return False

        character_name = list_of_words[1]
        room = game.player.current_room

        for character in room.characters:
            if character.name.lower() == character_name.lower():
                print("\n" + character.talk() + "\n")
                # Check quest objectives
                if character.name == "Témoin":
                    game.quest_manager.complete_objective("interroger_suspects", "temoin")
                elif character.name == "Archiviste":
                    game.quest_manager.complete_objective("interroger_suspects", "archiviste")
                elif character.name == "Technicien":
                    game.quest_manager.complete_objective("interroger_suspects", "technicien")
                return True

        print(f"\nIl n'y a personne nommé '{character_name}' ici.\n")
        return False

    def quests(game, list_of_words, number_of_parameters):
        """
        List all quests.
        """
        if len(list_of_words) != 1:
            command_word = list_of_words[0]
            print(MSG0.format(command_word=command_word))
            return False

        quests = game.quest_manager.list_quests()
        if not quests:
            print("\nAucune quête disponible.\n")
            return True

        print("\nQuêtes disponibles:")
        for quest in quests:
            print(f"- {quest}")
        print()
        return True

    def quest(game, list_of_words, number_of_parameters):
        """
        Show details of a specific quest.
        """
        if len(list_of_words) != 2:
            command_word = list_of_words[0]
            print(MSG1.format(command_word=command_word))
            return False

        quest_name = list_of_words[1]
        quest = game.quest_manager.get_quest(quest_name)
        if not quest:
            print(f"\nQuête '{quest_name}' introuvable.\n")
            return False

        print(f"\n{quest.name}: {quest.description}")
        print(f"Statut: {quest.get_status()}")
        print(f"Objectifs: {', '.join(quest.objectives)}")
        print(f"Récompenses: {', '.join(quest.rewards)}\n")
        return True

    def activate(game, list_of_words, number_of_parameters):
        """
        Activate a quest.
        """
        if len(list_of_words) != 2:
            command_word = list_of_words[0]
            print(MSG1.format(command_word=command_word))
            return False

        quest_name = list_of_words[1]
        quest = game.quest_manager.get_quest(quest_name)
        if not quest:
            print(f"\nQuête '{quest_name}' introuvable.\n")
            return False

        if quest.active:
            print(f"\nQuête '{quest_name}' déjà activée.\n")
            return False

        quest.activate()
        print(f"\nQuête '{quest_name}' activée.\n")
        return True

    def rewards(game, list_of_words, number_of_parameters):
        """
        Show player's rewards.
        """
        if len(list_of_words) != 1:
            command_word = list_of_words[0]
            print(MSG0.format(command_word=command_word))
            return False

        game.player.show_rewards()
        return True

