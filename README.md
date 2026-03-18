# Monteverdi's Madrigals - A Statistical Analysis

This repository contains a computational analysis of Claudio Monteverdi’s nine books of madrigals. The project tracks the shift from the Renaissance polyphonic tradition (**Prima Pratica**) to the early Baroque emphasis on monody and harmonic support (**Seconda Pratica**).

## 📊 Analysis Overview

The study focuses on three primary musical dimensions:
1.  **The Evolution of the Basso Role**: Measuring the transition from melodic counterpoint to harmonic "pedal" support.
2.  **Dissonance & Madrigalisms**: Reconstructing full lyrics to identify which words (e.g., *morire*, *dolce*, *cruda*) Monteverdi most frequently paired with vertical dissonances.
3.  **Formalizing Sprezzatura**: A heuristic-based approach to finding "hotspots" of expressive freedom (*tempo dell'animo*) where the upper voices defy strict rhythm over a stable bass.

---

## 🛠 Methodology

The analysis is powered by `music21` and custom Python heuristics. The core logic is divided into two primary analytical pipelines:

### 1. Dissonance & Text Mapping
* **`build_note_to_word_map()`**: Reconstructs full Italian words from fragmented MusicXML syllables, allowing for accurate text-to-music alignment.
* **`analyze_dissonant_words()`**: Scans vertical chords across all parts. If a chord is dissonant and contains more than two pitch classes, the function captures the specific word being sung.

### 2. Heuristic Sprezzatura Finder
The function **`find_all_sprezzatura()`** evaluates measures on a **0–10 scale** based on the following weights:

| Points | Heuristic | Description |
| :--- | :--- | :--- |
| **+2** | **Sustained Bass Pedal** | Basso notes with a duration $\ge$ 2.0 quarter lengths (Support role). |
| **+3** | **Stile Concitato** | Rapid repeated-note declamation in vocal parts. |
| **+5** | **Dissonant Lyrics** | Syllables landing on unprepared or unresolved vertical dissonances. |

---

## 📈 Key Findings

### The Basso Role
As Monteverdi moved toward the *Seconda Pratica* (Books 5–9), the bass line's **Average Duration** increased significantly, signaling a move away from melodic equality toward a "Harmonic Pedal" function. Simultaneously, the **Leap Ratio** (movement by leap vs. step) fluctuates, reflecting the emergence of the *Basso Continuo* as a functional harmonic driver.

### Dissonance Trends
* **Book 1** shows a high ratio of unprepared dissonance (0.47), likely due to experimental "madrigalisms."
* **Book 8 (*Guerrieri, et Amorosi*)** marks the peak of **Stile Concitato**, with a massive spike in rapid repeated notes per piece compared to the earlier books.

### Sprezzatura Hotspots
In "Cruda Amarilli" (Book 5, Measure 1), the algorithm identifies perfect scores of **10/10**, where sustained bass pedals anchor aggressive vocal declamations on highly dissonant words—quantifying the "expressive freedom" Caccini termed *Tempo dell'animo*.

---

## 🚀 Getting Started

### Prerequisites
* Python 3.8+
* `music21`, `pandas`, `seaborn`, `matplotlib`

### Installation
```bash
git clone [https://github.com/your-repo/monteverdi-analysis.git](https://github.com/your-repo/monteverdi-analysis.git)
cd monteverdi-analysis
pip install -r requirements.txt
