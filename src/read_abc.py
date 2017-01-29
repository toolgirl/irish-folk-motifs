import json
# Dictionary of possible keys.
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
