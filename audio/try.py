from pydub import AudioSegment
from pydub.playback import play
try:
    # 读取多个.wav文件

    audio_files = ["./AudioFiles/dxl/area/red.wav", "./AudioFiles/dxl/signal/fire.wav", "./AudioFiles/dxl/people/zero.wav"]

    audio_segments = [AudioSegment.from_wav(file) for file in audio_files]

    # 将音频片段组合成一个声音流
    combined_audio = sum(audio_segments)

    # 加速倍数（例如，2表示两倍速）
    speed_multiplier = 1.2

    # 加速声音流
    speeded_audio = combined_audio.speedup(playback_speed=speed_multiplier)

    # 播放修改后的声音流
    play(speeded_audio)
except Exception as e:
    print(e)
