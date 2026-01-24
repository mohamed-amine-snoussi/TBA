class Quest:
    """
    Représente une quête dans le jeu.

    Une quête a un nom, une description, une liste d'objectifs et des récompenses.
    """

    def __init__(self, name, description, objectives, rewards, manager):
        self.name = name
        self.description = description
        self.objectives = objectives  # list of objectives
        self.rewards = rewards  # list of rewards
        self.active = False
        self.completed_objectives = set()
        self.manager = manager

    def activate(self):
        """Active la quête."""
        self.active = True

    def complete_objective(self, objective):
        """Marque un objectif comme complété."""
        if objective in self.objectives:
            self.completed_objectives.add(objective)
        if self.is_completed():
            print(f"Quête '{self.name}' complétée !")
            for reward in self.rewards:
                self.manager.player.add_reward(reward)
            if self.name == "recuperer_disque_dur":
                print(f"Récompenses obtenues : {', '.join(self.rewards)}")
            else:
                print(f"Récompenses obtenues: {', '.join(self.rewards)}")

    def is_completed(self):
        """Vérifie si tous les objectifs sont complétés."""
        return len(self.completed_objectives) == len(self.objectives)

    def get_status(self):
        """Retourne le statut de la quête."""
        if not self.active:
            return "Non activée"
        elif self.is_completed():
            return "Complétée"
        else:
            return f"En cours ({len(self.completed_objectives)}/{len(self.objectives)} objectifs)"

    def __str__(self):
        return f"{self.name}: {self.description} - {self.get_status()}"


class QuestManager:
    """
    Gère l'ensemble des quêtes du jeu.
    """

    def __init__(self, player):
        self.quests = {}
        self.player = player

    def add_quest(self, quest):
        """Ajoute une quête."""
        self.quests[quest.name] = quest

    def get_quest(self, name):
        """Retourne une quête par nom."""
        return self.quests.get(name)

    def list_quests(self):
        """Liste toutes les quêtes."""
        return list(self.quests.values())

    def complete_objective(self, quest_name, objective):
        """Complète un objectif d'une quête."""
        quest = self.get_quest(quest_name)
        if quest and quest.active:
            quest.complete_objective(objective)

    def get_active_quests(self):
        """Retourne les quêtes actives."""
        return [q for q in self.quests.values() if q.active]

    def get_completed_quests(self):
        """Retourne les quêtes complétées."""
        return [q for q in self.quests.values() if q.is_completed()]