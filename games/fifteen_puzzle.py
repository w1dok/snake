import tkinter as tk
import random

class FifteenPuzzle:
    def __init__(self, root):
        self.root = root
        self.root.title("Пятнашки")
        self.tiles = list(range(1, 16)) + [None]
        random.shuffle(self.tiles)
        self.buttons = []
        self.create_widgets()

    def create_widgets(self):
        for i in range(4):
            row = []
            for j in range(4):
                tile = self.tiles[i * 4 + j]
                if tile is not None:
                    button = tk.Button(self.root, text=str(tile), width=4, 
                                       height=2, command=lambda t=tile: self.move_tile(t))
                else:
                    button = tk.Button(self.root, text="", width=4, height=2, state=tk.DISABLED)
                button.grid(row=i, column=j)
                row.append(button)
            self.buttons.append(row)

    def move_tile(self, tile):
        index = self.tiles.index(tile)
        empty_index = self.tiles.index(None)
        if self.is_adjacent(index, empty_index):
            self.tiles[empty_index], self.tiles[index] = self.tiles[index], self.tiles[empty_index]
            self.update_buttons()
            self.print_tiles()  # Выводим текущее состояние tiles

    def is_adjacent(self, index1, index2):
        row1, col1 = divmod(index1, 4)
        row2, col2 = divmod(index2, 4)
        return abs(row1 - row2) + abs(col1 - col2) == 1

    def update_buttons(self):
        for i in range(4):
            for j in range(4):
                tile = self.tiles[i * 4 + j]
                button = self.buttons[i][j]
                if tile is not None:
                    button.config(text=str(tile), state=tk.NORMAL)
                else:
                    button.config(text="", state=tk.DISABLED)

    def print_tiles(self):
        for i in range(4):
            print(self.tiles[i * 4:(i + 1) * 4])
        print()

if __name__ == "__main__":
    root = tk.Tk()
    game = FifteenPuzzle(root)
    root.mainloop()