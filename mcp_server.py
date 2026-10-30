# -*- coding: utf-8 -*-
"""
OpenClaw GenPark Music Creator FastMCP Server
"""

import json
from typing import List, Optional
from mcp.server.fastmcp import FastMCP
from client import OpenClawGenParkMusicCreator

mcp = FastMCP("openclaw-genpark-music-creator")
creator = OpenClawGenParkMusicCreator()

@mcp.tool()
def synthesize_harmonic_overtones(
    fundamental_freq_hz: float,
    duration_ms: float = 1000.0,
    sample_rate_hz: int = 44100,
    harmonic_weights: Optional[List[float]] = None
) -> str:
    """
    Synthesizes harmonic overtone spectrum f_k = (k+1)*f_0 and computes RMS power and spectral centroid.
    """
    res = creator.synthesize_harmonic_overtones(fundamental_freq_hz, duration_ms, sample_rate_hz, harmonic_weights)
    return json.dumps(res, indent=2)

@mcp.tool()
def convert_midi_and_pitch_scale(
    midi_note_or_freq: float,
    is_midi_number: bool = True,
    a4_tuning_hz: float = 440.0
) -> str:
    """
    Converts between MIDI note number and acoustic frequency with microtonal cents precision.
    """
    res = creator.convert_midi_and_pitch_scale(midi_note_or_freq, is_midi_number, a4_tuning_hz)
    return json.dumps(res, indent=2)

@mcp.tool()
def generate_markov_chord_progression(
    seed_chord: str = "I",
    scale_mode: str = "major",
    length: int = 8,
    harmonic_rhythm: str = "4/4"
) -> str:
    """
    Generates a chord progression using functional diatonic Markov transition probabilities.
    """
    res = creator.generate_markov_chord_progression(seed_chord, scale_mode, length, harmonic_rhythm)
    return json.dumps(res, indent=2)

def main():
    print("Testing Music Creator:")
    print(generate_markov_chord_progression("I", "major", 4))

if __name__ == "__main__":
    main()
