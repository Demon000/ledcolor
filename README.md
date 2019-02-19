This project allows Rival mouses to transition between multiple colors of your choice.
Also, morse, and sound-based lighting.

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
