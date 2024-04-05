import pyaudio
from pydub import AudioSegment
from pydub.playback import play

class Audio:
<<<<<<< HEAD

    def __call__(self, area='red',signal='fire',people='zero'):
=======
    def __call__(self, area='red',signal='fire',people = 0):
>>>>>>> 3a8f4b3 (2024-4-5_第一次提交)
        return self.go(area,signal,people)

    # 具体实现
    def go(self, area,signal,people):
        # 读取多个.wav文件
        audio_files = [f"./AudioFiles/area/{area}.wav", f"./AudioFiles/signal/{signal}.wav", f"./AudioFiles/people/{people}.wav"]
        audio_segments = [AudioSegment.from_wav(file) for file in audio_files]
        # 将音频片段组合成一个声音流
        combined_audio = sum(audio_segments)
        # 播放修改后的声音流
        play(combined_audio)

if __name__ == '__main__':
    area = 'red'
<<<<<<< HEAD
    signal = 'fall'
    people = 'one'
=======
    signal = 'fire'
    people = '0'
>>>>>>> 3a8f4b3 (2024-4-5_第一次提交)
    a = Audio()
    a(area,signal,people)
