import tkinter as tk
from tkinter import messagebox
import random

# Game Configuration
TILE_SIZE = 40
GRID_WIDTH = 12
GRID_HEIGHT = 10

class HashmapGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Tile Crawler - HashMap & Tkinter Game")
        
        # Player state
        self.player_pos = [0, 0]
        self.score = 0
        self.total_gold = 0
        
        # HashMap storing world grid: Key = (x, y) tuple, Value = entity type ("wall", "gold")
        self.game_map = {}
        
        # UI Header
        self.info_label = tk.Label(
            root, 
            text="Use Arrow Keys or WASD to move!", 
            font=("Arial", 12, "bold"),
            bg="#0f172a", 
            fg="#f8fafc",
            padding=10
        )
        self.info_label.pack(fill=tk.X)

        # Tkinter Canvas View
        self.canvas = tk.Canvas(
            root, 
            width=GRID_WIDTH * TILE_SIZE, 
            height=GRID_HEIGHT * TILE_SIZE, 
            bg="#1e293b"
        )
        self.canvas.pack()

        # Keyboard Controls
        self.root.bind("<Up>", lambda e: self.move(0, -1))
        self.root.bind("<Down>", lambda e: self.move(0, 1))
        self.root.bind("<Left>", lambda e: self.move(-1, 0))
        self.root.bind("<Right>", lambda e: self.move(1, 0))
        self.root.bind("<w>", lambda e: self.move(0, -1))
        self.root.bind("<s>", lambda e: self.move(0, 1))
        self.root.bind("<a>", lambda e: self.move(-1, 0))
        self.root.bind("<d>", lambda e: self.move(1, 0))

        self.generate_map()
        self.render()

    def generate_map(self):
        """Populates the HashMap game_map with walls and gold."""
        self.game_map.clear()
        
        # Populate HashMap dynamically
        for x in range(GRID_WIDTH):
            for y in range(GRID_HEIGHT):
                if (x, y) == (0, 0):
                    continue  # Player start tile
                
                rand_val = random.random()
                if rand_val < 0.18:
                    self.game_map[(x, y)] = "wall"
                elif rand_val < 0.28:
                    self.game_map[(x, y)] = "gold"
                    self.total_gold += 1

    def move(self, dx, dy):
        """Handles O(1) collision checking and state update using HashMap."""
        new_x = self.player_pos[0] + dx
        new_y = self.player_pos[1] + dy

        # Boundary checks
        if not (0 <= new_x < GRID_WIDTH and 0 <= new_y < GRID_HEIGHT):
            return

        # O(1) HashMap lookup for wall collision
        if self.game_map.get((new_x, new_y)) == "wall":
            return  # Blocked move

        # Update player coordinate
        self.player_pos = [new_x, new_y]

        # O(1) HashMap check for item interaction
        if self.game_map.get((new_x, new_y)) == "gold":
            self.score += 10
            del self.game_map[(new_x, new_y)]  # Remove item from map state

        self.render()

        # Win condition check
        if "gold" not in self.game_map.values():
            messagebox.showinfo("Victory!", f"You collected all gold! Final Score: {self.score}")
            self.root.destroy()

    def render(self):
        """Renders grid objects from HashMap model onto Canvas view."""
        self.canvas.delete("all")

        # Draw HashMap entries
        for (x, y), tile_type in self.game_map.items():
            x1, y1 = x * TILE_SIZE, y * TILE_SIZE
            x2, y2 = x1 + TILE_SIZE, y1 + TILE_SIZE

            if tile_type == "wall":
                self.canvas.create_rectangle(x1, y1, x2, y2, fill="#64748b", outline="#334155")
            elif tile_type == "gold":
                self.canvas.create_oval(x1 + 8, y1 + 8, x2 - 8, y2 - 8, fill="#f59e0b", outline="#b45309")

        # Draw Player
        px1, py1 = self.player_pos[0] * TILE_SIZE, self.player_pos[1] * TILE_SIZE
        px2, py2 = px1 + TILE_SIZE, py1 + TILE_SIZE
        self.canvas.create_oval(px1 + 4, py1 + 4, px2 - 4, py2 - 4, fill="#38bdf8", outline="#0284c7")

        # Update Info Bar
        remaining = sum(1 for v in self.game_map.values() if v == "gold")
        self.info_label.config(text=f"Score: {self.score} | Gold Remaining: {remaining}")

if __name__ == "__main__":
    root = tk.Tk()
    app = HashmapGame(root)
    root.mainloop()
