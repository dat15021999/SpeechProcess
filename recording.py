import sounddevice as sd
from scipy.io.wavfile import write

fs = 44100
second = 5

myrecording = sd.rec(int(second * fs), samplerate = fs, channels = 2)
sd.wait()
write('output', fs, myrecording)