from pydub import AudioSegment
from pydub.generators import Square
import simpleaudio as sa

def play_tone(frequency, duration, volume=0.5):
    # 8비트 음악은 주로 Square wave(사각파)로 생성
    sample_rate = 44100
    samples = Square(frequency).to_audio_segment(duration=duration, volume=volume).get_array_of_samples()
    audio = AudioSegment(samples.tobytes(), frame_rate=sample_rate, sample_width=samples.typecode, channels=1)
    
    # 파일로 저장하거나 바로 재생
    audio.export("8bit_music.wav", format="wav")
    wave_obj = sa.WaveObject.from_wave_file("8bit_music.wav")
    play_obj = wave_obj.play()
    play_obj.wait_done()

# 간단한 멜로디 생성 예제
notes = [440, 494, 523, 587, 659, 698, 784, 880] # A4, B4, C5, D5, E5, F5, G5, A5의 주파수
for note in notes:
    play_tone(note, duration=500) # 각 음표를 500ms 동안 재생
