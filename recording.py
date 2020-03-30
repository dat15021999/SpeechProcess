import tkinter as tk
import threading
import pyaudio
import wave
from os import walk
from nltk.tokenize import sent_tokenize


class Frame:
    chunk = 1024
    sample_format = pyaudio.paInt16
    channels = 2
    fs = 44100

    frames = []

    def __init__(self, master, topics):
        self.sentences = []
        self.current_index = -1
        self.is_recording = False

        self.record_button = tk.Button(main, text='record', command=self.start, width=10)
        self.record_button.pack()

        self.stop_button = tk.Button(main, text='stop', command=self.stop, width=10)
        self.stop_button.pack() 

        self.next_button = tk.Button(main, text='next', command=self.goNext, width=10)
        self.next_button.pack()
        
        self.prev_button = tk.Button(main, text='back', command=self.goPrev, width=10)
        self.prev_button.pack()

        self.lable = tk.Label(main, text='Sentences')
        self.lable.pack()

        self.text = tk.Text(main, height=10, width=250)
        self.text.pack()


        #Topic Option
        self.emo = tk.StringVar(main)
        self.emo.set('Topics')
        self.popupMenu = tk.OptionMenu(main, self.emo, *topics)
        self.emo.trace('w', self.getTopic)
        self.popupMenu.pack()

        

    def getTopic(self, *args):
        topic_name = self.emo.get()
        file_name = topic_name.lower() + '.txt'
        dir = 'Data/' + topic_name + '/' + file_name
        
        with open(dir, 'r') as f:
            text = f.read()
            self.sentences = sent_tokenize(text)

        dir = 'Data/' + topic_name + '/' + 'index.txt'

        with open(dir, 'w') as f:
            for i in range(len(self.sentences)):
                f.write(self.sentences[i] + '\n')
                f.write(str(i) + '.wav\n')
        self.current_index = -1

    def goNext(self):
        self.current_index += 1

        if self.current_index >= len(self.sentences):
            print('End of article. Choose other topic')

        self.text.delete('1.0', tk.END)
        self.text.insert(tk.END, self.sentences[self.current_index])
        print(self.sentences[self.current_index])

    def goPrev(self):
        self.current_index -= 1

        if self.current_index < 0:
            self.current_index = 0

        self.text.delete('1.0', tk.END)
        self.text.insert(tk.END, self.sentences[self.current_index])
        print(self.sentences[self.current_index])

    def start(self):
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(format=self.sample_format, channels=self.channels, rate=self.fs,
                                  frames_per_buffer=self.chunk, input=True)
        self.is_recording = True

        print('Recording')
        self.t = threading.Thread(target=self.record)
        self.t.start()

    def stop(self):
        self.is_recording = False
        print('recording complete')

        filename = 'Data/' + self.emo.get() + '/' + str(self.current_index) + '.wav'
        wf = wave.open(filename, 'wb')
        wf.setnchannels(self.channels)
        wf.setsampwidth(self.p.get_sample_size(self.sample_format))
        wf.setframerate(self.fs)
        wf.writeframes(b''.join(self.frames))
        wf.close()
        self.frames.clear()

    def record(self):
        while self.is_recording:
            data = self.stream.read(self.chunk)
            self.frames.append(data)


# Get list of topics
topics = {}
for (dirpath, dirnames, filenames) in walk('Data'):
    for dirname in dirnames:
        topics.update({dirname: dirname})
    break

main = tk.Tk()
main.title('Recording')
main.geometry('800x500')
frame = Frame(main, topics)
main.mainloop()