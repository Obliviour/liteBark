# liteBark
A deep look into the performance of the Raspberry Pi for parallel processing of speech recognition and object detection


### Contents

* [Installing from pip (easy)](#Overview)
* [Building from source (hard)](#Purpose)
* [Docker image](#Software Used and Parts List)
* [Credits](#Results)
* [License](#Future Work)


## Overview
Main goals: 
Human Tracking – Detect the location of humans and follow/turn towards them
Speech Enabled – Voice enabled commands to turn, go forward, and stop
Light Tracking – Follow highest intensity of light 

## Purpose: 
Understand the performance capabilities of the Raspberry Pi for machine learning applications
Can it train models? Build Tensorflow? Run multiple threads?
Power Consumption? Overheating?

## Software Used and Parts List
#### Software Used
    Tensorflow 
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


### Installing Tensorflow:

* [Installing from pip (easy)](#installing-from-pip)
* [Building from source (hard)](#building-from-source)
* [Docker image](#docker-image)
* [Credits](#credits)
* [License](#license)

## Installing from Pip
**Note: These are unofficial binaries (though built from the minimally modified official source), and thus there is no expectation of support from the TensorFlow team. Please don't create issues for these files in the official TensorFlow repository.**

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

# For Python 3.3+
sudo apt-get install python3-pip python3-dev
```

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

## Building from Source

[_Step-by-step guide_](GUIDE.md)

If you aren't able to make the wheel file from the previous section work, you may need to build from source. Additionally, if you want to use features that have not been included in an official release, such as the [initial distributed runtime](https://github.com/tensorflow/tensorflow/tree/master/tensorflow/core/distributed_runtime), you'll have to build from source. Don't worry, as we've figured out most of the quirks of getting it right. The guide will be updated as needed to be as correct as possible.

See the [step-by-step guide here](GUIDE.md). **Warning: it takes a while.**

## Non-Raspberry Pi Model 3 builds

There are numerous single-board computers available on the market, but binaries and build instructions aren't necessarily compatible with what's available in this repository. This is a list of resources to help those with non-RPi3 (or RPi 2) computers get up and running:

* ODROID
    * [Issue thread for ODROID](https://github.com/samjabrahams/tensorflow-on-raspberry-pi/issues/41)
		* [NeoTitans guide to building on ODROID C2](https://www.neotitans.net/install-tensorflow-on-odroid-c2.html)

## Credits

While the final pieces of grunt work were done primarily by myself and @petewarden, this effort has been going on for almost as long as TensorFlow has been open-source, and involves work that spans multiple months in separate codebases. This is an incomprehensive list of people and their work I ran across while working on this.

The majority of the source-building guide is a modified version of [these instructions for compiling TensorFlow on a Jetson TK1](http://cudamusing.blogspot.com/2015/11/building-tensorflow-for-jetson-tk1.html). Massimiliano, you are the real MVP. _Note: the TK1 guide was [updated on June 17, 2016](http://cudamusing.blogspot.com/2016/06/tensorflow-08-on-jetson-tk1.html)_

@vmayoral put a huge amount of time and effort trying to put together the pieces to build TensorFlow, and was the first to get something close to a working binary.

A bunch of awesome Googlers working in both the TensorFlow and Bazel repositories helped make this possible. In no particular order: @vrv, @damienmg, @petewarden, @danbri, @ulfjack, @girving, and @nlothian

_Issue threads of interest:_

* [Initial issue for building Bazel on ARMv7l](https://github.com/bazelbuild/bazel/issues/606)
* [First thread about running TensorFlow on RPi](https://github.com/tensorflow/tensorflow/issues/254)
* [Parallel thread on building TensorFlow on ARMv7l](https://github.com/tensorflow/tensorflow/issues/445)
	* This is where the most recent conversation is located

## License

Subdirectories contained within the `third_party` directory each contain relevant licenses for the code and software within those subdirectories.

The file TENSORFLOW_LICENSE applies to the binaries distributed in the [releases.](https://github.com/samjabrahams/tensorflow-on-raspberry-pi/releases)

The file LICENSE applies to other files in this repository. I want to stress that a majority of the lines of code found in the guide of this repository was created by others. If any of those original authors want more prominent attribution, please contact me and we can figure out how to make it acceptable.
