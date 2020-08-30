import random

def answer_from_distribution(dist):
    r = random.random()
    prob_sum = 0.0
    for key in dist.keys():
        prob_sum += dist[key]
        if prob_sum >= r:
            return key, dist
    return None, dist

def multiply_dict(dct, val):
    dct2 = {}
    for key in dct.keys():
        dct2[key] = dct[key] * val
    return dct2

def add_to_dict(dct, val):
    dct2 = {}
    for key in dct.keys():
        dct2[key] = dct[key] + val
    return dct2

def add_dicts(dct1, dct2):
    ans = {}
    all_keys = []
    if dct1.keys()!= None:
        all_keys.extend(dct1.keys())
    if dct2.keys()!= None:
        all_keys.extend(dct2.keys())

    for key in all_keys:
        if key not in dct1.keys():
            ans[key] = dct2[key]
        elif key not in dct2.keys():
            ans[key] = dct1[key]
        else:
            ans[key] = dct1[key] + dct2[key]
    return ans
        
    
