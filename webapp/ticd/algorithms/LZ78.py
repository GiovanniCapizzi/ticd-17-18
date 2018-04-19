import time


def lz78_encoded(s: str):
    dict_ = dict()
    dict_[''] = 0
    i = 0
    output = list()
    N = len(s)
    while i < N:
        sb = s[i:]
        pos, succ, l = search(dict_, sb)
        i += l
        output.append((pos, succ))
    return output


def search(dict_, sb):
    a = ''
    for c in sb:
        a += c
        if a not in dict_:
            break
    dict_[a] = len(dict_)
    return dict_[a[:-1]], a[-1], len(a)


def lz78_decoded(list_: list):
    dict_ = dict()
    dict_[0] = ''
    s = ''
    for t in list_:
        tmp = dict_[t[0]] + t[1]
        dict_[len(dict_)] = tmp
        s += tmp
    return s


def main():
    lines = 'abababababab'
    start = time.time()
    encoded = lz78_encoded(lines)
    step = time.time()
    decoded = lz78_decoded(encoded)
    end = time.time()
    print('encoding :' + str(step - start))
    print('decoding :' + str(end - step))
    print('total :' + str(end - start))
    assert lines == decoded


if __name__ == '__main__':
    main()
