This project allows animating leds based on your choice of colors and timing,
or the volume of the sound currently playing.

# Setup

Create a virtual environment:
```
python3 -m venv venv
```

Use the virtual environment:
```
. venv/bin/activate
```

Install the dependencies using:
```
pip install -r requirements.txt
```

# Running

Use the virtual environment:
```
. venv/bin/activate
```

Start the backend using:
```
./ledcolor_backend.py
```

Configure the backend using:
```
./ledcolor.py
```

# Usage

Details about usage are available using:
```
./ledcolor --help
```

To get the sound syncing feature working, the backend must have access to the pulseaudio
socket. The easiest way to provide this ability is to run the backend using the same
user as the pulseuadio server.

On some setups (for example, when using, KDE) the pulseaudio server is started as the current user, so you
must start the backend _without_ using `sudo`.
You will have to chown the brightness files of the LEDs you want to let the backend control.
```
sudo chown <username> /sys/class/leds/<name>/brightness
```

On other setups, the pulseuadio server is started in system mode, in which case you need
to start the backend using `sudo` and configure it using `sudo` too, because of the socket ownership.
