
import socket
import threading
from PyQt5.QtCore import QThread
import pyaudio

class AudioClient(QThread):

    def __init__(self, IP, PORT):

        self.bConnect = False
        self.aConnect = False

        super().__init__()
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.target_ip = IP
        print("\n AUDIO SERVER IP : ", IP)
        self.target_port = PORT
        print("\n AUDIO SERVER PORT : ", PORT)
        while 1:
            try:
                self.s.connect((self.target_ip, self.target_port))

            except Exception as e:
                print("Couldn't connect to server : ", e)
                break


        chunk_size = 1024 # 512
        audio_format = pyaudio.paInt16
        channels = 1
        rate = 20000

        # initialise microphone recording
        self.p = pyaudio.PyAudio()
        self.playing_stream = self.p.open(format=audio_format, channels=channels, rate=rate, output=True, frames_per_buffer=chunk_size)
        self.recording_stream = self.p.open(format=audio_format, channels=channels, rate=rate, input=True, frames_per_buffer=chunk_size)
        
        print("Connected to Server")

    def __del__(self):
        self.wait()
        self.stop()

    def stop(self):
        print('\n Audio Client socket stop method Called')
        self.aConnect = False

        self.s.close()
        self.p.close()

        self.playing_stream.close()
        self.recording_stream.close()    
        
    def start(self):
        # start threads
        while self.aConnect:

            self.receive_thread = threading.Thread(target=self.receive_server_data, args=())
            self.receive_thread.start()

            self.sending_thread = threading.Thread(target=self.send_data_to_server, args=())
            self.sending_thread.start()
        

    def receive_server_data(self):
        while True:
            try:
                data = self.s.recv(1024)
                self.playing_stream.write(data)
            except:
                pass


    def send_data_to_server(self):
        while True:
            try:
                data = self.recording_stream.read(1024)
                self.s.sendall(data)
            except:
                pass