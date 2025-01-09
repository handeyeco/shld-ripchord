# SHLD MIDI file to Ripchord Preset

Just a basic Python script for converting the [SHLD MIDI Chord Pack](https://github.com/ldrolez/free-midi-chords) into [Ripchord](https://trackbout.com/) presets.

[If you just want the presets, they're on my blog.](https://handeyeco.github.io/tech-blog/shld-ripchord/)

## Usage

You need Python and Pip on your computer.

> [!CAUTION]
> The script clears `./output` before each run.

1. `python3 -m venv env`
2. `source env/bin/activate`
3. `pip install -r ./requirements.txt`
4. Put the unzipped SHLD chord progression folder into `./input`
5. (Optional) Remove the rhythmic variation folders: `basic4`, `alt4`, and `hiphop`
6. `python3 main.py`
7. Ripchord presets will go into `./output`
