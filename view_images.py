#!/usr/bin/env python3
"""
Démonstration des images des salles du jeu.
Affiche toutes les images générées pour vérifier le résultat.
"""

import tkinter as tk
from PIL import Image, ImageTk
import os
from pathlib import Path

class ImageViewer(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Aperçu des images du jeu - L'Affaire du LYS")
        self.geometry("600x500")

        # Liste des images
        self.images = []
        self.current_index = 0

        # Charger les images
        self.load_images()

        # Interface
        self.setup_ui()

        if self.images:
            self.show_image(0)

    def load_images(self):
        """Charge toutes les images des salles."""
        assets_dir = Path(__file__).parent / 'assets'
        room_images = [
            'police.png', 'street.png', 'hotel.png', 'roof.png', 'bedroom.png',
            'square.png', 'metro.png', 'secret.png', 'interrogation.png',
            'archives.png', 'technical.png'
        ]

        for img_name in room_images:
            img_path = assets_dir / img_name
            if img_path.exists():
                try:
                    img = Image.open(img_path)
                    img = img.resize((400, 300), Image.Resampling.LANCZOS)
                    self.images.append((img_name, img))
                except Exception as e:
                    print(f"Erreur chargement {img_name}: {e}")

    def setup_ui(self):
        """Configure l'interface."""
        # Frame principal
        main_frame = tk.Frame(self)
        main_frame.pack(pady=10)

        # Label pour le nom de l'image
        self.name_label = tk.Label(main_frame, text="", font=('Helvetica', 14, 'bold'))
        self.name_label.pack(pady=5)

        # Canvas pour l'image
        self.canvas = tk.Canvas(main_frame, width=400, height=300, bg='black')
        self.canvas.pack()

        # Boutons de navigation
        nav_frame = tk.Frame(main_frame)
        nav_frame.pack(pady=10)

        tk.Button(nav_frame, text="◀ Précédent", command=self.prev_image).pack(side=tk.LEFT, padx=5)
        tk.Button(nav_frame, text="Suivant ▶", command=self.next_image).pack(side=tk.LEFT, padx=5)

        # Label compteur
        self.counter_label = tk.Label(main_frame, text="")
        self.counter_label.pack(pady=5)

    def show_image(self, index):
        """Affiche l'image à l'index donné."""
        if not self.images:
            return

        name, img = self.images[index]
        self.photo = ImageTk.PhotoImage(img)

        self.canvas.delete("all")
        self.canvas.create_image(200, 150, image=self.photo)

        self.name_label.config(text=name.replace('.png', '').replace('_', ' ').title())
        self.counter_label.config(text=f"{index + 1} / {len(self.images)}")

    def next_image(self):
        """Passe à l'image suivante."""
        if self.images:
            self.current_index = (self.current_index + 1) % len(self.images)
            self.show_image(self.current_index)

    def prev_image(self):
        """Passe à l'image précédente."""
        if self.images:
            self.current_index = (self.current_index - 1) % len(self.images)
            self.show_image(self.current_index)

if __name__ == "__main__":
    app = ImageViewer()
    app.mainloop()