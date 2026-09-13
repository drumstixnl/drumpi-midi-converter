# drumpi-midi-converter
A Python script that converts Drumpi midi recordings into usable midi files, ready to import into your DAW.

## Why
[Drumpi](https://www.drumpi.com) is a great piece of software that turns your e-drum into a great sounding drumkit.  
It can record your performance both in audio as well as in midi. There is an issue with the midi file though. And that caused issues with my DAW of choice (Ableton Live).  

### Issue 1
It seems that in the recorded midi file there is an orphan note-off (a note-off event with no note-on event). That somehow messes up the import functionality of Ableton Live.

### Issue 2
As Drumpi doesn't have a metronome, it doesn't know at what BPM you're recording. A midi files doesn't have to have a BPM set. It can use SMPTE and that's what Drumpi does.  
But DAWs do use a set tempo. Also, the SMPTE setting of Drumpi seems not to be a standard. So again, this messes up the imported clip (usually resulting in a stretched clip).

## Fix
This Python scripts tries to fix these issues. Download your midi recording from Drumpi, run it through this script and import the resulting midi file. The script assumes that Drumpi uses 44100 ticks per second. Which comes close to my measurements. It also makes sense because 44100Hz is the samplerate of Drumpi. I don't know if this value is actually correct. But it works.

## Installation
This script requires python3 and the mido package.  

Install the required Python package if you haven't already:
```bash
python3 -m pip install mido
```

Download this script and run it in the terminal (macOS, linux) or in command prompt (Windows).

## Usage
```bash
python3 convert_for_ableton.py <input.mid> <output.mid> [bpm]
```

### Example 1
In this example the bpm is not given. So 120 bpm is assumed as that is the standard that most DAWs use.  
```bash
python3 drumpi_converter.py drumpi_recording.mid daw_friendly_recording.mid
```
### Example 2
In this example the bpm is given, for example when the recording was made on a click with this tempo.  

```bash
python3 drumpi_converter.py drumpi_recording_to_click.mid daw_friendly_recording_with_tempo.mid 132
```

### note that I'm not affiliated with Drumpi
