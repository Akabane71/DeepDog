import os

import pyaudio
from pydub import AudioSegment
from pydub.playback import play
# 该资源的绝对路径
code_path = os.path.dirname(os.path.abspath(__file__))


class Audio:

    def __call__(self, area='red',signal='fire',people='zero'):
        return self.go(area, signal, people)

    # 具体实现
    def go(self, area,signal,people):
        base_path = '2024_DeepDogCup/audio/'
        # 读取多个.wav文件
        audio_files = [f"{code_path}/AudioFiles/area/{area}.wav", f"{code_path}/AudioFiles/signal/{signal}.wav", f"{code_path}/AudioFiles/people/{people}.wav"]
        audio_segments = [AudioSegment.from_wav(file) for file in audio_files]
        # 将音频片段组合成一个声音流
        combined_audio = sum(audio_segments)
        # 播放修改后的声音流
        play(combined_audio)

if __name__ == '__main__':
    area = 'red'
    signal = 'fall'
    people = 'one'
    a = Audio()
    a(area,signal,people)
