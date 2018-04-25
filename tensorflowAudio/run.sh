#! /bin/bash

python wav_trigger_inference.py \
--graph=./speech_commands/conv_actions_frozen.pb \
--labels=./speech_commands/conv_actions_labels.txt \
--wav=./file.wav 
