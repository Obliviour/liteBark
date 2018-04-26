# Copyright 2017 The TensorFlow Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================
r"""Runs a trained audio graph against a WAVE file and reports the results.

The model, labels and .wav file specified in the arguments will be loaded, and
then the predictions from running the model against the audio data will be
printed to the console. This is a useful script for sanity checking trained
models, and as an example of how to use an audio model from Python.

Here's an example of running it:

python tensorflow/examples/speech_commands/label_wav.py \
--graph=/tmp/my_frozen_graph.pb \
--labels=/tmp/speech_commands_train/conv_labels.txt \
--wav=/tmp/speech_dataset/left/a5d485dc_nohash_0.wav

"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import argparse
import sys

import os
os.environ['TF_CPP_MIN_LOG_LEVEL']='2'

import tensorflow as tf
import pyaudio
import wave
import math
import audioop

from threading import Thread
import cv2
import time
import numpy as np

# pylint: disable=unused-import
from tensorflow.contrib.framework.python.ops import audio_ops as contrib_audio
# pylint: enable=unused-import

graph_path = '/home/pi/ECE4180/tensorflowAudio/speech_commands/conv_actions_frozen.pb'
labels_path = '/home/pi/ECE4180/tensorflowAudio/speech_commands/conv_actions_labels.txt'
wav_path = './file.wav'
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
CHUNK = 1024 
RECORD_SECONDS = 1
WAVE_OUTPUT_FILENAME = "file.wav"
INTENSITY=150
num_samples=50


class Microphone():

    def __init__(self):
        self.keyword = None
        self.stopped = False

    def startRecording(self):
        #Thread(target=self.label_wav, args=(wav_path, labels_path, graph_path, 'wav_data:0','labels_softmax:0', 1)).start()
        #return self
        return self.label_wav(wav_path, labels_path, graph_path, 'wav_data:0','labels_softmax:0', 1)
        

    def read(self):
        return self.keyword 

    def close(self):
        self.stopped = True

    def load_graph(self, filename):
      """Unpersists graph from file as default graph."""
      with tf.gfile.FastGFile(filename, 'rb') as f:
        graph_def = tf.GraphDef()
        graph_def.ParseFromString(f.read())
        tf.import_graph_def(graph_def, name='')


    def load_labels(self, filename):
      """Read in labels, one label per line."""
      return [line.rstrip() for line in tf.gfile.GFile(filename)]


    def run_graph(self, wav_data, labels, input_layer_name, output_layer_name,
                  num_top_predictions):
      """Runs the audio data through the graph and prints predictions."""
      with tf.Session() as sess:
        # Feed the audio data as input to the graph.
        #   predictions  will contain a two-dimensional array, where one
        #   dimension represents the input image count, and the other has
        #   predictions per class
        softmax_tensor = sess.graph.get_tensor_by_name(output_layer_name)
        predictions, = sess.run(softmax_tensor, {input_layer_name: wav_data})

        # Sort to show labels in order of confidence
        top_k = predictions.argsort()[-num_top_predictions:][::-1]
        
        for node_id in top_k:
          human_string = labels[node_id]
          score = predictions[node_id]
          print('%s (score = %.5f)' % (human_string, score))

        
        self.keyword = labels[np.argmax(predictions)]
        print(self.keyword)

        return 0


    def label_wav(self, wav, labels, graph, input_name, output_name, how_many_labels):
      """Loads the model and labels, and runs the inference to print predictions."""
      if not wav or not tf.gfile.Exists(wav):
        tf.logging.fatal('Audio file does not exist %s', wav)

      if not labels or not tf.gfile.Exists(labels):
        tf.logging.fatal('Labels file does not exist %s', labels)

      if not graph or not tf.gfile.Exists(graph):
        tf.logging.fatal('Graph file does not exist %s', graph)

      labels_list = self.load_labels(labels)

      # load graph, which is stored in the default session
      self.load_graph(graph)


      p = pyaudio.PyAudio()
      # start Recording
      prev_data0=[]
      prev_data1=[]
      prev_data2=[]
      prev_data3=[]
      prev_data4=[]
      while True:
        
        stream = p.open(format=FORMAT, channels=CHANNELS,rate=RATE, input=True,frames_per_buffer=CHUNK)
        cur_data = stream.read(CHUNK) # exception_on_overflow=False)
        values = [math.sqrt(abs(audioop.avg(cur_data, 4)))
                  for x in range(num_samples)]
        values = sorted(values, reverse=True)
        r = sum(values[:int(num_samples * 0.2)]) / int(num_samples * 0.2)
        #print " Finished "
        if (r > INTENSITY):
          print (' recording... Average audio intensity is r', r)
          frames = []
          frames.append(prev_data0)
          frames.append(prev_data1)
          frames.append(prev_data2)
          frames.append(prev_data3)
          frames.append(prev_data4)
          frames.append(cur_data)
          for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
            data = stream.read(CHUNK) # exception_on_overflow=False)
            frames.append(data)
          print ('finished recording')
          waveFile = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
          waveFile.setnchannels(CHANNELS)
          waveFile.setsampwidth(p.get_sample_size(FORMAT))
          waveFile.setframerate(RATE)
          #if type(frames) is str:
          try:
            waveFile.writeframes(b''.join(frames))
          except TypeError:
            print("Something went wrong...")
            return False  
          waveFile.close()
          with open(wav, 'rb') as wav_file:
            wav_data = wav_file.read()
          self.run_graph(wav_data, labels_list, input_name, output_name, how_many_labels)
          return True
        prev_data0=prev_data1
        prev_data1=prev_data2
        prev_data2=prev_data3
        prev_data3=prev_data4
        prev_data4=cur_data
        stream.stop_stream()
        stream.close()

        if self.stopped:
            p.terminate()
            return
      p.terminate()


def main(_):
  """Entry point for script, converts flags to arguments."""
  
  mic = Microphone().startRecording()


if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument(
      '--wav', type=str, default='', help='Audio file to be identified.')
  parser.add_argument(
      '--graph', type=str, default='', help='Model to use for identification.')
  parser.add_argument(
      '--labels', type=str, default='', help='Path to file containing labels.')
  parser.add_argument(
      '--input_name',
      type=str,
      default='wav_data:0',
      help='Name of WAVE data input node in model.')
  parser.add_argument(
      '--output_name',
      type=str,
      default='labels_softmax:0',
      help='Name of node outputting a prediction in the model.')
  parser.add_argument(
      '--how_many_labels',
      type=int,
      default=1,
      help='Number of results to show.')
  #main()
  #FLAGS, unparsed = parser.parse_known_args()
  tf.app.run(main=main) #argv=[sys.argv[0]] + unparsed)
