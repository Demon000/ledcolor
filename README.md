This project allows animating leds based on your choice of colors and timing,
or the volume of the sound currently playing.

# Dependencies

Install `portaudio` manually or from your distro's package repository.

Install the dependencies using:
```
pip install -r requirements.txt
```

# Running

Run the program using:
```
./rival.py
```

# Usage

Details about usage are available using:
```
./rival --help
```

To get the sound syncing feature working, start the program using the `-s`
option, then open `pavucontrol`, press on the `Recording` tab, and switch
captured device to your output's monitor.

Alternatively, you can install `pulseaudio-alsa` and then follow the steps
(here)[https://wiki.archlinux.org/index.php/PulseAudio/Examples#ALSA_monitor_source],
and then specify the `-i` option with the value of your defined source, eg. `pulse_monitor`.
