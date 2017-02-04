import pandas as pd
import json
import glob

'''
Reads in the data from all the different sources and puts them all in a pandas df. Drops the apropriate columns and cleans out any rows that have empty 'abc', 'meter', 'or type'
'''

def read_data(filepath):
    data = pd.read_json(filepath)

    # Read in oneill's 1001 tunes.
    # tunes1001 = construct_tune_list(glob.glob('../data/oneills/1001/T/*.abc'))
    # data = data.append(tunes1001)
    # tunes1850 = construct_tune_list(glob.glob('../data/oneills/1850/X/*.abc'))
    # data = data.append(tunes1850)
    # Transform all relative modes to their base keys.
    data = transform_to_base_key(data)
    # Drop the columns that are mistken entries.
    dropcols = ['field10', 'field11', 'field12', 'field13', 'field14',
                'field15', 'field16', 'field17', 'field18', 'field19',
                'field20', 'field21', 'field22']
    data.drop(dropcols, axis=1, inplace=True)
    # Drop all rows with empty values.
    data = data.dropna()
    data = drop_data_subset(data, 'type', 'mazurka')
    data = drop_data_subset(data, 'type', 'strathspey')
    data = drop_data_subset(data, 'type', 'three-two')
    data['mode'] =data['mode'].astype(str)
    data.reset_index(drop=True, inplace=True)
    return data


def drop_data_subset(df, colname, name):
    # Drop the definitly non-Irish tunes.
    to_drop = list(df[df[colname] == name].index)
    df.drop(to_drop, axis=0, inplace=True)
    return df


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

def abc_to_dict(abc_file):
    with open(abc_file) as f:
        tune = {"tune":None,
                "setting":None,
                "name":None,
                "type":None,
                "meter":None,
                "mode":None,
                "abc":'',
                "date":None,
                "username":"O'Neill's"}
        for line in f:
            try:
                key, value = line.split(':', 1)
            except:
                tune['abc'] += line
            key = key.strip()
            value = value.strip()


            if len(key) != 1 or not key[0].isalpha():
                tune['abc'] += line
            if key == 'T':
                tune['name'] = value
            elif key == 'R':
                tune['type'] = value
            elif key == 'M':
                tune['meter'] = value
            elif key == 'K':
                tune['mode'] = possible_keys[value]
            else:
                continue
    return tune

def construct_tune_list(files):
    if len(files) == 0:
        raise RuntimeError("Filelist is empty.")
    return [abc_to_dict(f) for f in files]


# def set_to_possible_keys(df):
#     possible_keys = {
#                 'A': 'Amajor',
#                 'Am': 'Aminor',
#                 'Ador': 'Adorian',
#                 'ADor': 'Adorian',
#                 'Amix': 'Amixolydian',
#                 'AMix': 'Amixolydian',
#                 'Aphr': 'Aphrygian',
#                 'Bb': 'Bbmajor',
#                 'Bn': 'Bmajor',
#                 'Bm': 'Bminor',
#                 'Bdor': 'Bdorian',
#                 'Bmix': 'Bmixolydian',
#                 'Bphr': 'Bphrygian',
#                 'C': 'Cmajor',
#                 'Cm': 'Cminor',
#                 'Cdor': 'Cdorian',
#                 'D': 'Dmajor',
#                 'Dm': 'Dminor',
#                 'Ddor': 'Ddorian',
#                 'DDor': 'Ddorian',
#                 'Dmix': 'Dmixolydian',
#                 'DMix': 'Dmixolydian',
#                 'Dmixm': 'Dmixolydian',
#                 'Dphr': 'Dphrygian',
#                 'Dlyd': 'Dlydian',
#                 'Eb': 'Ebmajor',
#                 'E': 'Emajor',
#                 'Em': 'Eminor',
#                 'Edor': 'Edorian',
#                 'Emix': 'Emixolydian',
#                 'F': 'Fmajor',
#                 'Fdor': 'Fdorian',
#                 'F#m': 'F#m',
#                 'Fmix': 'Fmixolydian',
#                 'G': 'Gmajor',
#                 'Gm': 'Gminor',
#                 'Gdor': 'Gdorian',
#                 'GDor': 'Gdorian',
#                 'Gmix': 'Gmixolydian',
#                 'Glyd': 'Glydian'
#                 }
#     df['mode'] = df['mode'].map(possible_keys)
#     return df
