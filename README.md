Analyzing Sprezzatura in Monteverdi's Madrigals: The Seconda Pratica
Project Overview
This project analyzes Claudio Monteverdi's Book 5 of Madrigals (with a primary focus on Cruda Amarilli) to find empirical, notational evidence of sprezzatura. Historically, sprezzatura in the Seconda Pratica was not a generalized rhythmic freedom, but rather a speech-like delivery (canto) where vocal lines are rhythmically displaced against a strict, unyielding tactus.

By separating the Basso Continuo (the tactus anchor) from the upper vocal lines, this Python workflow identifies instances where voices enter on off-beats against a held bass note, effectively mapping the composer's written-out emotional friction.

Dataset Acknowledgment
The data driving this analysis is extracted from the open-source Monteverdi Madrigals Corpus compiled by the Digital and Cognitive Musicology Lab (DCMLab).

Source Repository: https://github.com/DCMLab/monteverdi_madrigals

Format: The scores are parsed using the ms3 library, which extracts MuseScore 3.6.2 files into tabular .tsv formats representing notes, chords, measures, and harmonies.

Workflow and Methodology
1. Environment Setup and Data Loading
The pipeline begins by cloning the DCMLab repository and utilizing the ms3 parser and pandas to load the TSV files. The data is filtered specifically to extract Book 5, the landmark publication where Monteverdi explicitly defended the Seconda Pratica.

2. Extracting the Tactus Framework
To measure rhythmic displacement, the score is split into two distinct layers:

The Basso Continuo (Anchor): The lowest staff in the score, acting as the mathematical, stable tactus.

The Vocal Lines (Sprezzatura Layer): The upper staves carrying the text.
The script calculates both a local_offset (the beat's position within a specific measure) and a general_offset (an absolute timeline from the beginning of the piece) to plot events chronologically.

3. Identifying Rhythmic Displacements
The core algorithm iterates through the vocal lines to find syncopations and anticipations. It specifically flags fractional metrical positions (off-beats) where the Basso Continuo is holding a steady note without attacking a new one. This friction between the voice and the bass is the structural footprint of sprezzatura.

4. Mapping Lyrics to Displacements
Because sprezzatura is a technique designed to serve the oration and the affetto (passion) of the text, the final step cross-references the rhythmic displacements with the chords dataset. This extracts the exact poetic syllables sung on the displaced notes, revealing which specific words Monteverdi chose to emphasize.

Requirements
Python 3.11+

ms3 (>= 2.6.0)

pandas (>= 2.0.0)

jupyterlab
