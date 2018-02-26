import random as r


def gen_name(min_len, max_len):
    length = r.randint(min_len, max_len)
    name = ''
    while len(name) < length:
        if len(name) == 0:
            name += r.choice(consonants+start_consonants+((vowels + dub_vow)*2))
            continue
        if name[-1] in consonants + ["'"]:
            if length - len(name) == 1:
                name += r.choice(vowels)
            else:
                name += r.choice(vowels + dub_vow)
        else:
            if length - len(name) == 1:
                name += r.choice(consonants)
            elif length - len(name) == 2:
                name += r.choice(end_consonants)
            else:
                second = r.randint(0, 1)
                name += r.choice(consonants + ["'"])
                if name[-1] == "'":
                    continue
                name += r.choice(consonants) * second
    name = name[0].capitalize() + name[1:]
    return name


consonants = [
    'b', 'c', 'd', 'f', 'g',
    'h', 'j', 'k', 'l', 'm',
    'n', 'p', 'q', 'r', 's',
    't', 'v', 'w', 'x', 'z',
    ]

start_consonants = [
    'th', 'ch', 'sh', 'gh', 'ph',
    'bl', 'br', 'cr', 'dh', 'dr',
    'fh', 'fl', 'fr', 'bw', 'fw',
    'gl', 'gn', 'gr', 'gw', 'jh',
    'kh', 'kn', 'kr', 'mn', 'pl',
    'pn', 'pr', 'qr', 'rh', 'sk',
    'sl', 'sm', 'sn', 'sp', 'sq',
    'st', 'sw', 'rw', 'tr', 'ts',
    'tw', 'vl', 'wh', 'wr', 'zh',
]


end_consonants = [
    'bm', 'bn', 'br', 'bs', 'bt',
    'ch', 'ck', 'ct', 'dh', 'dl',
    'dr', 'ds', 'dt', 'fl', 'fr',
    'fs', 'ft', 'gs', 'hl', 'hn',
    'hr', 'kh', 'kr', 'lb', 'lm',
    'ln', 'lp', 'lf', 'ld', 'lt',
    'mn', 'mp', 'mr', 'ms', 'nl',
    'ns', 'nt', 'ph', 'ps', 'pt',
    'rb', 'rd', 'rh', 'rk', 'rl',
    'rm', 'rn', 'rp', 'rq', 'rs',
    'rt', 'rx', 'rz', 'sh', 'sk',
    'sm', 'sp', 'st', 'th', 'tl',
    'vs', 'wl', 'xh', 'xl', 'xx',
    'zl', 'zn', 'zr', 'zz'
]


vowels = [
    'a', 'e', 'i', 'o', 'u',
    'y']

dub_vow = [
    'ae', 'ai', 'io', 'ou',
    'ei', 'ao', 'au', 'ui', 'iu',
    'ua', 'oo', 'ee', 'uy', 'oy',
    'ay', 'ia',
]