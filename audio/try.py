from pydub import AudioSegment
from pydub.playback import play

# 读取多个.wav文件
<<<<<<< HEAD
audio_files = ["./AudioFiles/area/red.wav", "./AudioFiles/signal/fire.wav", "./AudioFiles/people/zero.wav"]
=======
audio_files = ["./AudioFiles/area/red.wav", "./AudioFiles/signal/fire.wav", "./AudioFiles/people/0.wav"]
>>>>>>> 3a8f4b3 (2024-4-5_第一次提交)
audio_segments = [AudioSegment.from_wav(file) for file in audio_files]

# 将音频片段组合成一个声音流
combined_audio = sum(audio_segments)

# 在这里可以对combined_audio进行其他处理，比如改变音调、添加混响等

# 播放修改后的声音流
play(combined_audio)
