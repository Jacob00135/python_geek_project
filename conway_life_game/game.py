import numpy as np


class Cell(object):

    def __init__(self, row, col, status):
        self.row = row
        self.col = col
        self.status = status

    def __str__(self):
        # TODO 在编写页面后删除该方法
        return self.__repr__()

    def __repr__(self):
        # TODO 在编写页面后删除该方法
        return '<Cell ({}, {}) {}>'.format(self.row, self.col, 'ON' if self.status else 'OFF')


class CellNetwork(object):

    def __init__(self, size, p=0.5):
        """
        细胞网格网络
        :param size: 网络长度和宽度
        :param p: 随机生成细胞中，状态为ON的细胞出现的概率，默认为0.5
        """
        super(CellNetwork, self).__init__()
        self.size = size

        # 初始化
        status_array = np.random.choice((0, 1), self.size * self.size, p=(1 - p, p)).reshape(self.size, self.size)
        self.cell_list = []
        for r in range(self.size):
            row = []
            for c in range(self.size):
                row.append(Cell(r, c, status_array[r, c]))
            self.cell_list.append(row)

        # TODO 用于迭代器，在编写页面后删除这些属性
        self.r = 0
        self.c = -1

    def __getitem__(self, item):
        # TODO 在编写页面后删除该方法
        r, c = item
        return self.cell_list[r][c]

    def __iter__(self):
        # TODO 在编写页面后删除该方法
        self.r = 0
        self.c = -1
        return self

    def __next__(self):
        # TODO 在编写页面后删除该方法
        self.c = self.c + 1
        if self.c >= self.size:
            self.r = self.r + 1
            if self.r >= self.size:
                raise StopIteration
            self.c = 0
        return self.cell_list[self.r][self.c]

    def __str__(self):
        # TODO 在编写页面后删除该方法
        return self.__repr__()

    def __repr__(self):
        # TODO 在编写页面后删除该方法
        result = []
        for r in range(self.size):
            row = []
            for c in range(self.size):
                row.append(str(self.cell_list[r][c].status))
            result.append(' '.join(row))
        return '\n'.join(result)

    def update_cell(self, cell):
        # 计算邻居ON个数
        on_cell_count = 0
        for delta_r, delta_c in ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)):
            r = (cell.row + delta_r) % self.size
            c = (cell.col + delta_c) % self.size
            on_cell_count = on_cell_count + self[r, c].status

        # 更新状态
        if cell.status == 0 and on_cell_count == 3:
            cell.status = 1
        elif cell.status == 1 and (on_cell_count < 2 or on_cell_count > 3):
            cell.status = 0

    def update(self, r, c):
        self.update_cell(self.cell_list[r][c])

    def update_all_cell(self):
        for r in range(self.size):
            for c in range(self.size):
                self.update_cell(self.cell_list[r][c])


if __name__ == '__main__':
    cell_network = CellNetwork(10, p=0.9)
    print(cell_network)
    cell_network.update_all_cell()
    print(cell_network)
