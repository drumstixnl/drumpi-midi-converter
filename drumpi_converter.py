import sys
from mido import MidiFile, MidiTrack, MetaMessage

# --------------------------------------------------
# Command line arguments
# --------------------------------------------------

if len(sys.argv) < 3:
    print("Usage:")
    print("  python3 drumpi_converter.py input.mid output.mid [bpm]")
    sys.exit(1)

INPUT_FILE = sys.argv[1]
OUTPUT_FILE = sys.argv[2]

BPM = int(sys.argv[3]) if len(sys.argv) >= 4 else 120

# --------------------------------------------------
# Constants
# --------------------------------------------------

DRUMPI_UNITS_PER_SECOND = 44100

PPQN = 480

TARGET_TICKS_PER_SECOND = (
    PPQN * BPM / 60
)

SCALE = (
    TARGET_TICKS_PER_SECOND
    / DRUMPI_UNITS_PER_SECOND
)

TEMPO_US_PER_QUARTER = int(
    60000000 / BPM
)

# --------------------------------------------------
# Load MIDI
# --------------------------------------------------

mid = MidiFile(INPUT_FILE)

new_mid = MidiFile(
    type=1,
    ticks_per_beat=PPQN
)

# --------------------------------------------------
# Tempo track
# --------------------------------------------------

tempo_track = MidiTrack()

tempo_track.append(
    MetaMessage(
        "set_tempo",
        tempo=TEMPO_US_PER_QUARTER,
        time=0
    )
)

tempo_track.append(
    MetaMessage(
        "end_of_track",
        time=0
    )
)

new_mid.tracks.append(tempo_track)

# --------------------------------------------------
# Convert event track(s)
# --------------------------------------------------

for old_track in mid.tracks:

    new_track = MidiTrack()

    active_notes = set()

    for msg in old_track:

        # Fix orphan note-offs
        if hasattr(msg, "note"):

            key = (
                getattr(msg, "channel", 0),
                msg.note
            )

            if msg.type == "note_on" and msg.velocity > 0:

                active_notes.add(key)

            elif msg.type == "note_off" or (
                msg.type == "note_on"
                and msg.velocity == 0
            ):

                if key not in active_notes:
                    # Skip orphan note-off
                    continue

                active_notes.remove(key)

        new_track.append(
            msg.copy(
                time=max(
                    0,
                    round(msg.time * SCALE)
                )
            )
        )

    new_mid.tracks.append(new_track)

# --------------------------------------------------
# Save
# --------------------------------------------------

new_mid.save(OUTPUT_FILE)

print()
print("Conversion complete")
print("-------------------")
print("Input file :", INPUT_FILE)
print("Output file:", OUTPUT_FILE)
print("BPM        :", BPM)
print("PPQN       :", PPQN)
#print("Scale      :", SCALE)
print()