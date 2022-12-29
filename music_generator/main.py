import os
import wave
import numpy as np
import pygame
from collections import deque
from random import random, choice
from time import sleep

root_path = os.path.realpath(os.path.dirname(__file__))


class NoteGenerator(object):
    sample_rate = 44100  # 每秒的采样率，44100是CD中使用的采样率

    def generate_note(self, frequency: float) -> bytes:
        """使用Karplus-Strong算法生成一个音符"""
        # 计算基本参数
        note_length = 1  # 音符的长短，以秒为单位
        num_sample = self.sample_rate * note_length
        alpha = 0.996  # 音符衰减参数

        # 生成环形缓冲区
        buffer = deque()
        buffer_size = int(self.sample_rate / frequency)
        for i in range(buffer_size):
            buffer.append(random() * 0.5)

        # 生成音符数据
        samples = np.zeros(num_sample, 'float32')
        for i in range(num_sample):
            samples[i] = buffer[0]
            avg = (buffer[0] + buffer[1]) * 0.5 * alpha
            buffer.append(avg)
            buffer.popleft()

        # 转换成可写入的字节流并返回
        return (samples * 32767).astype('int16').tobytes()

    def save_audio(self, filename: str, data: bytes, save_dir: str = 'audio') -> None:
        # 检查目录是否存在
        save_dir_path = os.path.abspath(os.path.join(root_path, save_dir))
        if not os.path.exists(save_dir_path):
            os.mkdir(save_dir_path)

        # 纠正文件名
        if not filename.endswith('.wav'):
            filename = filename + '.wav'

        # 保存
        save_path = os.path.abspath(os.path.join(save_dir_path, filename))
        with wave.open(save_path, 'wb') as file:
            file.setparams((
                1,  # 单声道
                2,  # 2字节（16位）
                self.sample_rate,
                self.sample_rate,
                'NONE',
                'uncompressed'  # 无压缩格式
            ))
            file.writeframes(data)
            file.close()


class Note(object):

    def __init__(self, name, func):
        self.name = name
        self.func = func

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return self.name

    def __call__(self, *args, **kwargs):
        self.func(*args, **kwargs)


class FiveNote(object):
    # 小调五声音阶的频率
    frequency_map = {
        'C4': 261.6,
        'Eb': 311.1,
        'F': 349.2,
        'G': 392.0,
        'Bb': 466.2
    }

    def __init__(self):
        self.generate_five_note()

        pygame.mixer.pre_init(NoteGenerator.sample_rate, -16, 1, 2048)
        pygame.init()
        self.C4 = Note('C4', pygame.mixer.Sound(os.path.join(root_path, 'base_audio/C4.wav')).play)
        self.Eb = Note('Eb', pygame.mixer.Sound(os.path.join(root_path, 'base_audio/Eb.wav')).play)
        self.F = Note('F', pygame.mixer.Sound(os.path.join(root_path, 'base_audio/F.wav')).play)
        self.G = Note('G', pygame.mixer.Sound(os.path.join(root_path, 'base_audio/G.wav')).play)
        self.Bb = Note('Bb', pygame.mixer.Sound(os.path.join(root_path, 'base_audio/Bb.wav')).play)

    def generate_five_note(self) -> None:
        """生成基础的小调五声音阶"""
        # 检查是否需要生成
        generate = False
        for note_name in self.frequency_map.keys():
            file_path = os.path.join(root_path, 'base_audio/{}.wav'.format(note_name))
            if not os.path.exists(file_path):
                generate = True
                break
        if not generate:
            return None

        # 生成文件
        ng = NoteGenerator()
        for note_name, frequency in self.frequency_map.items():
            note = ng.generate_note(frequency)
            ng.save_audio(note_name, note, 'base_audio')

    @staticmethod
    def beats(n: int) -> Note:
        return Note('beats{}'.format(n), lambda: sleep(0.25 * n))

    def note_sequence(self, funcs: list) -> list:
        result = []
        for f in funcs:
            if callable(f):
                result.append(f)
            else:
                result.extend(self.note_sequence(f))

        return result

    def random_note(self) -> Note:
        return choice([self.C4, self.Eb, self.F, self.G, self.Bb])

    def random_note_sequence(self, length: int, p: tuple = (0.15, 0.7, 0.1, 0.05)) -> list:
        note_sequence = []
        for _ in range(length):
            note_sequence.append(self.random_note())
            random_beats = np.random.choice([1, 2, 4, 8], 1, p=p)[0]
            note_sequence.append(self.beats(random_beats))
        return note_sequence


def play(note_seq: list):
    note_seq = FiveNote().note_sequence(note_seq)
    for func in note_seq:
        func()


if __name__ == '__main__':
    fn = FiveNote()
    seq1 = fn.note_sequence([
        fn.C4,
        fn.beats(1),
    ])
    seq2 = fn.note_sequence([
        seq1,
        fn.G,
        fn.beats(1)
    ])
    seq3 = fn.note_sequence([
        seq2,
        fn.Eb,
        seq2,
        fn.beats(1),
        seq2,
        fn.beats(1)
    ])

    play([
        seq3,
        seq3
    ])
