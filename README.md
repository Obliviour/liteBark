# liteBark
A deep look into the performance of the Raspberry Pi for parallel processing of speech recognition and object detection

## Authors
Victor Barr
Derin Ozturk


### Contents

* [Overview](#overview)
* [Running Code From Pi](#runningcode)
* [Purpose](#purpose)
* [Software Used and Parts List](#software-used-and-parts-list)
* [Results](#results)
* [Future Work](#future-work)
* [Installation of Tensorflow](#installing-tensorflow)
* [Tensorflow for Audio Recognition](#creating-tensorflow-based-audio-recognition)
* [Installing OpenCV on Raspberry Pi 3](#installing-opencv-on-raspberry-pi-3)
* [Installing Other Libraries Used for Human Detection](#installing-other-libraries)


## Overview
Main goals: 
Human Tracking – Detect the location of humans and follow/turn towards them
Speech Enabled – Voice enabled commands to turn, go forward, and stop
Light Tracking – Follow highest intensity of light 

## Running Code
Installation of software on pi was done in python virtual environments located in 
    
    /home/pi/.virtualenvs/cv
    
Add software environments to path by doing the following: 

    cd ~
    source .profile
    workon cv
    
Note Tensorflow was accidently not placed in the virtual environment. This virtual environment
just adds the software packages to the root directory.

Run Demo through the following:
    
    cd /home/pi/ECE4180
    python robot.py

## Purpose: 
Understand the performance capabilities of the Raspberry Pi for machine learning applications
Can it train models? Build Tensorflow? Run multiple threads?
Power Consumption? Overheating?

## Software Used and Parts List
#### Software Used
    Tensorflow 1.7
    
    60,000+ .wav file model
    “Go”, “Stop”, “Left”, “Right”, “Yes”, “No”, “Up”, “Down”
    OpenCV
    Python-based Code

#### Hardware Used
    Raspberry Pi 3b+
    Pi Camera v2
    Motor Bridge
    Robot Frame
    Corsair Void Headset


## Results

#### Speech Recognition:
Detects speech of multiple keywords
Can rotate, and actuate motors based on these keywords
#### Object Detection
Can detect intensities of light from camera
Detect human objects and actuate motors for robot to follow human object
#### Problems
Power surge problems with current output of battery
Multithread to combine speech recognition and object detection is too performance heavy

## Future Work


#### Improvements
Manipulate threads to improve voice recognition and object detection in combined interface
Look into better power options for the Raspberry Pi
Add additional wheel to front of the robot
3D print pi mount, more solid wires
No Ethernet Cable (fully headless)

## Installing Tensorflow

Below is taking from the following github readme by samjabrahams. A wonderful guide on getting tensorflow installed.
https://github.com/samjabrahams/tensorflow-on-raspberry-pi. We need tensorflow 1.7 instead of 1.1. Be sure to get the correct file for the built tensorflow package.

* [Installing from pip (easy)](#installing-from-pip)
* [Building from source (hard)](#building-from-source)
* [Docker image](#docker-image)


## Installing from Pip

This is the easiest way to get TensorFlow onto your Raspberry Pi 3. Note that currently, the pre-built binary is targeted for Raspberry Pi 3 running Raspbian 8.0 ("Jessie"), so this may or may not work for you. The specific OS release is the following:

```
Raspbian 8.0 "Jessie"
Release: March 2, 2017
Installed via NOOBS 2.3
```

First, install the dependencies for TensorFlow:

```shell
sudo apt-get update

# For Python 2.7
sudo apt-get install python-pip python-dev


Next, download the wheel file from this repository and install it:

```shell
# For Python 2.7
wget https://github.com/samjabrahams/tensorflow-on-raspberry-pi/releases/download/v1.1.0/tensorflow-1.1.0-cp27-none-linux_armv7l.whl
sudo pip install tensorflow-1.1.0-cp27-none-linux_armv7l.whl

# For Python 3.4
wget https://github.com/samjabrahams/tensorflow-on-raspberry-pi/releases/download/v1.1.0/tensorflow-1.1.0-cp34-cp34m-linux_armv7l.whl
sudo pip3 install tensorflow-1.1.0-cp34-cp34m-linux_armv7l.whl
```

Finally, we need to reinstall the `mock` library to keep it from throwing an error when we import TensorFlow:

```shell
# For Python 2.7
sudo pip uninstall mock
sudo pip install mock

# For Python 3.3+
sudo pip3 uninstall mock
sudo pip3 install mock
```

And that should be it!

### Docker image

Instructions on setting up a Docker image to run on Raspberry Pi are being maintained by @romilly [here](https://github.com/romilly/rpi-docker-tensorflow), and a pre-built image is hosted on DockerHub [here](https://hub.docker.com/r/romilly/rpi-docker-tensorflow/). Woot!

### Troubleshooting

_This section will attempt to maintain a list of remedies for problems that may occur while installing from `pip`_

#### "tensorflow-1.1.0-cp27-none-linux_armv7l.whl is not a supported wheel on this platform."

This wheel was built with Python 2.7, and can't be installed with a version of `pip` that uses Python 3. If you get the above message, try running the following command instead:

```
sudo pip2 install tensorflow-1.1.0-cp27-none-linux_armv7l.whl
```

Vice-versa for trying to install the Python 3 wheel. If you get the error "tensorflow-1.1.0-cp34-cp34m-any.whl is not a supported wheel on this platform.", try this command:

```
sudo pip3 install tensorflow-1.1.0-cp34-cp34m-linux_armv7l.whl
```

**Note: the provided binaries are for Python 2.7 and 3.4 _only_. If you've installed Python 3.5/3.6 from source on your machine, you'll need to either explicitly install these wheels for 3.4, or you'll need to build TensorFlow [from source](GUIDE.md). Once there's an officially supported installation of Python 3.5+, this repo will start including wheels for those versions.**



## Creating Tensorflow based Audio Recognition

### Building a model:
Following the link below to understand how to create a model and labels from wav file data
https://www.tensorflow.org/versions/master/tutorials/audio_recognition

### Getting Audio File using PyAudio
We want to stream audio files from an incoming wav file. The tutorial below explains how to do that

Tutorial 1: http://www.kiranjose.in/blogs/speech-detection-with-tensorflow-1-4-on-raspberry-pi-3-part-1-getting-audio-file-using-pyaudio/ 

### Streaming Audio File based on Intensity of sound from microphone
Tutorial 2: http://www.kiranjose.in/blogs/speech-detection-with-tensorflow-1-4-on-raspberry-pi-3-part-2-live-audio-inferencing-using-pyaudio/

### Github code for the above two tutorials
Github code: https://github.com/kiranjose/python-tensorflow-speech-recognition

## Installing OpenCV on Raspberry Pi 3
To install OpenCV from source onto the Raspbian Pi 3 on Raspbian use follow the steps found here: https://www.pyimagesearch.com/2016/04/18/install-guide-raspberry-pi-3-raspbian-jessie-opencv-3/. This tutorial also goes over using virtual environments in python which we highly recommend.

## Installing Other Libraries Used for Human Detection
To use our human detection methods, you must install the imutils package using pip. To do this:
``` shell
pip install imutils
```
