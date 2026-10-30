# -*- coding: utf-8 -*-
"""
OpenClaw GenPark Music Creator Client
Zero-dependency musical signal synthesizer, MIDI pitch converter, and Markov chord progression composer.
"""

import math
import random
from typing import Dict, List, Any, Optional

class OpenClawGenParkMusicCreator:
    """
    Synthesizes harmonic overtones, converts MIDI pitches with microtonal cents precision,
    and composes diatonic chord progressions using Markov transition matrices.
    """

    NOTE_NAMES = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]

    DIATONIC_CHORDS_MAJOR = {
        "I": ["C", "E", "G"],
        "ii": ["D", "F", "A"],
        "iii": ["E", "G", "B"],
        "IV": ["F", "A", "C"],
        "V": ["G", "B", "D"],
        "vi": ["A", "C", "E"],
        "vii*": ["B", "D", "F"]
    }

    # Transition probability matrix for functional diatonic harmony (Major)
    TRANSITIONS_MAJOR = {
        "I": {"I": 0.05, "ii": 0.15, "iii": 0.05, "IV": 0.30, "V": 0.30, "vi": 0.15},
        "ii": {"V": 0.65, "vii*": 0.15, "IV": 0.10, "I": 0.10},
        "iii": {"vi": 0.60, "IV": 0.25, "ii": 0.15},
        "IV": {"V": 0.45, "I": 0.25, "ii": 0.20, "vii*": 0.10},
        "V": {"I": 0.70, "vi": 0.20, "IV": 0.10},
        "vi": {"ii": 0.35, "IV": 0.35, "V": 0.20, "iii": 0.10},
        "vii*": {"I": 0.85, "iii": 0.15}
    }

    def synthesize_harmonic_overtones(
        self,
        fundamental_freq_hz: float,
        duration_ms: float = 1000.0,
        sample_rate_hz: int = 44100,
        harmonic_weights: Optional[List[float]] = None
    ) -> Dict[str, Any]:
        """
        Synthesizes harmonic overtone spectrum f_k = (k+1)*f_0 and computes RMS, peak, and spectral centroid.
        """
        if fundamental_freq_hz <= 0:
            raise ValueError("Fundamental frequency must be strictly positive.")
        if duration_ms <= 0:
            raise ValueError("Duration must be strictly positive.")

        weights = harmonic_weights or [1.0, 0.5, 0.25, 0.125, 0.0625]
        total_weight = sum(weights)
        norm_weights = [w / total_weight for w in weights]

        # Analyze overtones
        overtones = []
        for idx, w in enumerate(norm_weights):
            k = idx + 1
            freq = round(fundamental_freq_hz * k, 2)
            overtones.append({
                "harmonic_index": k,
                "frequency_hz": freq,
                "relative_weight": round(w, 4),
                "is_audible": freq < 20000.0
            })

        # Generate sample points (simulate discrete synthesis window of 256 samples)
        num_samples = min(256, int(sample_rate_hz * (duration_ms / 1000.0)))
        waveform_samples = []
        sum_sq = 0.0
        peak_amp = 0.0

        for n in range(num_samples):
            t = n / sample_rate_hz
            val = 0.0
            for idx, w in enumerate(norm_weights):
                k = idx + 1
                freq = fundamental_freq_hz * k
                val += w * math.sin(2.0 * math.pi * freq * t)
            
            abs_v = abs(val)
            if abs_v > peak_amp:
                peak_amp = abs_v
            sum_sq += val * val
            if n < 32:  # store sample slice
                waveform_samples.append(round(val, 4))

        rms_power = round(math.sqrt(sum_sq / max(1, num_samples)), 4)
        crest_factor = round(peak_amp / (rms_power + 1e-9), 3)

        # Spectral Centroid (f_centroid = sum(f_k * w_k) / sum(w_k))
        spectral_centroid_hz = round(sum( fundamental_freq_hz * (i + 1) * w for i, w in enumerate(norm_weights) ), 2)

        return {
            "fundamental_freq_hz": fundamental_freq_hz,
            "duration_ms": duration_ms,
            "sample_rate_hz": sample_rate_hz,
            "harmonic_count": len(overtones),
            "spectral_centroid_hz": spectral_centroid_hz,
            "rms_amplitude": rms_power,
            "peak_amplitude": round(peak_amp, 4),
            "crest_factor": crest_factor,
            "overtone_spectrum": overtones,
            "waveform_preview_32_samples": waveform_samples
        }

    def convert_midi_and_pitch_scale(
        self,
        midi_note_or_freq: float,
        is_midi_number: bool = True,
        a4_tuning_hz: float = 440.0
    ) -> Dict[str, Any]:
        """
        Converts between MIDI note number and acoustic frequency with microtonal cents precision.
        Formula: f = A4 * 2^((m - 69) / 12)
        """
        if is_midi_number:
            midi_num = midi_note_or_freq
            freq_hz = a4_tuning_hz * math.pow(2.0, (midi_num - 69.0) / 12.0)
        else:
            if midi_note_or_freq <= 0:
                raise ValueError("Frequency must be strictly positive.")
            freq_hz = midi_note_or_freq
            midi_num = 69.0 + 12.0 * math.log2(freq_hz / a4_tuning_hz)

        closest_midi = int(round(midi_num))
        cents_deviation = round(100.0 * (midi_num - closest_midi), 2)
        
        note_idx = closest_midi % 12
        octave = (closest_midi // 12) - 1
        note_name = f"{self.NOTE_NAMES[note_idx]}{octave}"

        # Standard 88-key piano key index (A0 = key 1, C8 = key 88)
        piano_key = closest_midi - 20
        is_standard_piano = 1 <= piano_key <= 88

        return {
            "input_val": midi_note_or_freq,
            "is_midi_input": is_midi_number,
            "frequency_hz": round(freq_hz, 3),
            "midi_note_number": round(midi_num, 3),
            "closest_note_name": note_name,
            "cents_deviation": cents_deviation,
            "piano_key_index": piano_key if is_standard_piano else None,
            "is_standard_piano_range": is_standard_piano,
            "a4_reference_hz": a4_tuning_hz
        }

    def generate_markov_chord_progression(
        self,
        seed_chord: str = "I",
        scale_mode: str = "major",
        length: int = 8,
        harmonic_rhythm: str = "4/4"
    ) -> Dict[str, Any]:
        """
        Generates a chord progression using functional diatonic Markov transition probabilities.
        """
        if length <= 0:
            raise ValueError("Progression length must be at least 1.")

        current = seed_chord if seed_chord in self.TRANSITIONS_MAJOR else "I"
        progression = []
        transitions = self.TRANSITIONS_MAJOR

        # Deterministic pseudo-random seed sequence based on input
        rng = random.Random(hash(f"{seed_chord}_{scale_mode}_{length}"))

        for step in range(length):
            chord_notes = self.DIATONIC_CHORDS_MAJOR.get(current, ["C", "E", "G"])
            progression.append({
                "bar": step + 1,
                "roman_numeral": current,
                "chord_symbol": f"{chord_notes[0]}maj" if current in ["I", "IV", "V"] else (f"{chord_notes[0]}dim" if current == "vii*" else f"{chord_notes[0]}min"),
                "notes": chord_notes,
                "harmonic_function": "Tonic" if current in ["I", "vi", "iii"] else ("Subdominant" if current in ["IV", "ii"] else "Dominant")
            })

            # Transition to next chord
            probs = transitions.get(current, {"I": 1.0})
            r = rng.random()
            cum = 0.0
            next_chord = "I"
            for cand, p in probs.items():
                cum += p
                if r <= cum:
                    next_chord = cand
                    break
            current = next_chord

        # Calculate harmonic tension curve (Dominant has highest tension 1.0, Subdominant 0.6, Tonic 0.2)
        tension_map = {"Tonic": 0.2, "Subdominant": 0.6, "Dominant": 1.0}
        tension_curve = [tension_map.get(c["harmonic_function"], 0.2) for c in progression]
        avg_tension = round(sum(tension_curve) / len(tension_curve), 3)

        return {
            "seed_chord": seed_chord,
            "scale_mode": scale_mode,
            "length_bars": length,
            "harmonic_rhythm": harmonic_rhythm,
            "average_tension": avg_tension,
            "cadence_concluded": progression[-1]["roman_numeral"] in ["I", "V"],
            "chords": progression
        }
