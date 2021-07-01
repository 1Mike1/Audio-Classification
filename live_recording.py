from datetime import datetime
import time
import pyaudio
import wave

class Record:
    
    def __init__(self, label):
        self.chunk = 1024
        self.sample_format = pyaudio.paInt16
        self.channels = 1
        self.fs = 8000
        self.seconds = 1
        self.label = label
    
    def recording(self):
        frames = list()
        filename = f"{self.label}_{self.random_id()}.wav"
        p = pyaudio.PyAudio()
        print('Recording')
        stream = p.open(format=self.sample_format,channels=self.channels,rate=self.fs,frames_per_buffer=self.chunk,input=True)
        for i in range(0, int(self.fs / self.chunk * self.seconds)):
            data = stream.read(self.chunk)
            frames.append(data)
    
        stream.stop_stream()
        stream.close()
        p.terminate()
        print('Finished recording')

        wf = wave.open(filename, 'wb')
        wf.setnchannels(self.channels)
        wf.setsampwidth(p.get_sample_size(self.sample_format))
        wf.setframerate(self.fs)
        wf.writeframes(b''.join(frames))
        wf.close()
        print(filename)
        return filename, frames, stream
      
    def random_id(self):
        dt = datetime.utcnow()
        stamp = time.mktime(dt.timetuple()) + dt.microsecond / 1e0
        today = time.strftime("%d%m%y")
        stamp_id = str(today) + str(stamp).split(".")[0]
        return stamp_id
