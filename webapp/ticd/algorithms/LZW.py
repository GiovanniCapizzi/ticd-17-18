# coding=utf-8
from typing import Dict, List

from .utils import input_example

#    _                               _      _______              _    _      _      _
#   | |                             | |    |___  (_)            | |  | |    | |    | |
#   | |     ___ _ __ ___  _ __   ___| |______ / / ___   ________| |  | | ___| | ___| |__
#   | |    / _ \ '_ ` _ \| '_ \ / _ \ |______/ / | \ \ / /______| |/\| |/ _ \ |/ __| '_ \
#   | |___|  __/ | | | | | |_) |  __/ |    ./ /__| |\ V /       \  /\  /  __/ | (__| | | |
#   \_____/\___|_| |_| |_| .__/ \___|_|    \_____/_| \_/         \/  \/ \___|_|\___|_| |_|
#                        | |
#                        |_|


__algorithm__ = "LZW"
__author__ = 'Giovanni Capizzi'
__group__ = "LZ"


@input_example(text='bcababbcbcbaaaabbc')
def encode(text: str, logging: bool = False) -> Dict:
    """
    >>> encode("bcababbcbcbaaaabbc")
    {'encoded': [2, 3, 1, 2, 6, 4, 9, 1, 11, 8, 3], 'codebook': {1: 'a', 2: 'b', 3: 'c'}}
    """

    # Initialization -----------------------
    in_alph = sorted(set(text))
    codebook = {}
    inverted_codebook = {}
    for index, item in enumerate(in_alph):
        codebook[item] = index + 1
        inverted_codebook[index + 1] = item

    # Position
    cursor = 0
    limit = len(text)
    output = []

    if logging:
        print("CODING...\n", text)

    # End of Initialization -----------------

    while cursor < limit:
        current = text[cursor]

        if logging:
            print("The current word is", current, 'at index', cursor)

        # searching the longest word in the dictionary
        relative_index = cursor + 1

        while text[cursor: relative_index] in codebook:
            relative_index += 1
            if relative_index > limit:
                # end of string, outputting remaining text,
                # relative_index bound doesn't matter in python substring
                coding_word = text[cursor:relative_index]
                output.append(codebook[coding_word])
                if logging:
                    print("and outputting the remaining", codebook[coding_word], "value")
                return {'encoded': output, 'codebook': inverted_codebook}

        # add this new word to the codebook
        word = text[cursor:relative_index]
        codebook[word] = len(codebook) + 1
        # outputting value
        coding_word = text[cursor:relative_index - 1]
        output.append(codebook[coding_word])

        if logging:
            print("I'm putting", word, "in the dictionary")
            print("outputting", codebook[coding_word], "value")
            print("moving cursor from ", cursor, "to ", cursor + len(coding_word))

        cursor += len(coding_word)


@input_example(encoded='2 3 1 2 6 4 9 1 11 8 3', codebook='{"1":"a","2":"b","3":"c"}')
def decode(encoded: List[int], codebook: Dict, logging: bool = False) -> str:
    """
    >>> decode([2, 3, 1, 2, 6, 4, 9, 1, 11, 8, 3], {1: 'a', 2: 'b', 3: 'c'})
    'bcababbcbcbaaaabbc'

    :param encoded:
    :param codebook:
    :param logging:
    :return output:
    """
    # Initialization -----------------------

    codebook = {int(key): value for key, value in codebook.items()}

    output = ''
    # last word added
    last = ''

    # End of Initialization -----------------

    for item in encoded:
        if item in codebook:
            current_item = codebook[item]
            output += current_item

            # adding new key to codebook
            candidate = last + current_item[0]
            c_len = len(candidate)
            if c_len > 1:
                # For initials characters
                # O(1) len sui dict
                codebook[len(codebook) + 1] = candidate

            last = current_item
        else:
            adding = last + last[0]
            output += adding
            codebook[len(codebook) + 1] = adding
            last = adding

        if logging:
            print("{Item %s,Codebook[item] %s,codebook %s}" % (item, codebook[item], codebook))

    return output


# TEST CODE --------------

if __name__ == '__main__':
    in_text = "La signora Aurora ha programmato in Java un software per la gestione dei ristoranti."
    # _in_text = "bcababbcbcbaaaabbc
    print("Testing code ")
    result = encode(in_text)
    code, inverted_cb = result['encoded'], result['codebook']
    print(code, "\n", decode(code, inverted_cb))
