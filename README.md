# Monteverdi's Madrigals - A Statistical Analysis

This repository contains a computational analysis of Claudio Monteverdi’s nine books of madrigals. The project tracks the shift from the Renaissance polyphonic tradition (**Prima Pratica**) to the early Baroque emphasis on monody and harmonic support (**Seconda Pratica**).

## Data Source
The musical scores used in this analysis were extracted and cleaned from the **Choral Public Domain Library**.

> Choral Public Domain Library, “Claudio Monteverdi,” ChoralWiki, 2022. [Online]. Available: [https://www.cpdl.org/wiki/index.php/Claudio_Monteverdi](https://www.cpdl.org/wiki/index.php/Claudio_Monteverdi)

## Methodology

The analysis is built on a custom heuristic framework that processes MusicXML/MXL files to extract lyrical and musicological data.

### 1. Textual Reconstruction & Dissonance Mapping
Because MusicXML fragments lyrics into syllables, the project uses a reconstruction engine to map vertical harmonic events to full words.
* `build_note_to_word_map()`: Iterates through vocal parts to reconstruct full Italian words (e.g., "A-ma-ril-li") and maps every note object to its parent word.
* `analyze_dissonant_words()`: Identifies vertical chords with 3+ unique pitch classes. If the chord is mathematically dissonant, it records the specific word being sung, allowing us to visualize Monteverdi's "dissonance vocabulary" across different books.

### 2. The Sprezzatura & Concitato Heuristic
We formalize the elusive concept of *Sprezzatura* (expressive rhythmic freedom) and *Stile Concitato* (the "excited style") using a weighted scoring system (0–10 points) per measure:

* **Basso Support (+2 pts):** Identifies measures where the bass acts as a harmonic anchor (pedal notes/long durations $\ge$ 2.0).
* **Stile Concitato (+3 pts):** Scans for rapid, repeated-pitch declamation (semiquaver/quaver pulses) in the vocal lines, a hallmark of Monteverdi's later dramatic works.
* **Dissonant Word Stress (+5 pts):** Triggered when a reconstructed "meaningful" word lands on a non-consonant vertical stack.

## Key Analytical Features

### The Evolution of the Basso
The project tracks the transition of the Basso from a melodic participant in a polyphonic web to a functional **Basso Continuo**. Metrics include:
* **Average Note Duration:** Increasing as the bass becomes more foundational.
* **Leap Ratio:** Analyzing the angularity of the bass line vs. its scalar movement.

### Dissonance & Madrigalisms
By analyzing the "Top Dissonant Words," the study reveals how Monteverdi’s use of "harsh" harmonies moved from traditional poetic triggers (*morte*, *dolore*) to more abstract expressive choices in the *Seconda Pratica*.

### Stile Concitato Analysis
The analysis highlights the spike in "agitated" textures in Book 8 (*Madrigali guerrieri, et amorosi*), quantifying the frequency of rapid rhythmic repetitions used to depict anger or bellicose energy.

## Summary of Results
The results clearly delineate the boundary between the "Two Practices." 
- **Books 1–4:** Characterized by following the Contrappunto rules.
- **Books 5–9:** Show a significant increase in Basso "pedal" behavior, higher dissonance counts on specific emotive keywords, and the emergence of the *Stile Concitato* as a primary structural device.

---
## Getting Started

### Prerequisites
* Python 3.8+
* `music21`, `pandas`, `seaborn`, `matplotlib`

### Installation
```bash
git clone [https://github.com/your-repo/monteverdi-analysis.git](https://github.com/your-repo/monteverdi-analysis.git)
cd monteverdi-analysis
pip install -r requirements.txt
