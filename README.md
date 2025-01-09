# SHLD MIDI file to Ripchord Preset

Just a basic Python script for converting [SHLD MIDI Chord Pack](https://github.com/ldrolez/free-midi-chords) into [Ripchord](https://trackbout.com/) presets (so I could use them with my [Norns-Ripchord](https://github.com/handeyeco/norns-ripchord) script for [Norns](https://monome.org/docs/norns/)).

---

## Usage

You need Python and Pip on your computer.

> [!CAUTION]
> The script clears `./output` before each run.

1. `source env/bin/activate`
2. `pip install -r ./requirements.txt`
3. Put the unzipped SHLD chord progression folder into `./input`
4. (Optional) Remove the rhythmic variation folders: `basic4`, `alt4`, and `hiphop`
5. `python3 main.py`
6. Ripchord presets will go into `./output`