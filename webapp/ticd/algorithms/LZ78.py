import time


def encode(s: str):
    codebook = dict()
    codebook[''] = 0
    i = 0
    count = 1
    output = list()
    N = len(s)
    while i < N:
        ii = i
        while ii < N:
            pattern = s[i:(ii + 1)]
            if pattern in codebook:
                ii += 1
            else:
                break
        codebook[pattern] = count
        output.append((codebook[pattern[:-1]], s[ii] if ii < N else s[ii - 1]))
        count += 1
        i += len(pattern)
    return output


def decode(list_: list):
    codebook = dict()
    codebook[0] = ''
    s = ''
    for t in list_:
        tmp = codebook[t[0]] + t[1]
        codebook[len(codebook)] = tmp
        s += tmp
    return s


def main():
    lines = 'ciao a tutti'
    start = time.time()
    encoded = encode(lines)
    step = time.time()
    decoded = decode(encoded)
    end = time.time()
    print('encoding :' + str(step - start))
    print('decoding :' + str(end - step))
    print('total :' + str(end - start))
    assert lines == decoded


if __name__ == '__main__':
    main()
