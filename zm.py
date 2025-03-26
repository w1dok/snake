import tkinter as tk
import random

class SnakeGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Snake Game")
        self.canvas = tk.Canvas(root, width=400, height=400, bg="black")
        self.canvas.pack()
        self.snake = [(20, 20), (20, 30), (20, 40)]
        self.food = self.create_food()
        self.direction = "Down"  # Направление движения змейки
        self.running = True
        self.paused = False  # Флаг для паузы
        self.speed = 250  # Скорость змейки (мс)
        self.root.bind("<KeyPress>", self.change_direction)
        self.update()

    def create_food(self):
        x = random.randint(0, 19) * 20
        y = random.randint(0, 19) * 20
        return (x, y)

    def change_direction(self, event):
        if event.keysym == "space":  # Если нажата клавиша пробела
            self.paused = not self.paused  # Переключаем состояние паузы
        elif not self.paused and event.keysym in ["Up", "Down", "Left", "Right"]:
            self.direction = event.keysym

    def move_snake(self):
        # Получаем координаты головы змейки (последний элемент списка self.snake)
        head_x, head_y = self.snake[-1]

        # Определяем новые координаты головы в зависимости от текущего направления
        if self.direction == "Up":
            new_head = (head_x, head_y - 20)
        elif self.direction == "Down":
            new_head = (head_x, head_y + 20)
        elif self.direction == "Left":
            new_head = (head_x - 20, head_y)
        elif self.direction == "Right":
            new_head = (head_x + 20, head_y)
        
        # Логика для прохождения сквозь края
        # Если координаты выходят за пределы (400x400), используем модуль (%)
        # Это позволяет змейке появляться с противоположной стороны
        new_head = (
            new_head[0] % 400,  # Если выходит за границу по X, появляется с противоположной стороны
            new_head[1] % 400   # Если выходит за границу по Y, появляется с противоположной стороны
        )
        
        # Проверяем, не столкнулась ли змейка с самой собой
        if new_head in self.snake:  # Если новая голова совпадает с любой частью тела
            self.running = False  # Останавливаем игру
            return  # Выходим из метода
        
        # Добавляем новую голову в список змейки
        self.snake.append(new_head)

        # Проверяем, съела ли змейка еду
        if new_head == self.food: # Если координаты головы совпадают с координатами еды
            self.food = self.create_food() # Создаем новую еду в случайном месте
        else:
            # Если еда не съедена, удаляем последний сегмент змейки (хвост)
            self.snake.pop(0)

    def update(self):
        if self.running and not self.paused:  # Проверяем, что игра не на паузе
            self.move_snake()
            self.canvas.delete(tk.ALL)
            self.canvas.create_rectangle(self.food[0], self.food[1], self.food[0] + 20, self.food[1] + 20, fill="red")
            for x, y in self.snake:
                self.canvas.create_rectangle(x, y, x + 20, y + 20, fill="green")
        elif not self.running:
            self.canvas.create_text(300, 300, text="Game Over", fill="white", font=("Arial", 24))
        self.root.after(self.speed, self.update)

if __name__ == "__main__":
    root = tk.Tk()
    game = SnakeGame(root)
    root.mainloop()