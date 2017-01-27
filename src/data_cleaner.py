import pandas as pd
import json
import glob

from read_abc import construct_tune_list

'''
Reads in the data from all the different sources and puts them all in a pandas df. Drops the apropriate columns and cleans out any rows that have empty 'abc', 'meter', 'or type'
'''
def read_data(filepath):
    data = pd.read_json(filepath)

    #Read in oneill's 1001 tunes.
    tunes1001 = construct_tune_list(glob.glob('../data/oneills/1001/T/*.abc'))
    data = data.append(tunes1001)
    tunes1850 = construct_tune_list(glob.glob('../data/oneills/1850/X/*.abc'))
    data = data.append(tunes1850)
    data = transform_to_base_key(data)
    dropcols = ['field10', 'field11', 'field12', 'field13', 'field14',
            'field15', 'field16', 'field17', 'field18', 'field19', 'field20', 'field21', 'field22']
    data = data.drop(dropcols, axis=1)
    data.reset_index(drop=True)
    data_null = data.isnull().unstack()
    t = data_null[data_null]
    drop_rows = list(t['base_keys'].index)
    data.drop(drop_rows, inplace=True)
    data.reset_index(drop=True)

    print len(data)
    return data


def transform_to_base_key(df):
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
    df['base_keys'] = df['mode'].map(base_keys)
    return df
