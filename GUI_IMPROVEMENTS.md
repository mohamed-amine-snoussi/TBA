# Amélioration de l'Interface Graphique

## Images des salles

Le jeu utilise maintenant des images spécifiques pour chaque salle. Les images sont générées automatiquement avec des couleurs et descriptions personnalisées.

### Personnalisation des images

Pour créer de belles images personnalisées, vous pouvez :

1. **Remplacer les images générées** dans le dossier `assets/` par vos propres images PNG de 400x300 pixels
2. **Modifier le script** `generate_images.py` pour changer les couleurs et descriptions
3. **Utiliser des outils graphiques** comme GIMP, Photoshop, ou des générateurs d'images IA

### Noms des fichiers d'images

- `police.png` - Poste de Police
- `street.png` - Ruelle du centre
- `hotel.png` - Hôtel abandonné
- `roof.png` - Toit de l'immeuble
- `bedroom.png` - Chambre 407
- `square.png` - Place du Lys
- `metro.png` - Métro désaffecté
- `secret.png` - Salle secrète du LYS
- `interrogation.png` - Salle d'interrogatoire
- `archives.png` - Archives municipales
- `technical.png` - Local technique du métro

## Icônes des boutons

Les boutons utilisent des icônes PNG de 50x50 pixels. Vous pouvez les remplacer par :

- `help-50.png` - Icône d'aide
- `quit-50.png` - Icône de quitter
- `take-50.png` - Icône de ramasser
- `drop-50.png` - Icône de déposer
- `up-arrow-50.png` - Flèche haut
- `right-arrow-50.png` - Flèche droite
- `down-arrow-50.png` - Flèche bas
- `left-arrow-50.png` - Flèche gauche

## Améliorations possibles

### 1. Images plus réalistes
- Utiliser des photos ou illustrations représentant chaque lieu
- Créer des atmosphères différentes (sombre pour le métro, lumineux pour la place, etc.)

### 2. Interface plus moderne
- Changer les couleurs du thème
- Ajouter des animations
- Utiliser des polices plus stylées

### 3. Plus de boutons
- Ajouter des raccourcis pour les commandes fréquentes
- Boutons pour l'historique, back, etc.

### 4. Sons et effets
- Ajouter des effets sonores
- Musique d'ambiance par salle

## Comment modifier

1. **Images** : Remplacez les fichiers dans `assets/`
2. **Couleurs** : Modifiez le script `generate_images.py`
3. **Interface** : Éditez la classe `GameGUI` dans `game.py`
4. **Style** : Ajustez les propriétés ttk.Style()

N'hésitez pas à expérimenter et personnaliser l'interface selon vos goûts ! 🎨