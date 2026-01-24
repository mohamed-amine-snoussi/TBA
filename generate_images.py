#!/usr/bin/env python3
"""
Script pour générer des images placeholder pour les salles du jeu.
"""

from PIL import Image, ImageDraw, ImageFont
import os

# Dimensions des images
WIDTH = 400
HEIGHT = 300

# Couleurs
BACKGROUND_COLORS = {
    'police': '#4A90E2',      # Bleu police
    'street': '#2C3E50',      # Gris foncé pour ruelle
    'hotel': '#8B4513',       # Marron pour hôtel
    'roof': '#87CEEB',        # Bleu ciel pour toit
    'bedroom': '#DDA0DD',     # Violet pour chambre
    'square': '#32CD32',      # Vert pour place
    'metro': '#696969',       # Gris pour métro
    'secret': '#8B0000',      # Rouge foncé pour salle secrète
    'interrogation': '#FFFFE0', # Jaune pâle pour interrogatoire
    'archives': '#DEB887',    # Beige pour archives
    'technical': '#708090'    # Gris ardoise pour local technique
}

ROOM_INFO = {
    'police.png': ('Poste de Police', 'Hall du poste de police\nDossiers et cartes'),
    'street.png': ('Ruelle du centre', 'Ruelle étroite et sombre\nGraffitis du LYS'),
    'hotel.png': ('Hôtel abandonné', 'Hall décrépit\nAffaire jamais élucidée'),
    'roof.png': ('Toit de l\'immeuble', 'Toit balayé par le vent\nVue sur la ville'),
    'bedroom.png': ('Chambre 407', 'Chambre en désordre\nCrime lié au LYS'),
    'square.png': ('Place du Lys', 'Grande place\nStatue du lys stylisé'),
    'metro.png': ('Métro désaffecté', 'Quai abandonné\nPlongé dans la pénombre'),
    'secret.png': ('Salle secrète', 'Salle cachée\nDossiers brûlés et symboles'),
    'interrogation.png': ('Salle d\'interrogatoire', 'Salle froide\nNéon et table métallique'),
    'archives.png': ('Archives municipales', 'Étagères poussiéreuses\nDossiers très anciens'),
    'technical.png': ('Local technique', 'Pièce étroite\nCâbles et coffres métalliques')
}

def create_room_image(filename, title, description, bg_color):
    """Crée une image placeholder pour une salle."""
    # Créer l'image
    img = Image.new('RGB', (WIDTH, HEIGHT), bg_color)
    draw = ImageDraw.Draw(img)

    # Essayer de charger une police, sinon utiliser la police par défaut
    try:
        font_title = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 24)
        font_desc = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 16)
    except:
        font_title = ImageFont.load_default()
        font_desc = ImageFont.load_default()

    # Calculer les positions
    title_bbox = draw.textbbox((0, 0), title, font=font_title)
    title_width = title_bbox[2] - title_bbox[0]
    title_x = (WIDTH - title_width) // 2
    title_y = 50

    # Dessiner le titre
    draw.text((title_x, title_y), title, fill='white', font=font_title)

    # Dessiner la description
    desc_lines = description.split('\n')
    desc_y = title_y + 60
    for line in desc_lines:
        desc_bbox = draw.textbbox((0, 0), line, font=font_desc)
        desc_width = desc_bbox[2] - desc_bbox[0]
        desc_x = (WIDTH - desc_width) // 2
        draw.text((desc_x, desc_y), line, fill='white', font=font_desc)
        desc_y += 25

    # Ajouter un cadre
    draw.rectangle([10, 10, WIDTH-10, HEIGHT-10], outline='white', width=2)

    return img

def main():
    """Fonction principale pour générer toutes les images."""
    assets_dir = 'assets'
    os.makedirs(assets_dir, exist_ok=True)

    for filename, (title, desc) in ROOM_INFO.items():
        # Extraire le type de salle pour la couleur
        room_type = filename.split('.')[0]
        bg_color = BACKGROUND_COLORS.get(room_type, '#333333')

        # Créer l'image
        img = create_room_image(filename, title, desc, bg_color)

        # Sauvegarder
        filepath = os.path.join(assets_dir, filename)
        img.save(filepath)
        print(f"Image créée : {filepath}")

    print("Toutes les images ont été générées !")

if __name__ == "__main__":
    main()