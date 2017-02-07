# Copyright (C) 2017  Zia Rauwolf. See LICENSE.txt

import subprocess
import pandas as pd
from tempfile import mkdtemp
import os.path


class TuneFragment(object):
    """
    Takes in a row of a pandas DataFrame() or a dictionary and plays it as midi.
    """

    def __init__(self, data):
        """
        Creates a .abc file and plays it with timidity from a text file using abc2midi.

        Parameters
        ----------
        data : .txt
            Text file that contains abc notation without any of the required notations for .abc.

        Attributes
        ----------
        _temp_dir : tempfile
            Temporary directory to put the working files in.
        _abc_file : abc file
            Path and file for temporary abc file.
        _midi_file : midi file
            Path and name for temporary midi file.
        """
        self.data = data
        self._temp_dir = mkdtemp()
        self._abc_file = os.path.join(self._temp_dir, 'current.abc')
        self._midi_file = os.path.join('/Users/zia/galvanize', 'current.mid')
        self.create_abcfile()
        self._convert_abc_2_midi()


    def play(self):
        """
        Takes the current data and plays it.
        """
        subprocess.call(['timidity', self._midi_file])

    def create_abcfile(self, filename=None):
        '''
        Writes the necessary lines to convert .txt to .abc.
        '''
        if filename is None:
            filename = self._abc_file
        else:
            self._abc_file = filename
        with open(filename, 'w') as f:
            f.write('X:1\n')
            f.write('M:{}\n'.format(self.data['meter']))
            f.write('L:1/16\n'.format())
            if 'type' in self.data:
                f.write('T:{}\n'.format(self.data['type']))
            f.write('K:{}\n'.format(self.data['mode']))
            f.write('%%MIDI program 73\n') #plays flute (piano is program 0.)
            f.write(self.data['abc'])

    def _convert_abc_2_midi(self):
        '''
        INPUT: .abc file
        Takes a .abc with at least an X: and a K: and a minimum fragment of
        one bar if necessary padded with z's that will still play
        '''
        subprocess.call(['abc2midi', self._abc_file, '-BF','-o', self._midi_file])
