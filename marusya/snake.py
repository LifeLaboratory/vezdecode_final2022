import curses
from random import randint


class Field:
    def __init__(self, size, field=None):
        self.size = size
        self.icons = {
            0: ' . ',
            1: ' * ',
            2: ' # ',
            3: ' & ',
        }
        self.snake_coords = []
        if field:
            self.field = field
        else:
            self._generate_field()
        self.add_entity()

    def add_entity(self):

        while (True):
            i = randint(0, self.size - 1)
            j = randint(0, self.size - 1)
            entity = [i, j]

            if entity not in self.snake_coords:
                self.field[i][j] = 3
                break

    def _generate_field(self):
        self.field = [[0 for j in range(self.size)] for i in range(self.size)]

    def _clear_field(self):
        self.field = [[j if j != 1 and j != 2 else 0 for j in i] for i in self.field]

    def render(self):
        size = self.size
        self._clear_field()

        for i, j in self.snake_coords:
            self.field[i][j] = 1

        head = self.snake_coords[-1]
        self.field[head[0]][head[1]] = 2
        matrix = []
        for i in range(size):
            row = ''
            for j in range(size):
                row += self.icons[self.field[i][j]]
            matrix.append(row)
        return matrix

    def get_entity_pos(self):
        for i in range(self.size):
            for j in range(self.size):
                if self.field[i][j] == 3:
                    return [i, j]

        return [-1, -1]

    def is_snake_eat_entity(self):
        entity = self.get_entity_pos()
        head = self.snake_coords[-1]
        return entity == head


class Snake:
    def __init__(self, name, coords=None):
        self.name = name
        self.direction = 'вправо'

        self.coords = coords if coords else [[0, 0], [0, 1], [0, 2], [0, 3]]

    def level_up(self):
        a = self.coords[0]
        b = self.coords[1]

        tail = a[:]

        if a[0] < b[0]:
            tail[0] -= 1
        elif a[1] < b[1]:
            tail[1] -= 1
        elif a[0] > b[0]:
            tail[0] += 1
        elif a[1] > b[1]:
            tail[1] += 1

        tail = self._check_limit(tail)
        self.coords.insert(0, tail)

    def is_alive(self):
        head = self.coords[-1]
        snake_body = self.coords[:-1]
        return head not in snake_body

    def _check_limit(self, point):
        if point[0] > self.field.size - 1:
            point[0] = 0
        elif point[0] < 0:
            point[0] = self.field.size - 1
        elif point[1] < 0:
            point[1] = self.field.size - 1
        elif point[1] > self.field.size - 1:
            point[1] = 0

        return point

    def move(self, direction):
        head = self.coords[-1][:]

        if direction == 'вверх':
            head[0] -= 1
        elif direction == 'вниз':
            head[0] += 1
        elif direction == 'вправо':
            head[1] += 1
        elif direction == 'влево':
            head[1] -= 1

        head = self._check_limit(head)

        del (self.coords[0])
        self.coords.append(head)
        self.field.snake_coords = self.coords

        if not self.is_alive():
            return True

        if self.field.is_snake_eat_entity():
            self.level_up()
            self.field.add_entity()

    def set_field(self, field):
        self.field = field


def main(direction):

    field = Field(10)
    snake = Snake("Маруся")
    snake.set_field(field)
    alive = snake.move(direction)


