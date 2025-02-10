import random


class Cell:
    def __init__(self, around_mines: int = 0, mine: bool = False):
        """
        Инициализация объектов.

        around_mines - количество мин
        mine - булева переменная, указывает, есть ли мина в клетке
        fl_open - булева переменная, указывает, открыта ли клетка
        """
        self.around_mines = around_mines
        self.mine = mine
        self.fl_open = False


class GamePole:
    def __init__(self, n: int, m: int):
        """
        Инициализация объектов.

        n - размер поля
        m - количество мин
        pole - 2D список клеток
        init - инициализация поля и расстановка мин рандомно
        """
        self.n = n
        self.m = m
        self.pole = [[Cell() for _ in range(n)] for _ in range(n)]
        self.init()

    def init(self):
        """ Инициализация поля и расстановка мин рандомно. """

        # Генерация случайных координат для мин
        mines = random.sample(range(self.n * self.n), self.m)

        for idx in mines:
            row = idx // self.n
            col = idx % self.n
            self.pole[row][col].mine = True

            # Увеличение количества мин вокруг соседних клеток
            for i in range(row - 1, row + 2):
                for j in range(col - 1, col + 2):
                    if 0 <= i < self.n and 0 <= j < self.n and not self.pole[i][j].mine:
                        self.pole[i][j].around_mines += 1

    def show(self):
        """ Отображение поля в консоли. """
        for row in self.pole:
            for cell in row:
                if cell.fl_open:
                    print(cell.around_mines, end=" ")
                else:
                    print("#", end=" ")
            print()


game = GamePole(10, 12)
game.show()
