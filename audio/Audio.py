import os

import pyaudio
from pydub import AudioSegment
from pydub.playback import play
# 该资源的绝对路径
code_path = os.path.dirname(os.path.abspath(__file__))


class Audio:
    # 具体实现
    def dxl(self, area='red',signal='fire',people='zero'):
        # 读取多个.wav文件
        audio_files = [f"./AudioFiles/dxl/area/{area}.wav", f"./AudioFiles/dxl/signal/{signal}.wav", f"./AudioFiles/dxl/people/{people}.wav"]
        audio_segments = [AudioSegment.from_wav(file) for file in audio_files]
        # 将音频片段组合成一个声音流
        combined_audio = sum(audio_segments)
        # 播放修改后的声音流
        play(combined_audio)

    def dz(self,area,left_right):
        # 读取多个.wav文件
        audio_files = [f"./AudioFiles/dz/left_right/{left_right}.wav",f"./AudioFiles/dz/area/{area}.wav"]
        audio_segments = [AudioSegment.from_wav(file) for file in audio_files]
        # 将音频片段组合成一个声音流
        combined_audio = sum(audio_segments)
        # 播放修改后的声音流
        play(combined_audio)


if __name__ == '__main__':
    # dxl
    area = 'red'
    signal = 'fall'
    people = 'one'
    a = Audio()
    a.dxl(area,signal,people)

    # dz
    area = 'a'
    left_right = 'left'
    a.dz(area,left_right)