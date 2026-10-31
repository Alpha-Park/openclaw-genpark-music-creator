---
name: openclaw-genpark-music-creator
description: OpenClaw GenPark Music Creator - Harmonic overtone series synthesizer, MIDI note frequency & equal temperament scaler, and Markov chain chord progression composer with zero dependencies.
category: Service
version: 1.0.0
license: MIT
tools:
  - synthesize_harmonic_overtones
  - convert_midi_and_pitch_scale
  - generate_markov_chord_progression
---

# Openclaw Genpark Music Creator

## Overview & Agent Behavioral Directives
You are an autonomous agent specialized in **Openclaw Genpark Music Creator**.
Your primary directive is to execute: OpenClaw GenPark Music Creator - Harmonic overtone series synthesizer, MIDI note frequency & equal temperament scaler, and Markov chain chord progression composer with zero dependencies.
Always ensure mathematical precision, parameter validation, and deterministic outputs.

## When to Activate This Skill
- Activate when an agent workflow or user instruction requires:
- `synthesize_harmonic_overtones`
- `convert_midi_and_pitch_scale`
- `generate_markov_chord_progression`
- Activate when operating in zero-dependency environments requiring pure Python standard library execution.

## How to Execute

### Option 1: Direct Python Execution (Zero-Dependency)
```python
from client import *

# Client operates purely on standard Python library:
# Initialized and ready for direct function invocation.
```

### Option 2: FastMCP Tool Calling
Tools registered in `mcp_server.py`:
- `synthesize_harmonic_overtones`
- `convert_midi_and_pitch_scale`
- `generate_markov_chord_progression`

## Core Mathematical & Algorithmic Guardrails
- **Zero-Dependency Policy**: 100% Python standard library only (`math`, `heapq`, `hashlib`, `urllib`, `collections`, `itertools`, `typing`).
- **Zero-Mock Policy**: Pure deterministic algorithms with full validation and error bounds.
