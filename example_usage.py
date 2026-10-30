# -*- coding: utf-8 -*-
from client import OpenClawGenParkMusicCreator

creator = OpenClawGenParkMusicCreator()

# 1. Harmonic Overtones Synthesis
overtones = creator.synthesize_harmonic_overtones(fundamental_freq_hz=440.0, duration_ms=500.0)
print(f"Overtone Synthesis: Fundamental={overtones['fundamental_freq_hz']}Hz, Centroid={overtones['spectral_centroid_hz']}Hz, RMS={overtones['rms_amplitude']}")

# 2. MIDI & Pitch Scale Conversion
pitch = creator.convert_midi_and_pitch_scale(midi_note_or_freq=60.0, is_midi_number=True)
print()
print(f"MIDI 60 Conversion: Note={pitch['closest_note_name']}, Freq={pitch['frequency_hz']}Hz, PianoKey={pitch['piano_key_index']}")

freq_pitch = creator.convert_midi_and_pitch_scale(midi_note_or_freq=523.25, is_midi_number=False)
print(f"Freq 523.25Hz Conversion: ClosestNote={freq_pitch['closest_note_name']}, CentsDeviation={freq_pitch['cents_deviation']}")

# 3. Markov Chord Progression
prog = creator.generate_markov_chord_progression(seed_chord="I", length=6)
print()
print(f"Markov Chord Progression (Avg Tension: {prog['average_tension']}):")
for bar in prog["chords"]:
    print(f"  Bar {bar['bar']}: {bar['roman_numeral']} ({bar['chord_symbol']}) - {bar['harmonic_function']} [{', '.join(bar['notes'])}]")
