def odig(dct, keys, condition=True):
    if type(dct) == dict and condition:
        for key in keys:
            try:
                dct = dct[key]
            except KeyError:
                return None
        return dct
    else:
        return None