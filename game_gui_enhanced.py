# Enhanced GUI for the game with visual map and improved interface
import tkinter as tk
from tkinter import ttk, simpledialog, messagebox
import sys
from pathlib import Path
from PIL import Image, ImageTk, ImageDraw
import threading

from game import Game
from room import Room

class GameGUIEnhanced(tk.Tk):
    """Enhanced GUI with visual map and interactive commands."""
    
    IMAGE_WIDTH = 400
    IMAGE_HEIGHT = 300
    
    def __init__(self):
        super().__init__()
        self.title("L'Affaire du LYS - Jeu d'Aventure")
        self.geometry("1400x800")
        self.resizable(True, True)
        
        # Initialize game to None (will be set later)
        self.game = None
        self.original_stdout = sys.stdout
        
        # Set background image
        self._set_background_image()
        
        # Setup GUI immediately (will be empty until game starts)
        self._setup_styles()
        self._setup_gui()
        
        # Show start screen in a separate window
        self._show_start_screen()
        
    def _show_start_screen(self):
        """Display the start screen with the beautiful PLAY button image."""
        # Create splash window
        splash = tk.Toplevel(self)
        splash.attributes('-topmost', True)
        splash.geometry("1400x800+0+0")
        splash.title("L'Affaire du Lys")
        
        # Set background image for splash
        assets_dir = Path(__file__).parent / 'assets'
        possible_names = ['splash_screen.png', 'splash_screen .png', 'splash_screen.PNG']
        splash_path = None
        
        for name in possible_names:
            path = assets_dir / name
            if path.exists():
                splash_path = path
                break
        
        try:
            if splash_path and splash_path.exists():
                img = Image.open(splash_path)
                img = img.resize((1400, 800), Image.Resampling.LANCZOS)
                splash_photo = ImageTk.PhotoImage(img)
                bg_label = tk.Label(splash, image=splash_photo)
                bg_label.image = splash_photo
                bg_label.pack(fill=tk.BOTH, expand=True)
        except:
            splash.configure(bg='#1a1a1a')
        
        # Try to load the play button image
        play_button_path = assets_dir / 'play_button.png'
        
        if play_button_path.exists():
            try:
                # Load play button image
                button_img = Image.open(play_button_path)
                button_img = button_img.resize((220, 155), Image.Resampling.LANCZOS)
                button_photo = ImageTk.PhotoImage(button_img)
                
                # Create button with image - no background
                play_button = tk.Label(
                    splash,
                    image=button_photo,
                    cursor='hand2'
                )
                play_button.image = button_photo
                play_button.bind('<Button-1>', lambda e: self._start_game(splash))
                play_button.place(relx=0.5, rely=0.5, anchor='center')
                
            except Exception as e:
                print(f"Erreur chargement image bouton: {e}")
                self._create_text_play_button(splash)
        else:
            # Fallback to text button if image not found
            self._create_text_play_button(splash)
    
    def _create_text_play_button(self, splash):
        """Create a text-based PLAY button as fallback."""
        center_container = tk.Frame(splash, bg='#000000')
        center_container.place(relx=0.5, rely=0.5, anchor='center')
        
        play_button = tk.Button(
            center_container,
            text="▶ PLAY",
            font=('Arial', 48, 'bold'),
            fg='#FFFFFF',
            bg='#DAA520',
            activeforeground='#FFFFFF',
            activebackground='#FFD700',
            padx=80,
            pady=30,
            relief=tk.RAISED,
            bd=6,
            cursor='hand2',
            command=lambda: self._start_game(splash)
        )
        play_button.pack()
        
        def on_enter(event):
            play_button.config(bg='#FFD700')
        
        def on_leave(event):
            play_button.config(bg='#DAA520')
        
        play_button.bind('<Enter>', on_enter)
        play_button.bind('<Leave>', on_leave)
    
    def _start_game(self, splash_window):
        """Start the game after asking for player name."""
        # First destroy splash window
        splash_window.destroy()
        
        # Small delay to ensure window is closed
        self.update()
        
        # Then get player name
        player_name = simpledialog.askstring("Nom du joueur", "Entrez votre nom:")
        if not player_name:
            player_name = "Joueur"
        
        # Initialize game
        self.game = Game()
        self.game.setup(player_name)
        self.original_stdout = sys.stdout
        
        # Update display
        self._update_display()
        
        # Redirect stdout
        sys.stdout = OutputRedirector(self.output_text)
        self.game.print_welcome()
    
    def _set_background_image(self):
        """Set the background image for the main window."""
        assets_dir = Path(__file__).parent / 'assets'
        
        # Try different possible filenames
        possible_names = ['splash_screen.png', 'splash_screen .png', 'splash_screen.PNG']
        splash_path = None
        
        for name in possible_names:
            path = assets_dir / name
            if path.exists():
                splash_path = path
                break
        
        try:
            if splash_path and splash_path.exists():
                # Load and resize image
                img = Image.open(splash_path)
                img = img.resize((1400, 800), Image.Resampling.LANCZOS)
                self.bg_photo = ImageTk.PhotoImage(img)
                
                # Create background label
                bg_label = tk.Label(self, image=self.bg_photo)
                bg_label.image = self.bg_photo
                bg_label.place(x=0, y=0, relwidth=1, relheight=1)
                bg_label.lower()
            else:
                # Fallback to solid color if image not found
                self.configure(bg='#1a1a1a')
        except Exception as e:
            print(f"Erreur chargement image: {e}")
            self.configure(bg='#1a1a1a')
        
    def _setup_styles(self):
        """Setup TTK styles for a modern look."""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure colors
        bg_color = '#1a1a1a'
        fg_color = '#ffffff'
        accent_color = '#4A90E2'
        
        style.configure('TFrame', background=bg_color)
        style.configure('TLabel', background=bg_color, foreground=fg_color)
        style.configure('TButton', font=('Helvetica', 9), padding=5)
        style.configure('Title.TLabel', background=bg_color, foreground=accent_color, 
                       font=('Helvetica', 14, 'bold'))
        style.configure('Subtitle.TLabel', background=bg_color, foreground='#888888',
                       font=('Helvetica', 10, 'bold'))
        style.configure('TEntry', fieldbackground='#2c2c2c', foreground=fg_color)
        style.configure('Output.TFrame', background=bg_color, relief='sunken', borderwidth=1)
        
    def _setup_gui(self):
        """Setup the main GUI layout."""
        # Main container with semi-transparent background
        main_frame = ttk.Frame(self)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Create background for left side (map and room)
        left_bg = tk.Frame(main_frame, bg='#1a1a1a', highlightthickness=0)
        left_bg.pack(side=tk.LEFT, fill=tk.BOTH, expand=False, padx=(0, 10))
        
        # Left side: Map and current room
        left_frame = ttk.Frame(left_bg)
        left_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Map title
        map_title = ttk.Label(left_frame, text="CARTE DU JEU", style='Title.TLabel')
        map_title.pack(pady=(0, 5))
        
        # Map canvas
        self.map_canvas = tk.Canvas(left_frame, width=280, height=280, bg='#2c2c2c', 
                                    relief='sunken', borderwidth=2)
        self.map_canvas.pack(pady=(0, 10))
        self._draw_map()
        
        # Current room frame
        room_frame = tk.LabelFrame(left_frame, text="Salle Actuelle", padx=10, pady=10,
                                  bg='#1a1a1a', fg='#4A90E2', font=('Helvetica', 10, 'bold'),
                                  relief='sunken', borderwidth=2)
        room_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Room image
        self.room_canvas = tk.Canvas(room_frame, width=280, height=200, bg='black',
                                     relief='sunken', borderwidth=2)
        self.room_canvas.pack()
        
        # Right side: Main content with background
        right_bg = tk.Frame(main_frame, bg='#1a1a1a', highlightthickness=0)
        right_bg.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        right_frame = ttk.Frame(right_bg)
        right_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Output area with title
        output_title = ttk.Label(right_frame, text="MESSAGES DU JEU", style='Title.TLabel')
        output_title.pack(anchor='w', pady=(0, 5))
        
        output_frame = ttk.Frame(right_frame, style='Output.TFrame')
        output_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        self.output_text = tk.Text(output_frame, wrap=tk.WORD, bg='#0a0a0a', 
                                   fg='#00ff00', font=('Courier New', 9),
                                   relief='flat', borderwidth=0)
        self.output_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        scrollbar = ttk.Scrollbar(output_frame, command=self.output_text.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.output_text.config(yscrollcommand=scrollbar.set)
        
        # Commands frame
        commands_title = ttk.Label(right_frame, text="ACTIONS DISPONIBLES", style='Title.TLabel')
        commands_title.pack(anchor='w', pady=(0, 5))
        
        commands_frame = ttk.Frame(right_frame)
        commands_frame.pack(fill=tk.BOTH, expand=False, pady=(0, 10))
        
        # Create command buttons in a grid
        self._create_command_buttons(commands_frame)
        
        # Input area
        input_title = ttk.Label(right_frame, text="ENTREZ UNE COMMANDE", style='Title.TLabel')
        input_title.pack(anchor='w', pady=(0, 5))
        
        input_frame = ttk.Frame(right_frame)
        input_frame.pack(fill=tk.X, expand=False)
        
        self.input_var = tk.StringVar()
        self.input_entry = ttk.Entry(input_frame, textvariable=self.input_var)
        self.input_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        self.input_entry.bind('<Return>', self._on_enter)
        self.input_entry.focus()
        
        send_btn = ttk.Button(input_frame, text="Envoyer", command=self._on_enter)
        send_btn.pack(side=tk.RIGHT)
        
    def _create_command_buttons(self, parent):
        """Create interactive command buttons."""
        # Direction buttons
        directions_frame = ttk.LabelFrame(parent, text="Déplacement", padding=10)
        directions_frame.pack(side=tk.LEFT, padx=5, expand=False)
        
        # Arrow buttons layout
        ttk.Button(directions_frame, text="↑ N", width=6, 
                  command=lambda: self._execute_command('go n')).grid(row=0, column=1, padx=2, pady=2)
        ttk.Button(directions_frame, text="← O", width=6,
                  command=lambda: self._execute_command('go o')).grid(row=1, column=0, padx=2, pady=2)
        ttk.Button(directions_frame, text="↓ S", width=6,
                  command=lambda: self._execute_command('go s')).grid(row=1, column=1, padx=2, pady=2)
        ttk.Button(directions_frame, text="E →", width=6,
                  command=lambda: self._execute_command('go e')).grid(row=1, column=2, padx=2, pady=2)
        ttk.Button(directions_frame, text="⬆ U", width=6,
                  command=lambda: self._execute_command('go u')).grid(row=0, column=0, padx=2, pady=2)
        ttk.Button(directions_frame, text="⬇ D", width=6,
                  command=lambda: self._execute_command('go d')).grid(row=0, column=2, padx=2, pady=2)
        
        # Inventory and look
        actions_frame = ttk.LabelFrame(parent, text="Interaction", padding=10)
        actions_frame.pack(side=tk.LEFT, padx=5, expand=False)
        
        ttk.Button(actions_frame, text="📋 Inventaire", width=12,
                  command=lambda: self._execute_command('inventory')).pack(pady=2, fill=tk.X)
        ttk.Button(actions_frame, text="👁 Regarder", width=12,
                  command=lambda: self._execute_command('look')).pack(pady=2, fill=tk.X)
        ttk.Button(actions_frame, text="💬 Parler", width=12,
                  command=lambda: self._on_talk()).pack(pady=2, fill=tk.X)
        ttk.Button(actions_frame, text="🔍 Ramasser", width=12,
                  command=lambda: self._on_take()).pack(pady=2, fill=tk.X)
        ttk.Button(actions_frame, text="📦 Déposer", width=12,
                  command=lambda: self._on_drop()).pack(pady=2, fill=tk.X)
        ttk.Button(actions_frame, text="⏮ Retour", width=12,
                  command=lambda: self._execute_command('back')).pack(pady=2, fill=tk.X)
        ttk.Button(actions_frame, text="📜 Historique", width=12,
                  command=lambda: self._execute_command('history')).pack(pady=2, fill=tk.X)
        
        # Quest and game
        quest_frame = ttk.LabelFrame(parent, text="Quêtes", padding=10)
        quest_frame.pack(side=tk.LEFT, padx=5, expand=False)
        
        ttk.Button(quest_frame, text="📜 Quêtes", width=12,
                  command=lambda: self._execute_command('quests')).pack(pady=2, fill=tk.X)
        ttk.Button(quest_frame, text="🏆 Récompenses", width=12,
                  command=lambda: self._execute_command('rewards')).pack(pady=2, fill=tk.X)
        ttk.Button(quest_frame, text="❓ Aide", width=12,
                  command=lambda: self._execute_command('help')).pack(pady=2, fill=tk.X)
        ttk.Button(quest_frame, text="🚪 Quitter", width=12,
                  command=lambda: self._execute_command('quit')).pack(pady=2, fill=tk.X)
        
    def _draw_map(self):
        """Draw the game map on the canvas with actual game connections."""
        self.map_canvas.delete('all')
        
        # Define room positions on the map (x, y) - centered with margins
        room_positions = {
            "Poste de Police": (140, 50),
            "Ruelle du centre": (140, 110),
            "Hôtel abandonné": (210, 110),
            "Toit de l'immeuble": (210, 50),
            "Chambre 407": (210, 80),
            "Place du Lys": (140, 170),
            "Archives municipales": (140, 230),
            "Métro désaffecté": (210, 170),
            "Salle secrète du LYS": (210, 230),
            "Local technique du métro": (260, 170),
            "Salle d'interrogatoire": (70, 50),
        }
        
        # Check if game is initialized
        if not hasattr(self, 'game') or not self.game or not self.game.player:
            current_room = None
            connections = set()
        else:
            current_room = self.game.player.current_room.name if self.game.player else None
            
            # Generate connections dynamically from actual game rooms
            connections = set()
            for room in self.game.rooms:
                if room.name in room_positions:
                    for exit_dir, exit_room in room.exits.items():
                        if exit_room and exit_room.name in room_positions:
                            # Add both directions to avoid duplicates
                            pair = tuple(sorted([room.name, exit_room.name]))
                            connections.add(pair)
        
        # Draw connections first
        for room1, room2 in connections:
            if room1 in room_positions and room2 in room_positions:
                x1, y1 = room_positions[room1]
                x2, y2 = room_positions[room2]
                self.map_canvas.create_line(x1, y1, x2, y2, fill='#444444', width=2)
        
        # Draw rooms
        if hasattr(self, 'game') and self.game:
            for room in self.game.rooms:
                if room.name not in room_positions:
                    continue
                    
                x, y = room_positions[room.name]
                
                if room.name == current_room:
                    # Current room in yellow
                    self.map_canvas.create_oval(x-12, y-12, x+12, y+12, 
                                               fill='#FFD700', outline='#FFA500', width=2)
                    self.map_canvas.create_text(x, y, text='●', fill='#FFD700', font=('Arial', 16))
                else:
                    # Other rooms in blue
                    self.map_canvas.create_oval(x-10, y-10, x+10, y+10,
                                               fill='#4A90E2', outline='#2c5aa0', width=1)
                    self.map_canvas.create_text(x, y, text='●', fill='#4A90E2', font=('Arial', 12))
        else:
            # No game yet - just draw all rooms in blue
            for room_name, (x, y) in room_positions.items():
                self.map_canvas.create_oval(x-10, y-10, x+10, y+10,
                                           fill='#4A90E2', outline='#2c5aa0', width=1)
                self.map_canvas.create_text(x, y, text='●', fill='#4A90E2', font=('Arial', 12))
        
        # Draw legend
        self.map_canvas.create_text(140, 275, text="● Bleu: Autres | ● Jaune: Position actuelle",
                                   fill='#888888', font=('Arial', 8))
    
    def _update_display(self):
        """Update the room image and map."""
        if not self.game or not self.game.player or not self.game.player.current_room:
            return
        
        room = self.game.player.current_room
        assets_dir = Path(__file__).parent / 'assets'
        
        # Update room image
        if room.image:
            image_path = assets_dir / room.image
        else:
            image_path = None
        
        try:
            if image_path and image_path.exists():
                img = Image.open(image_path)
                img = img.resize((400, 300), Image.Resampling.LANCZOS)
                self.photo = ImageTk.PhotoImage(img)
                self.room_canvas.delete('all')
                self.room_canvas.create_image(200, 150, image=self.photo)
            else:
                self._draw_text_room()
        except Exception as e:
            self._draw_text_room()
        
        # Update map
        self._draw_map()
    
    def _draw_text_room(self):
        """Draw room info as text fallback."""
        room = self.game.player.current_room
        self.room_canvas.delete('all')
        self.room_canvas.create_text(200, 150, text=f"{room.name}\n\n{room.description}",
                                     fill='white', font=('Helvetica', 10), justify='center',
                                     width=350)
    
    def _execute_command(self, command):
        """Execute a game command."""
        if self.game.finished:
            messagebox.showinfo("Jeu terminé", "La partie est finie.")
            return
        
        print(f"> {command}\n")
        self.game.process_command(command)
        self._update_display()
        
        if self.game.finished:
            self.input_entry.config(state='disabled')
            messagebox.showinfo("Fin du jeu", "Partie terminée!")
    
    def _on_talk(self):
        """Handle talk command with character selection."""
        room = self.game.player.current_room
        if not room.characters:
            print("\nIl n'y a personne à qui parler ici.\n")
            return
        
        characters = [c.name for c in room.characters]
        dialog = tk.Toplevel(self)
        dialog.title("Parler à...")
        ttk.Label(dialog, text="Choisissez un personnage:").pack(padx=10, pady=10)
        
        for char_name in characters:
            ttk.Button(dialog, text=char_name,
                      command=lambda n=char_name: self._do_talk(n, dialog)).pack(pady=5, padx=10, fill=tk.X)
    
    def _do_talk(self, char_name, dialog):
        """Execute the talk command."""
        dialog.destroy()
        self._execute_command(f'talk {char_name}')
    
    def _on_take(self):
        """Handle take command with item selection."""
        room = self.game.player.current_room
        if not room.items:
            print("\nIl n'y a rien à ramasser ici.\n")
            return
        
        items = [item.name for item in room.items]
        dialog = tk.Toplevel(self)
        dialog.title("Ramasser...")
        ttk.Label(dialog, text="Choisissez un objet:").pack(padx=10, pady=10)
        
        for item_name in items:
            ttk.Button(dialog, text=item_name,
                      command=lambda n=item_name: self._do_take(n, dialog)).pack(pady=5, padx=10, fill=tk.X)
    
    def _do_take(self, item_name, dialog):
        """Execute the take command."""
        dialog.destroy()
        self._execute_command(f'take {item_name}')
    
    def _on_drop(self):
        """Handle drop command with item selection."""
        if not self.game.player.inventory:
            print("\nVous n'avez rien à déposer.\n")
            return
        
        items = [item.name for item in self.game.player.inventory]
        dialog = tk.Toplevel(self)
        dialog.title("Déposer...")
        ttk.Label(dialog, text="Choisissez un objet:").pack(padx=10, pady=10)
        
        for item_name in items:
            ttk.Button(dialog, text=item_name,
                      command=lambda n=item_name: self._do_drop(n, dialog)).pack(pady=5, padx=10, fill=tk.X)
    
    def _do_drop(self, item_name, dialog):
        """Execute the drop command."""
        dialog.destroy()
        self._execute_command(f'drop {item_name}')
    
    def _on_enter(self, event=None):
        """Handle Enter key in input."""
        command = self.input_var.get().strip()
        self.input_var.set('')
        if command:
            self._execute_command(command)


class OutputRedirector:
    """Redirect stdout to Text widget."""
    
    def __init__(self, text_widget):
        self.text_widget = text_widget
    
    def write(self, string):
        """Write to text widget."""
        self.text_widget.insert(tk.END, string)
        self.text_widget.see(tk.END)
    
    def flush(self):
        """Flush method for file-like objects."""
        pass


def main():
    try:
        app = GameGUIEnhanced()
        app.mainloop()
    except Exception as e:
        print(f"Erreur: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
