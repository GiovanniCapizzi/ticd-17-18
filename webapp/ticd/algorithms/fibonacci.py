# coding=utf-8
sequences = [0, 1]

# initial computation

for i in range(100):
    sequences.append(sequences[-1] + sequences[-2])


def encode(integers):
    """
    >>> encode([5, 5, 5, 8, 13])
    '0001100011000110000110000011'

    :param integers:
    :return:
    """
    symbols = {}

    for integer in set(integers):
        tmp = integer
        fns = []

        while tmp > 0:
            value = max(filter(lambda x: x <= tmp, sequences))
            fns.append(sequences.index(value) - 2)
            tmp -= value

        symbols[integer] = ''.join(['1' if x in fns else '0' for x in range(max(fns) + 1)]) + '1'

    return ''.join([symbols[integer] for integer in integers])


def decode(text):
    """
    >>> decode('0001100011000110000110000011')
    [5, 5, 5, 8, 13]

    :param text:
    :return:
    """
    integers = map(lambda x: x + '1', filter(lambda x: x, text.split('11')))
    return [sum([sequences[x + 2] for x, value in enumerate(integer) if value == '1']) for integer in integers]


if __name__ == '__main__':
    import time

    start_time = time.clock()
    to_encode = [5, 5, 5, 8, 13]
    encoded = encode(to_encode)
    print(" >> encoding", to_encode, " to ", encoded)
    decoded = decode(encoded)
    print(" >> decoding", encoded, 'to', decoded)
    print("execution time", time.clock() - start_time, "seconds")
