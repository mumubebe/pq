def odig(dct, keys, value=None, condition=True):
    if type(dct) == dict and condition:
        for key in keys:
            try:
                dct = dct[key]
            except KeyError:
                return value
        return dct
    else:
        return value