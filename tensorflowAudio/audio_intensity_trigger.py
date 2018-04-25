import pyaudio
import wave
import math
import audioop
 
p = pyaudio.PyAudio() 
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
CHUNK = 512 
RECORD_SECONDS = 1
WAVE_OUTPUT_FILENAME = "file.wav"
INTENSITY=11000
 
def audio_int(num_samples=50):
    """ Gets average audio intensity of your mic sound. You can use it to get
        average intensities while you're talking and/or silent. The average
        is the avg of the 20% largest intensities recorded.
    """

    print ('Getting intensity values from mic.')
    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)
    while True:
      cur_data = stream.read(CHUNK)
      values = [math.sqrt(abs(audioop.avg(cur_data, 4)))
                for x in range(num_samples)]
      values = sorted(values, reverse=True)
      r = sum(values[:int(num_samples * 0.2)]) / int(num_samples * 0.2)
      #print " Finished "
      if (r > INTENSITY):
        print (' Average audio intensity is r', r)

    stream.close()
    p.terminate()
    return r


if(__name__ == '__main__'):
    audio_int()  # To measure your  mic levels





 
