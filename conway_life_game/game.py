import numpy as np
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation


class CellNetwork(object):
    OFF = 100
    ON = 150

    def __init__(self, size, p=0.5):
        """
        细胞网格网络
        :param size: 网络长度和宽度
        :param p: 随机生成细胞中，状态为ON的细胞出现的概率，默认为0.5
        """
        # 初始化
        self.size = size
        self.status_array = np.random.choice(
            (self.OFF, self.ON),
            self.size * self.size,
            p=(1 - p, p)
        ).reshape(self.size, self.size).astype(np.uint8)

    def update_cell(self, r, c):
        # 计算邻居ON个数
        on_cell_count = 0
        for delta_r, delta_c in ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)):
            round_r = (r + delta_r) % self.size
            round_c = (c + delta_c) % self.size
            on_cell_count = on_cell_count + int(self.status_array[round_r, round_c] == self.ON)

        # 更新状态
        if self.status_array[r, c] == self.OFF and on_cell_count == 3:
            self.status_array[r, c] = self.ON
        elif self.status_array[r, c] == self.ON and (on_cell_count < 2 or on_cell_count > 3):
            self.status_array[r, c] = self.OFF

    def update(self, frame_id, img):
        # 更新所有细胞
        for r in range(self.size):
            for c in range(self.size):
                self.update_cell(r, c)

        # 将更新展现到画布上
        img.set_data(self.status_array)
        return img

    def start(self, refresh_interval=None):
        if refresh_interval is None:
            refresh_interval = 25 * self.size // 10 + 25
        fig, ax = plt.subplots()
        img = ax.imshow(self.status_array, cmap='gray', vmin=0, vmax=255, interpolation='nearest')
        ani = FuncAnimation(fig, self.update, fargs=(img, ), interval=refresh_interval)
        plt.show()


if __name__ == '__main__':
    cell_network = CellNetwork(100, p=0.1)
    cell_network.start(500)
