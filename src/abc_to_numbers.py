import numpy as np
import pandas as pd
from collections import Counter



possible_keys = {
                'A': 'Amajor',
                'Am': 'Aminor',
                'Ador': 'Adorian',
                'ADor': 'Adorian',
                'Amix': 'Amixolydian',
                'AMix': 'Amixolydian',
                'Aphr': 'Aphrygian',
                'Bb': 'Bbmajor',
                'Bn': 'Bmajor',
                'Bm': 'Bminor',
                'Bdor': 'Bdorian',
                'Bmix': 'Bmixolydian',
                'Bphr': 'Bphrygian',
                'C': 'Cmajor',
                'Cm': 'Cminor',
                'Cdor': 'Cdorian',
                'D': 'Dmajor',
                'Dm': 'Dminor',
                'Ddor': 'Ddorian',
                'DDor': 'Ddorian',
                'Dmix': 'Dmixolydian',
                'DMix': 'Dmixolydian',
                'Dmixm': 'Dmixolydian',
                'Dphr': 'Dphrygian',
                'Dlyd': 'Dlydian',
                'Eb': 'Ebmajor',
                'E': 'Emajor',
                'Em': 'Eminor',
                'Edor': 'Edorian',
                'Emix': 'Emixolydian',
                'F': 'Fmajor',
                'Fdor': 'Fdorian',
                'F#m': 'F#m',
                'Fmix': 'Fmixolydian',
                'G': 'Gmajor',
                'Gm': 'Gminor',
                'Gdor': 'Gdorian',
                'GDor': 'Gdorian',
                'Gmix': 'Gmixolydian',
                'Glyd': 'Glydian'
                }





actual_keys = ['B', 'E', 'A', 'D', 'G', 'C', 'F', 'Bb', 'Eb']

sharps_flats = {'B': ['B#, D#', 'F#', 'G#', 'A#'],
                'E': ['C#', 'D#','F#','G#'],
                'A': ['C#', 'F#', 'G#'],
                'D': ['C#', 'F#'],
                'G': ['C#'],
                'C': [None],
                'F': ['Bb'],
                'Bb': ['Bb', 'Eb'],
                'Eb': ['Bb', 'Eb', 'Ab']
                }

def abc_to_basekeys(df):
    base_keys = {
                'Amajor': 'A',
                'Aminor': 'C',
                'Amixolydian': 'D',
                'Adorian': 'G',
                'Aphrygian': 'F',
                'Bbmajor': 'Bb',
                'Bmajor': 'B',
                'Bminor': 'D',
                'Bmixolydian': 'E',
                'Bdorian': 'A',
                'Bphrygian': 'G',
                'Cmajor': 'C',
                'Cminor': 'Eb',
                'Cdorian': 'Bb',
                'Dmajor': 'D',
                'Dminor': 'F',
                'Dmixolydian': 'G',
                'Ddorian': 'C',
                'Dphrygian': 'Bb',
                'Dlydian': 'A',
                'Ebmajor': 'Eb',
                'Emajor': 'E',
                'Eminor': 'G',
                'Emixolydian': 'A',
                'Edorian': 'D',
                'Fmajor': 'F',
                'Fmixolydian': 'Bb',
                'Fdorian': 'Eb',
                'F#m': 'A',
                'Gmajor': 'G',
                'Gminor': 'Bb',
                'Gmixolydian': 'C',
                'Gdorian': 'F',
                'Glydian': 'D'
                }
        df.replace({'mode': base_keys})


df = pd.DataFrame(0, index=possible_keys)

import re

abc = """
E|A2E Ace|ede ABA|=G2D G>Bc|dcd =G2B|A2E ABd|e2f =gfg|edc Bcd|ecA A2:|
|:a|aga A2a|aga A2=g|=gfg =G2g|=gfg =G2B|c2c d2d|e2f =gfg|edc Bcd|ecA A2:|
"""

abc = "|=G2D G>Bc|dcd =G2B|A2E ABd|e2f =gfg|"

accidentals = {
   "A": '',
   "B": '',
   "C": '',
   "D": '',
   "E": '',
   "F": '',
   "G": ''
}

pattern = r"[\^=_]?[a-gA-G][,\']?\d?"
offset = 0
while offset < len(abc):
   if abc[offset] == '|':
       for note in accidentals:
           accidentals[note] = ''
   match = re.match(pattern, abc[offset:])
   if not match:
       offset += 1
       continue
   note_str = match.group(0)
   if note_str[0] in ('^', '=', '_'):
       uppercase_note = note_str[1].upper()
       accidentals[uppercase_note] = note_str[0]
   else:
       uppercase_note = note_str[0].upper()
       note_str = accidentals[uppercase_note] + note_str
   print(note_str)
   offset += len(note_str)
