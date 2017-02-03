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
        Instantiates a tunefragment from the input.

        Parameters
        ----------
        data : dict-like
            Pandas Series or dict that contains 'mode' and 'abc' keys.
        """
        self.data = data
        self._temp_dir = mkdtemp()
        self._abc_file = os.path.join(self._temp_dir, 'current.abc')
        self._midi_file = os.path.join(self._temp_dir, 'current.mid')
        self.create_abcfile()
        self._convert_abc_2_midi()


    def play(self):
        """
        Takes the current data and plays it.
        """
        subprocess.call(['timidity', self._midi_file])


    def sheet_music(self):
        pass

    def create_abcfile(self, filename=None):
        if filename is None:
            filename = self._abc_file
        with open(filename, 'w') as f:
            f.write('X:1\n')
            f.write('M:{}\n'.format(self.data['meter']))
            f.write('L:1/16\n'.format())
            if 'type' in self.data:
                f.write('T:{}\n'.format(self.data['type']))
            f.write('K:{}\n'.format(self.data['mode']))
            f.write(self.data['abc'])


    def _convert_abc_2_midi(self):
        '''
        INPUT: .abc file
        Takes a .abc with at least an X: and a K: and a minimum fragment of
        one bar if necessary padded with z's that will still play
        '''
        subprocess.call(['abc2midi', self._abc_file, '-BF','-o', self._midi_file])



    def _pad_fragement_with_breaks(self):
        #takes a fragement and fils it with zs until the minimum has been met.
        pass
