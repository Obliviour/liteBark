#! /bin/bash

python wav_trigger_inference.py \
--graph=/home/pi/tensorflowAudio/speech_commands/conv_actions_frozen.pb \
--labels=/home/pi/tensorflowAudio/speech_commands/conv_actions_labels.txt \
--wav=./file.wav 
