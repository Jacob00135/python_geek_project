import os
import math
import turtle
from random import randint, uniform, random
from datetime import datetime
from matplotlib import pyplot as plt

root_path = os.path.realpath(os.path.dirname(__file__))


class Spiro(object):

    def __init__(self, R, r, l, circle_center=(0, 0), color=(0, 0, 0), quick_mode=False, delay=1):
        self.x, self.y = circle_center
        self.quick_mode = quick_mode

        # 初始化海龟
        self.t = turtle.Turtle()
        self.t.shape('turtle')  # 设置画笔形状为海龟
        self.step = 5
        self.t.color(color)
        turtle.delay(delay)

        # 设置参数方程的参数
        self.R = int(R)  # 外圆半径
        self.r = int(r)  # 内圆半径
        self.l = l  # 笔尖与内圆圆心距离 / 内圆半径
        self.n_rot = self.r // math.gcd(self.r, self.R)  # 要画出完整图形，所需要转的最少圈数
        self.k = r / R

        # 重置参数，准备好画图
        self.restart()

    def restart(self):
        # 隐藏画笔
        self.t.hideturtle()

        # 提笔移动到起始位置
        self.t.up()
        x, y = self.get_x_y(0)
        if not self.quick_mode:
            self.setheading(x, y)
        self.t.setpos(x, y)
        self.t.down()

    def get_x_y(self, t):
        t = math.radians(t)
        t2 = t * (1 - self.k) / self.k
        x = self.R * ((1 - self.k) * math.cos(t) + self.l * self.k * math.cos(t2))
        y = self.R * ((1 - self.k) * math.sin(t) - self.l * self.k * math.sin(t2))
        return self.x + x, self.y + y

    def setheading(self, x, y):
        now_x, now_y = self.t.pos()
        distance = math.sqrt(pow(x - now_x, 2) + pow(y - now_y, 2))
        if abs(distance) < 1:
            return None
        a = math.acos((x - now_x) / distance)
        if y < now_y:
            a = 2 * math.pi - a
        angle = math.degrees(a)
        self.t.setheading(angle)

    def draw(self):
        if not self.quick_mode:
            self.t.showturtle()
        for t in range(0, 360 * self.n_rot + self.step, self.step):
            x, y = self.get_x_y(t)
            if not self.quick_mode:
                self.setheading(x, y)
            self.t.setpos(x, y)
        self.t.hideturtle()


class SpiroAnimator(object):

    def __init__(self, num_spiro=4, quick_mode=True, delay=0):
        self.num_spiro = num_spiro  # 在同一张画布上要绘制的万花尺图形个数
        self.quick_mode = quick_mode  # 是否开启快速绘制模式：隐藏海龟、不调整朝向
        self.delay = delay  # 越小绘制速度越快
        self.delta_t = 10  # 一个海龟的绘制时间，超出此时间将切换到另一个海龟
        self.draw_finish_count = 0  # 对绘制完成的曲线计数

        # 获取画布信息
        self.width = turtle.window_width()
        self.height = turtle.window_height()

        # 初始化曲线
        self.spiro_list = []
        self.generate_spiro()

    def generate_spiro(self):
        max_R = min(self.width, self.height) // 2
        for i in range(self.num_spiro):
            R = randint(50, max_R)
            r = randint(10, R * 9 // 10)
            l = uniform(0.1, 0.9)
            x = randint(R - self.width // 2, self.width // 2 - R)
            y = randint(R - self.height // 2, self.height // 2 - R)
            color = (random(), random(), random())
            spiro = Spiro(R, r, l, circle_center=(x, y), color=color, quick_mode=self.quick_mode, delay=self.delay)
            self.spiro_list.append(spiro)

    def draw_sequence(self):
        for spiro in self.spiro_list:
            spiro.draw()

    def restart(self):
        turtle.clearscreen()
        self.spiro_list = []
        self.generate_spiro()


class Spirograph(object):

    def __init__(self, R=None, r=None, l=None, random_graph=False, title=True):
        # 设置参数方程的参数
        if random_graph:
            self.R, self.r = self.get_random_param()
            while self.r // math.gcd(self.r, self.R) > 100:
                self.R, self.r = self.get_random_param()
            self.l = uniform(0.1, 0.9)
            self.color = (random(), random(), random())
        else:
            self.R = int(R)  # 外圆半径
            self.r = int(r)  # 内圆半径
            self.l = l  # 笔尖与内圆圆心距离 / 内圆半径
            self.color = 'black'
        self.n_rot = self.r // math.gcd(self.r, self.R)  # 要画出完整图形，所需要转的最少圈数
        self.k = self.r / self.R

        # 画图相关参数
        self.step = 3  # 画图时选点步长
        self.before_x = 0
        self.before_y = 0
        self.lw = 0.5

    def get_x_y(self, t):
        t = math.radians(t)
        t2 = t * (1 - self.k) / self.k
        x = self.R * ((1 - self.k) * math.cos(t) + self.l * self.k * math.cos(t2))
        y = self.R * ((1 - self.k) * math.sin(t) - self.l * self.k * math.sin(t2))
        return x, y

    def coord_generator(self):
        for t in range(0, 360 * self.n_rot + self.step, self.step):
            x, y = self.get_x_y(t)
            yield t, x, y

    @staticmethod
    def get_random_param(max_R=500, max_r=1000):
        R = randint(50, max_R)
        if random() < 0.5:
            r = randint(10, R * 9 // 10)
        else:
            r = randint(10, max_r)
        return R, r

    def draw(self):
        plt.figure()
        self.before_x, self.before_y = self.get_x_y(0)
        for t, x, y in self.coord_generator():
            plt.plot([self.before_x, x], [self.before_y, y], color=self.color, lw=self.lw)
            self.before_x, self.before_y = x, y
        plt.xlim(-self.R, self.R)
        plt.ylim(-self.R, self.R)
        plt.axis('image')
        plt.axis('off')
        plt.title('R = {}, r = {}, l = {}'.format(self.R, self.r, self.l))
        filename = 'spirograph-{}.png'.format(datetime.now().strftime('%Y-%M-%d-%H-%m-%S'))
        plt.savefig(os.path.join(root_path, 'images/{}'.format(filename)))
        plt.show()


def main(draw_method='turtle'):
    if draw_method == 'turtle':
        # 画图
        spiro_animator = SpiroAnimator(quick_mode=False)
        spiro_animator.draw_sequence()

        # 加入事件循环
        turtle.mainloop()
    elif draw_method == 'matplotlib':
        # spiro = Spirograph(300, 700, 0.4)
        # spiro.color = (random(), random(), random())
        spiro = Spirograph(random_graph=True)
        spiro.draw()


if __name__ == '__main__':
    main('matplotlib')
