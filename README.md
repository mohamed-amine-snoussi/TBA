## Projet TBA : l'Affaire du LYS (par Amine Snoussi et David Benadon)
# Guide Utilisateur
## Introduction
Contexte du jeu :
L'Affaire du LYS est un jeu d'aventure textuel jouable dans le terminal ou avec une interface graphique, dans lequel le joueur incarne un détective chargé de résoudre une affaire liée à une organisation secrète nommée "LYS". Le but est d'explorer différentes salles, récupérer des indices et preuves, interroger des témoins, accomplir des quêtes, et infiltrer le repaire secret de l'organisation pour mettre fin à leurs activités.
Tout au long de la partie, le joueur doit faire des choix importants : où se déplacer, quels objets ramasser, quels personnages interroger ou éviter, et comment progresser dans l'enquête. Attention : certaines rencontres peuvent être fatales, notamment avec un mystérieux individu en manteau noir qui rôde dans les ruelles sombres de la ville.

But du jeu :
L'objectif principal est de résoudre l'Affaire du LYS et de démanteler l'organisation secrète en accomplissant les quêtes nécessaires, en rassemblant tous les indices au bon moment, en interrogeant les bons témoins, et en évitant les pièges mortels, jusqu'à atteindre la condition de victoire finale : récupérer le disque dur chiffré dans la salle secrète du LYS.

## Commandes du jeu

Pour lancer le jeu, il faut exécuter la commande suivante dans le terminal :

```bash
python game.py
```

Le jeu peut se jouer avec une interface graphique (mode par défaut sur VsCode) ou dans le terminal en mode texte (si lancé depuis GitHub).


Les commandes sont saisies directement dans le terminal ou dans la zone de texte de l'interface graphique pendant la partie.

- **help**
  
  Affiche l'aide du jeu, avec toutes les commandes disponibles et comment les utiliser.

- **quit**
  
  Quitte le jeu immédiatement et termine la partie.

- **go <direction>**
  
  Permet de se déplacer dans une direction depuis la salle actuelle.
  
  **Directions possibles :**
  - `N` pour Nord
  - `E` pour Est
  - `S` pour Sud
  - `O` pour Ouest
  - `U` pour Haut (Up)
  - `D` pour Bas (Down)

- **history**
  
  Affiche l'historique des salles que le joueur a visitées depuis le début de la partie.

- **back**
  
  Permet de revenir dans la salle précédente (retour arrière), en utilisant l'historique du joueur.

- **take <objet>**
  
  Permet de ramasser un objet présent dans la salle et de l'ajouter à l'inventaire du joueur.

- **drop <objet>**
  
  Permet de déposer un objet de l'inventaire du joueur dans la salle actuelle.

- **inventory**
  
  Affiche l'inventaire du joueur (tous les objets qu'il possède actuellement).

- **look**
  
  Permet d'observer la salle actuelle et voir les objets et personnages présents dedans.

- **check**
  
  Affiche aussi l'inventaire du joueur (commande équivalente à inventory).

- **talk <personne>**
  
  Permet de parler à un personnage présent dans la salle (PNJ), et d'obtenir un dialogue, des indices ou une interaction.
  ⚠️ **Attention :** Ne parlez pas à l'Homme_Mysterieux dans la ruelle, cela vous sera fatal !

- **quests**
  
  Affiche toutes les quêtes du jeu (liste globale des quêtes disponibles).

- **quest <nom>**
  
  Affiche les détails d'une quête spécifique, en fonction de son nom (objectif, infos, progression).

- **activate <nom>**
  
  Active une quête spécifique (pas besoin de le faire, les quêtes sont activées automatiquement au debut).
  Vous pouvez aussi utiliser `activate quests` pour activer toutes les quêtes disponibles.

- **rewards**
  
  Affiche les récompenses obtenues ou disponibles dans le jeu (liées aux quêtes / progression).

## Règles du jeu

**Conditions de victoire**

Le jeu se gagne lorsque le joueur accomplit toutes les quêtes principales et récupère le disque dur chiffré dans la salle secrète du LYS, en survivant aux dangers et en utilisant correctement les indices et objets nécessaires pour progresser dans l'enquête.

**Conditions de défaite**

Le joueur perd s'il parle à l'Homme Mystérieux dans la ruelle sombre, ce qui entraîne une mort immédiate et une fin du jeu. Il faut donc éviter toute interaction avec ce personnage dangereux.

**Objets**

Certains objets sont indispensables pour réussir certaines quêtes ou accéder à certaines zones verrouillées. Ils doivent être trouvés dans les salles puis ajoutés à l'inventaire afin d'être utilisés au bon moment. Par exemple, la carte est nécessaire pour accéder au local technique, et la clé lourde est indispensable pour entrer dans la salle secrète du LYS.


# Contenu du jeu
## Salles (Room)

Le jeu repose sur une carte composée de **11 salles**, chacune ayant :
- **un nom** (ex : "Poste de Police", "Ruelle du centre", "Salle secrète du LYS")
- **une description** détaillée de l'environnement
- **des sorties** vers d'autres salles (N, S, E, O, U, D)
- **des objets disponibles** à ramasser (badge, dossier, photo, carte, etc.)
- **des personnages présents** (Témoin, Archiviste, Technicien, Homme Mystérieux)

Chaque salle est gérée grâce à la classe `Room` qui permet :
- d'obtenir une sortie (`get_exit`) : retourne la salle adjacente dans une direction donnée
- d'obtenir la liste des objets présents dans la salle
- d'afficher une description complète (`get_long_description`) : affiche le nom, la description et les sorties disponibles
- de gérer les personnages présents dans la salle

## Personnages (PNJ)

Les personnages sont gérés avec les classes `Character` et `StaticCharacter` qui permettent :
- de savoir où ils se trouvent (dans quelle salle)
- de stocker leurs messages et dialogues possibles
- de gérer leur déplacement potentiel (certains bougent aléatoirement, d'autres restent statiques)
- d'interagir avec le joueur

**PNJ présents dans le jeu :**

• **Témoin** : Un homme nerveux présent dans la salle d'interrogatoire. Sert à donner des indices sur les activités du LYS et peut déclencher une quête. Révèle des informations sur les réunions secrètes à l'hôtel et la Place du Lys.

• **Archiviste** : Une employée fatiguée mais curieuse présente aux archives municipales. Sert à guider le joueur vers le métro désaffecté et révèle l'historique du LYS à travers les décennies.

• **Technicien** : Un ancien agent du métro au regard méfiant présent dans le local technique. Sert à donner des informations sur les accès verrouillés et l'importance de la carte et de la clé lourde.

• **Homme Mystérieux** : Un individu dangereux en manteau noir présent dans la ruelle sombre. ⚠️ **Représente un piège mortel** - Parler à ce personnage entraîne une mort immédiate et la fin du jeu. C'est le seul personnage qu'il faut absolument éviter.

Ces personnages apparaissent dans certaines salles, et le joueur peut interagir avec eux via la commande `talk <nom>`.

## Items (objets) et utilité

Les objets sont définis avec la classe `Item`, contenant :
- **un nom** (identifiant unique de l'objet)
- **une description** (informations sur l'objet et son utilité)
- **un poids** (weight) en kilogrammes

**Objets présents dans le jeu :**

- **Badge** : Badge d'accès réservé au personnel du poste. Permet de prouver son identité et est un indice important pour la quête principale.

- **Dossier** : Dossier secret portant le sceau du LYS. Permet d'obtenir des informations cruciales sur l'organisation et fait partie des preuves à collecter.

- **Photo** : Photographie montrant une réunion secrète du LYS. Permet d'identifier les membres de l'organisation et sert de preuve visuelle.

- **Carte** : Carte indiquant un passage scellé sous la place. **Indispensable** pour accéder au local technique du métro (zone verrouillée).

- **Dictaphone** : Dictaphone contenant un message chiffré. Permet d'obtenir des indices audio sur les activités du LYS.

- **Clé lourde** : Clé massive permettant d'ouvrir une grille sécurisée. **Indispensable** pour accéder à la salle secrète du LYS.

- **Témoignage** : Compte rendu d'un témoin évoquant des réunions secrètes du LYS. Permet d'obtenir des informations écrites et des indices supplémentaires.

- **Dossier d'archives** : Dossiers anciens reliant le LYS à des affaires passées. Permet de comprendre l'historique de l'organisation sur plusieurs décennies.

- **Disque dur** : Disque dur chiffré contenant des preuves compromettantes. **Objectif final du jeu** - Récupérer cet objet dans la salle secrète permet de gagner la partie.

Chaque objet peut être récupéré avec `take <objet>` puis vérifié avec `check` ou `inventory`.

## Quêtes

Le système de quêtes est représenté par les classes `Quest` et `QuestManager`.
Le jeu contient **4 quêtes** interconnectées, qui permettent de structurer la progression de l'enquête.

**Quêtes principales :**

- **Collecter les preuves** : C'est la première quête centrale du jeu, elle demande de rassembler les 8 indices sur l'affaire du LYS (badge, dossier, photo, carte, dictaphone, clé lourde, témoignage, dossier d'archives). Récompense : "Indices rassemblés".

- **Interroger les suspects** : Quête parallèle qui consiste à parler aux 3 personnages clés (Témoin, Archiviste, Technicien) pour obtenir des informations cruciales. Récompense : "Informations cruciales".

- **Accéder à la salle secrète** : Quête qui se débloque après avoir complété les deux premières. Le joueur doit infiltrer le repaire secret du LYS en utilisant la clé lourde. Récompense : "Accès aux zones secrètes".

- **Récupérer le disque dur** : **Quête finale** du jeu. Le joueur doit récupérer le disque dur chiffré dans la salle secrète pour démanteler définitivement l'organisation. Récompense : "Victoire sur l'affaire du LYS".

**Système de progression :**

Les quêtes ont des prérequis : certaines ne peuvent être accomplies qu'après avoir complété d'autres quêtes. Par exemple, il faut avoir collecté toutes les preuves et interrogé tous les suspects avant de pouvoir accéder à la salle secrète du LYS.

Le joueur peut consulter ses quêtes avec `quests` et obtenir les détails d'une quête spécifique avec `quest <nom>`.

# Guide développeur 
## Architecture du projet

Le projet est séparé en plusieurs fichiers Python, chacun gérant une partie précise du jeu :

**game.py :**

Fichier principal qui lance le jeu, initialise les 11 salles, les 9 objets, les 4 personnages, les commandes disponibles, le système de quêtes, puis démarre la boucle de jeu. Contient également les classes pour l'interface graphique (`GameGUI`) et gère les conditions de victoire et de défaite.

**player.py :**

Contient la classe `Player`, qui gère la salle actuelle du joueur, son inventaire, ses récompenses, l'historique des déplacements et les fonctions de déplacement.

**room.py :**

Contient la classe `Room` pour représenter les salles du jeu. Gère le nom, la description, les sorties vers d'autres salles, les objets présents et les personnages dans chaque salle. Permet d'afficher une description complète avec les sorties disponibles.

**item.py :**

Contient la classe `Item` qui représente les objets manipulables (preuves, indices, clés). Chaque objet a un nom, une description et un poids.

**character.py :**

Contient les classes `Character` et `StaticCharacter` pour les PNJ du jeu. Gère leurs dialogues, leur position, leurs déplacements aléatoires (ou leur immobilité pour les personnages statiques comme l'Homme Mystérieux).

**quest.py :**

Contient les classes `Quest` et `QuestManager` pour structurer les objectifs du joueur. Gère les prérequis entre quêtes, la progression, les récompenses et l'activation automatique des quêtes disponibles.

**command.py :**

Contient la classe `Command`, utilisée pour organiser les commandes disponibles (help, go, take, talk, etc.), leurs descriptions et le nombre de paramètres attendus.

**actions.py :**

Contient l'ensemble des fonctions de commandes (go, take, drop, look, talk, back, history, quests, etc.). C'est le cœur du gameplay interactif car ce fichier relie les actions du joueur au monde du jeu. Gère également les restrictions d'accès aux salles verrouillées et la détection de la mort du joueur.

**game_gui_enhanced.py :**

Contient l'interface graphique améliorée du jeu avec Tkinter, permettant de jouer avec des boutons et une zone de texte au lieu du terminal.

## Diagramme de Classe (voir photo diagramme dans fichier Map + Diagrammes)
Game "1" --> "1" Player : has
    Game "1" --> "*" Room : manages
    Game "1" --> "*" Command : uses
    Game "1" --> "1" QuestManager : has
    GameGUI "1" --> "1" Game : uses
    Player "1" --> "1" Room : current_room
    Player "1" --> "*" Item : inventory
    Room "1" --> "*" Item : contains
    Room "1" --> "*" Character : contains
    Room "*" --> "*" Room : exits
    StaticCharacter --|> Character : inherits
    QuestManager "1" --> "*" Quest : manages
    Quest "*" --> "1" QuestManager : references
    Command "1" --> "1" Actions : executes
    
**Explications du diagramme :**

- **Game** : Classe principale qui orchestre tout le jeu (gestion des salles, commandes, joueur, quêtes)
- **GameGUI** : Interface graphique Tkinter qui utilise Game pour afficher le jeu visuellement avec boutons et canvas
- **Player** : Représente le joueur avec son inventaire et sa position actuelle
- **Room** : Représente les 11 salles du jeu avec leurs sorties, objets et personnages
- **Item** : Représente les 9 objets/indices collectables (badge, dossier, photo, etc.)
- **Character** : PNJ avec dialogues et déplacements aléatoires (Témoin, Archiviste, Technicien)
- **StaticCharacter** : Hérite de Character mais ne bouge jamais (Homme Mystérieux)
- **Command** : Représente une commande disponible avec son action associée
- **Actions** : Classe statique contenant toutes les fonctions de commandes (go, take, talk, etc.)
- **Quest** : Représente une quête avec objectifs, récompenses et prérequis
- **QuestManager** : Gère toutes les quêtes et leur progression

Les flèches montrent les relations entre les classes : composition (`-->`), héritage (`--|>`), et les cardinalités (`"1"`, `"*"`).



## Fonctionnement général du jeu

Le fonctionnement général du jeu repose sur une structure simple mais efficace. Au démarrage, le programme initialise tout l'univers de L'Affaire du LYS : il crée les 11 salles différentes (du Poste de Police à la Salle secrète du LYS), relie ces salles entre elles grâce aux directions possibles (N, S, E, O, U, D), place les 9 objets (indices et preuves) dans certaines pièces et positionne les 4 personnages à des endroits précis. Le système de quêtes est également initialisé avec ses prérequis. Ensuite, le joueur est créé et placé au Poste de Police (salle de départ), ce qui permet de commencer l'enquête directement.

Une fois cette phase d'initialisation terminée, le jeu entre dans une boucle principale. À chaque tour, le joueur saisit une commande dans le terminal ou l'interface graphique, comme se déplacer (`go`), regarder autour de lui (`look`), ramasser un objet (`take`), parler à un personnage (`talk`) ou consulter ses quêtes (`quests`). Le programme analyse alors ce que le joueur a écrit, vérifie si la commande existe et lance l'action correspondante via le module `actions.py`. Cette action modifie ensuite l'état du jeu, par exemple en changeant la salle actuelle, en ajoutant un objet dans l'inventaire, en complétant un objectif de quête ou en déclenchant un événement (comme la mort si le joueur parle à l'Homme Mystérieux). Les personnages non-statiques peuvent également se déplacer aléatoirement entre les tours.

Tout au long de la partie, le jeu met à jour en permanence la progression du joueur, notamment grâce au système de quêtes interconnectées (`QuestManager`), aux interactions avec les objets (collecte d'indices) et aux dialogues avec les personnages (témoignages). Le jeu se termine lorsque le joueur atteint une condition de fin : une victoire après avoir récupéré le disque dur chiffré dans la salle secrète du LYS, ou une défaite immédiate si le joueur parle à l'Homme Mystérieux dans la ruelle sombre.

# Perspectives de Développement 
## Améliorations possibles 

Le jeu est déjà fonctionnel et complet, mais plusieurs améliorations pourraient enrichir l'expérience de jeu et offrir plus de profondeur à l'enquête :

**Système de combat / Affrontements :**
Ajouter un système de combat permettrait au joueur de se défendre contre l'Homme Mystérieux ou d'autres menaces potentielles, au lieu d'une mort immédiate. Cela pourrait inclure des statistiques de santé, des armes à trouver et des choix tactiques.

**Indices visuels et images :**
Enrichir l'interface graphique avec des images spécifiques pour chaque objet collecté, des portraits des personnages et des illustrations pour les scènes clés de l'enquête. Cela rendrait l'immersion plus forte.

**Système de temps et d'urgence :**
Implémenter un compte à rebours ou une limite de tours forcerait le joueur à être plus stratégique dans ses choix. Par exemple, le LYS pourrait s'échapper si le joueur prend trop de temps à collecter les preuves.

**Fins multiples :**
Créer plusieurs fins possibles en fonction des choix du joueur (par exemple : arrêter le LYS seul, demander des renforts, infiltrer secrètement, négocier, etc.). Cela augmenterait la rejouabilité.

**Système de sauvegarde :**
Permettre au joueur de sauvegarder sa progression à tout moment et de charger une partie précédente. Cela éviterait de devoir recommencer depuis le début en cas d'erreur fatale.

**Sons et musique d'ambiance :**
Intégrer des effets sonores (bruits de pas, portes, dialogues) et une bande sonore d'ambiance pour renforcer l'atmosphère policière et mystérieuse du jeu.

**Extension de la carte :**
Ajouter de nouvelles zones à explorer (commissariat central, quartiers de la ville, planques secrètes du LYS) pour agrandir l'univers du jeu et prolonger l'enquête.

**Mode multijoueur coopératif :**
Permettre à deux joueurs de coopérer dans l'enquête, chacun avec son propre inventaire et ses propres objectifs à remplir pour résoudre l'affaire ensemble.


