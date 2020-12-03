# Simple Flask Local Music Streaming App With Sockets  

A simple Flask app for streaming music using sockets. Practical work for the discipline of computer networks of the course systems for internet 2020.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

What things you need to install the software and how to install them

```
Python 3
Flask
PyAudio
```

### Installing

Installing dependencies 

```
pip install -r requirements.txt
```

Once all packages are downloaded and installed, configure the target server port and address in socket_helpers.py.
Run the files in the below sequence:

```
1 - server.py

2 - web_cliente.py
```

## Running the tests

The audio library is composed of songs in the .wav format. To add songs to library, just add them to the project's 'music' directory.

Open up your browser and visit
```
http://localhost:8080
```
